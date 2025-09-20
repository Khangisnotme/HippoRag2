"""
generation_evaluator.py

Module đánh giá hiệu quả của khâu generation trong hệ thống RAG.
Tính toán các chỉ số:
  - BLEU-1, BLEU-2, BLEU-3, BLEU-4
  - Rouge-L
  - F1 (token overlap)
  - LLM-based evaluation (overall_score và detailed_scores)
  - Phân tích thông tin thiếu (missing_information)
  - Phát hiện hallucinations
  - Đánh giá chất lượng ngôn ngữ (answer_quality)

Đầu vào:
  - question: câu hỏi gốc
  - answer: câu trả lời do hệ thống sinh ra
  - documents: danh sách Document tham khảo làm context
  - reference_answer (optional): câu trả lời chuẩn để so sánh BLEU/Rouge/F1

Đầu ra:
  - GenerationEvaluationResult chứa tất cả metrics và phân tích bổ sung.
"""

import re
import json
import numpy as np
from typing import List, Dict, Any, Optional
from collections import Counter
from dataclasses import dataclass, field
from dotenv import load_dotenv

from langchain_core.documents import Document
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# Nạp biến môi trường (ví dụ API key)
load_dotenv()

@dataclass
class GenerationEvaluationResult:
    """Lưu trữ kết quả đánh giá cho một câu trả lời."""
    question: str
    answer: str
    llm_score: float
    detailed_scores: Dict[str, float]
    bleu_1: float
    bleu_2: float
    bleu_3: float
    bleu_4: float
    rouge_l: float
    f1: float
    missing_information: List[str]
    hallucinations: List[str]
    answer_quality: Dict[str, Any]
    llm_raw_response: str = field(repr=False)

class GenerationEvaluator:
    """
    Class đánh giá hiệu quả khâu generation trong hệ thống RAG.

    Tính năng chính:
      1. BLEU-n (n=1..4) với Brevity Penalty
      2. Rouge-L dựa trên Longest Common Subsequence (LCS)
      3. F1 token overlap
      4. LLM-based evaluation (overall_score, detailed_scores, feedback)
      5. Phát hiện thông tin thiếu
      6. Phát hiện hallucinations
      7. Đánh giá ngôn ngữ (độ dài, ngữ pháp, logic, readability)
    """

    def __init__(
        self,
        model_name: str = "gpt-4o-mini",
        temperature: float = 0.0,
        evaluation_prompt: Optional[str] = None
    ):
        """
        Khởi tạo evaluator với cấu hình LLM và prompt đánh giá.

        Args:
          model_name: Tên model OpenAI
          temperature: Độ sáng tạo (0.0–1.0)
          evaluation_prompt: Template system prompt cho LLM
        """
        if evaluation_prompt is None:
            evaluation_prompt = """
Bạn là chuyên gia đánh giá chất lượng câu trả lời của hệ thống RAG.
Đầu ra phải là JSON với cấu trúc:
{{
  "overall_score": [điểm từ 0-100],
  "detailed_scores": {{
    "accuracy": [0-100],
    "completeness": [0-100],
    "relevance": [0-100],
    "clarity": [0-100],
    "consistency": [0-100]
  }},
  "feedback": {{
    "accuracy_reason": "",
    "completeness_reason": "",
    "relevance_reason": "",
    "clarity_reason": "",
    "consistency_reason": "",
    "overall_assessment": ""
  }}
}}
Chỉ trả về đúng JSON, không kèm text nào khác."""
        # Khởi tạo chain cho LLM
        self.llm = ChatOpenAI(model_name=model_name, temperature=temperature)
        self.eval_prompt = ChatPromptTemplate.from_messages([
            ("system", evaluation_prompt),
            ("human", """Tài liệu tham khảo:
{context}

Câu hỏi: {question}

Câu trả lời: {answer}

Đánh giá câu trả lời (JSON):""")
        ])
        self.chain = (
            {"context": RunnablePassthrough(),
             "question": RunnablePassthrough(),
             "answer": RunnablePassthrough()}
            | self.eval_prompt
            | self.llm
            | StrOutputParser()
        )

    def evaluate_answer(
        self,
        question: str,
        answer: str,
        documents: List[Document],
        reference_answer: Optional[str] = None
    ) -> GenerationEvaluationResult:
        """
        Đánh giá một câu trả lời.

        Trả về tất cả metrics và phân tích bổ sung.
        """
        # Chuẩn bị context
        context = "\n\n".join(doc.page_content for doc in documents)
        # Gọi LLM để lấy JSON đánh giá
        raw_resp = self.chain.invoke({
            "context": context,
            "question": question,
            "answer": answer
        })
        # Parse JSON response
        try:
            data = self._parse_json_response(raw_resp)
            llm_score = data.get("overall_score", 0.0)
            detailed = data.get("detailed_scores", {})
        except Exception:
            llm_score = 0.0
            detailed = {}

        # Reference-based metrics (BLEU/Rouge/F1)
        ref = reference_answer if reference_answer else context
        ref_metrics = self._calculate_reference_metrics(answer, ref)

        # Phân tích thông tin thiếu và hallucinations
        missing = self._find_missing_information(question, answer, documents)
        hallu   = self._detect_hallucinations(answer, documents)
        quality = self._assess_answer_quality(answer)

        return GenerationEvaluationResult(
            question=question,
            answer=answer,
            llm_score=llm_score,
            detailed_scores=detailed,
            bleu_1=ref_metrics["bleu_1"],
            bleu_2=ref_metrics["bleu_2"],
            bleu_3=ref_metrics["bleu_3"],
            bleu_4=ref_metrics["bleu_4"],
            rouge_l=ref_metrics["rouge_l"],
            f1=ref_metrics["f1"],
            missing_information=missing,
            hallucinations=hallu,
            answer_quality=quality,
            llm_raw_response=raw_resp
        )

    def _calculate_reference_metrics(
        self,
        generated: str,
        reference: str
    ) -> Dict[str, float]:
        """
        Tính các chỉ số reference‐based: BLEU-1..4, Rouge-L, F1 token overlap.
        """
        gen_toks = self._tokenize(generated)
        ref_toks = self._tokenize(reference)

        scores: Dict[str, float] = {}
        # BLEU 1..4
        for n in range(1, 5):
            scores[f"bleu_{n}"] = round(
                self._calculate_bleu(gen_toks, ref_toks, n), 4
            )
        # Rouge-L
        scores["rouge_l"] = round(
            self._calculate_rouge_l(gen_toks, ref_toks), 4
        )
        # F1 token overlap
        scores["f1"] = round(
            self._calculate_f1(gen_toks, ref_toks), 4
        )
        return scores

    def _tokenize(self, text: str) -> List[str]:
        """
        Chuyển văn bản thành danh sách token (chữ thường, loại bỏ dấu câu).
        Thêm kiểm tra kiểu dữ liệu để đảm bảo input là string.
        """
        if not isinstance(text, str):
            print(f"⚠️ Cảnh báo: _tokenize nhận input không phải string (type: {type(text)}, value: {repr(text)}). Ép kiểu thành string.")
            text = str(text) # Ép kiểu thành string để tránh lỗi AttributeError
            
        t = text.lower()
        t = re.sub(r"[^\w\s]", " ", t)
        return [w for w in t.split() if w]

    def _get_ngrams(self, tokens: List[str], n: int) -> List[tuple]:
        """Sinh n-gram từ danh sách tokens."""
        if len(tokens) < n:
            return []
        return [tuple(tokens[i:i+n]) for i in range(len(tokens)-n+1)]

    def _calculate_bleu(
        self,
        gen: List[str],
        ref: List[str],
        n: int
    ) -> float:
        """Tính BLEU-n với Brevity Penalty."""
        gen_ngrams = self._get_ngrams(gen, n)
        ref_ngrams = self._get_ngrams(ref, n)
        if not gen_ngrams or not ref_ngrams:
            return 0.0
        gen_cnt = Counter(gen_ngrams)
        ref_cnt = Counter(ref_ngrams)
        matches = sum(min(gen_cnt[g], ref_cnt.get(g,0)) for g in gen_cnt)
        p_n = matches / len(gen_ngrams)
        bp = np.exp(1 - len(ref)/len(gen)) if len(gen) < len(ref) else 1.0
        return bp * p_n

    def _calculate_rouge_l(
        self,
        gen: List[str],
        ref: List[str]
    ) -> float:
        """Tính Rouge-L F1 dựa trên Longest Common Subsequence."""
        m, n = len(gen), len(ref)
        dp = [[0]*(n+1) for _ in range(m+1)]
        for i in range(1, m+1):
            for j in range(1, n+1):
                dp[i][j] = dp[i-1][j-1]+1 if gen[i-1]==ref[j-1] else max(dp[i-1][j], dp[i][j-1])
        lcs = dp[m][n]
        if m == 0 or n == 0:
            return 0.0
        p = lcs / m
        r = lcs / n
        return 2*p*r/(p+r) if (p+r) > 0 else 0.0

    def _calculate_f1(
        self,
        gen: List[str],
        ref: List[str]
    ) -> float:
        """Tính F1 token overlap."""
        set_g, set_r = set(gen), set(ref)
        if not set_g or not set_r:
            return 0.0
        inter = set_g & set_r
        p = len(inter) / len(set_g)
        r = len(inter) / len(set_r)
        return 2*p*r/(p+r) if (p+r) > 0 else 0.0

    def _find_missing_information(
        self,
        question: str,
        answer: str,
        docs: List[Document]
    ) -> List[str]:
        """Dùng LLM để liệt kê các thông tin trong docs nhưng bị thiếu trong answer."""
        context = "\n\n".join(d.page_content for d in docs)
        prompt = ChatPromptTemplate.from_messages([
            ("system", "Liệt kê thông tin quan trọng có trong tài liệu nhưng bị thiếu trong câu trả lời. Mỗi dòng một điểm."),
            ("human", """Tài liệu:
{context}

Câu hỏi: {question}

Câu trả lời: {answer}

Thông tin thiếu:""")
        ])
        chain = prompt | self.llm | StrOutputParser()
        raw = chain.invoke({"context": context, "question": question, "answer": answer})
        return [line.strip() for line in raw.split("\n") if line.strip()]

    def _detect_hallucinations(
        self,
        answer: str,
        docs: List[Document]
    ) -> List[str]:
        """Dùng LLM để liệt kê các thông tin trong answer không có trong tài liệu."""
        context = "\n\n".join(d.page_content for d in docs)
        prompt = ChatPromptTemplate.from_messages([
            ("system", "Liệt kê các thông tin trong câu trả lời KHÔNG có trong tài liệu tham khảo. Mỗi dòng một hallucination."),
            ("human", """Docs:
{context}

Answer: {answer}

Hallucinations:""")
        ])
        chain = prompt | self.llm | StrOutputParser()
        raw = chain.invoke({"context": context, "answer": answer})
        return [line.strip() for line in raw.split("\n") if line.strip()]

    def _assess_answer_quality(self, answer: str) -> Dict[str, Any]:
        """Dùng LLM đánh giá chất lượng ngôn ngữ theo các tiêu chí: độ dài, ngữ pháp, logic, từ vựng."""
        prompt = ChatPromptTemplate.from_messages([
            ("system", "Đánh giá chất lượng ngôn ngữ: độ dài, cấu trúc, ngữ pháp, từ vựng, logic. Trả về JSON."),
            ("human", "Answer: {answer}\n\nAssessment:")
        ])
        chain = prompt | self.llm | StrOutputParser()
        raw = chain.invoke({"answer": answer})
        # Tính thêm độ dài và readability nếu cần
        return {"assessment": raw, "length": len(answer.split())}

    def _parse_json_response(self, text: str) -> Dict[str, Any]:
        """Làm sạch và parse JSON response từ LLM."""
        t = text.strip()
        if t.startswith("```"):
            t = t.strip("```json").strip("```")
        t = t.replace("'", '"')
        t = re.sub(r",(\s*[}\]])", r"\1", t)
        return json.loads(t)


if __name__ == "__main__":
    """Test GenerationEvaluator với ví dụ mẫu."""
    from langchain_core.documents import Document

    docs = [
        Document(page_content="RAG là viết tắt của Retrieval-Augmented Generation.", metadata={}),
        Document(page_content="Hệ thống RAG kết hợp retrieval và generation.", metadata={})
    ]
    question = "RAG là gì?"
    gen_answer = "RAG là phương pháp kết hợp tìm kiếm và sinh văn bản."
    ref_answer = "RAG (Retrieval-Augmented Generation) kết hợp tìm kiếm tài liệu và sinh văn bản."

    evaluator = GenerationEvaluator()
    result = evaluator.evaluate_answer(question, gen_answer, docs, ref_answer)

    print("LLM Score:", result.llm_score)
    print("BLEU-1..4:", result.bleu_1, result.bleu_2, result.bleu_3, result.bleu_4)
    print("Rouge-L:", result.rouge_l, "F1:", result.f1)
    print("Missing Info:", result.missing_information)
    print("Hallucinations:", result.hallucinations)
    print("Language Quality:", result.answer_quality)
