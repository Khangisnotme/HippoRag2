"""
evaluator_generation_for_xlsx.py

Script đánh giá generation từ file Excel với BATCH PROCESSING:

  • Tham số --sheet để chọn sheet input (mặc định baseline_result_QA_raw)
  • Tham số --start_row và --end_row để giới hạn dòng đánh giá
  • Tham số --batch_size để thiết lập kích thước batch (mặc định 10)
  • Tham số --max_workers để thiết lập số worker song song (mặc định 3)

Input sheet chứa các cột:
  - question_id
  - question
  - answer           (sẽ rename thành reference_answer)
  - ai_answer        (sẽ rename thành generated_answer)
  - supporting_facts (VD: "[['doc1',0],['doc2',1]]")

Output sheet "generation_evaluated" với cột:
  • Input nguyên gốc
  • gen_bleu_1..gen_f1
  • gen_overall_score, gen_relevance_score, gen_completeness_score
  • gen_missing_info, gen_hallucinations
  • gen_answer_length, gen_quality_assessment
"""

import pandas as pd
import ast
import argparse
import os
import time
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from dotenv import load_dotenv, find_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock
import threading

from langchain_core.documents import Document
from generation_evaluator import GenerationEvaluator

# Tự động tìm file .env gần nhất trong cây thư mục
env_file = find_dotenv()
if env_file:
    load_dotenv(env_file)
    print(f"✅ Đã tìm thấy và load file .env: {env_file}")
else:
    print("⚠️ Không tìm thấy file .env trong cây thư mục")

def check_openai_api_key():
    """Kiểm tra và lấy OpenAI API key từ biến môi trường."""
    # Debug: in tất cả biến môi trường chứa "OPENAI"
    print("🔍 Debug: Tất cả biến môi trường chứa 'OPENAI':")
    for key, value in os.environ.items():
        if "OPENAI" in key:
            print(f"  {key} = {value[:10]}{'...' if len(value) > 10 else ''}")
    
    api_key = os.getenv("OPENAI_API_KEY")
    print(f"🔍 Debug: os.getenv('OPENAI_API_KEY') = {repr(api_key)}")
    
    if not api_key:
        print("❌ API key is None or empty")
        raise ValueError(
            "❌ Không tìm thấy OpenAI API key!\n"
            "Vui lòng làm theo các bước sau:\n"
            "1. Tạo API key tại: https://platform.openai.com/account/api-keys\n"
            "2. Tạo file .env trong thư mục gốc dự án với nội dung:\n"
            "   OPENAI_API_KEY=sk-your-actual-api-key-here\n"
            "3. Hoặc thiết lập biến môi trường:\n"
            "   - Windows: set OPENAI_API_KEY=sk-your-actual-api-key-here\n"
            "   - Linux/Mac: export OPENAI_API_KEY=sk-your-actual-api-key-here\n"
            "4. Khởi động lại terminal và chạy lại script"
        )
    
    if api_key == "your_api_key" or api_key == "sk-your-actual-api-key-here":
        print("❌ API key is placeholder value")
        raise ValueError(
            "❌ API key là giá trị mẫu!\n"
            "Vui lòng thay thế bằng API key thật của bạn trong file .env hoặc biến môi trường."
        )
    
    if not api_key.startswith("sk-"):
        print(f"❌ API key format invalid: {api_key[:20]}...")
        raise ValueError(
            "❌ Định dạng API key không hợp lệ!\n"
            "API key phải bắt đầu bằng 'sk-'"
        )
    
    print(f"✅ API key hợp lệ: {api_key[:10]}...{api_key[-4:]}")
    return api_key

class BatchProgressTracker:
    """Class theo dõi tiến độ xử lý batch."""
    
    def __init__(self, total_batches: int, total_rows: int):
        self.total_batches = total_batches
        self.total_rows = total_rows
        self.completed_batches = 0
        self.completed_rows = 0
        self.lock = Lock()
        self.start_time = time.time()
    
    def update_progress(self, batch_size: int):
        """Cập nhật tiến độ khi hoàn thành một batch."""
        with self.lock:
            self.completed_batches += 1
            self.completed_rows += batch_size
            
            elapsed_time = time.time() - self.start_time
            progress_pct = (self.completed_rows / self.total_rows) * 100
            
            if self.completed_rows > 0:
                avg_time_per_row = elapsed_time / self.completed_rows
                remaining_rows = self.total_rows - self.completed_rows
                eta_seconds = avg_time_per_row * remaining_rows
                eta_minutes = eta_seconds / 60
                
                print(f"📊 [{self.completed_batches}/{self.total_batches}] "
                      f"{self.completed_rows}/{self.total_rows} dòng "
                      f"({progress_pct:.1f}%) - "
                      f"ETA: {eta_minutes:.1f} phút")

class ExcelGenerationEvaluator:
    """
    Class đánh giá generation từ file Excel với batch processing.
    Đọc dữ liệu, chạy GenerationEvaluator theo batch song song và ghi kết quả.
    """
    
    def __init__(self, model_name: str, temperature: float, batch_size: int = 10, max_workers: int = 3):
        # Kiểm tra API key trước khi khởi tạo
        check_openai_api_key()
        
        self.model_name = model_name
        self.temperature = temperature
        self.batch_size = batch_size
        self.max_workers = max_workers
        
        print(f"⚙️ Cấu hình batch processing:")
        print(f"  • Batch size: {self.batch_size}")
        print(f"  • Max workers: {self.max_workers}")
        print(f"  • Model: {self.model_name}")

    def _create_evaluator(self) -> GenerationEvaluator:
        """Tạo một instance mới của GenerationEvaluator cho mỗi worker."""
        return GenerationEvaluator(
            model_name=self.model_name,
            temperature=self.temperature
        )

    def _process_single_row(
        self, 
        evaluator: GenerationEvaluator,
        row_data: Dict[str, Any], 
        doc_map: Dict[str, Document],
        row_index: int,
        global_index: int
    ) -> Dict[str, Any]:
        """
        Xử lý một dòng dữ liệu duy nhất.
        
        Args:
            evaluator: Instance của GenerationEvaluator
            row_data: Dữ liệu của dòng
            doc_map: Mapping từ doc_id đến Document
            row_index: Index trong batch (0-based)
            global_index: Index toàn cục trong dataset
        
        Returns:
            Dict chứa kết quả đánh giá
        """
        try:
            # Lấy documents cho câu hỏi này
            docs = [doc_map[doc_id] for doc_id in row_data["relevant_docs"] if doc_id in doc_map]
            
            # Ép kiểu các giá trị text thành string
            current_question = str(row_data["question"])
            current_generated_answer = str(row_data["generated_answer"])
            current_reference_answer = str(row_data["reference_answer"])
            
            # Gọi evaluator
            res = evaluator.evaluate_answer(
                question=current_question,
                answer=current_generated_answer,
                documents=docs,
                reference_answer=current_reference_answer
            )
            
            # Thu thập kết quả
            result_entry = {
                # Input columns (giữ nguyên)
                "question_id": row_data["question_id"],
                "question": row_data["question"],
                "reference_answer": row_data["reference_answer"],
                "generated_answer": row_data["generated_answer"],
                "supporting_facts": row_data["supporting_facts"],
                
                # Reference-based metrics
                "gen_bleu_1": res.bleu_1,
                "gen_bleu_2": res.bleu_2,
                "gen_bleu_3": res.bleu_3,
                "gen_bleu_4": res.bleu_4,
                "gen_rouge_l": res.rouge_l,
                "gen_f1": res.f1,
                
                # LLM-based primary scores
                "gen_overall_score": res.llm_score,
                "gen_relevance_score": res.detailed_scores.get("relevance", 0),
                "gen_completeness_score": res.detailed_scores.get("completeness", 0),
                
                # Error analysis
                "gen_missing_info": "; ".join(res.missing_information),
                "gen_hallucinations": "; ".join(res.hallucinations),
                
                # Language quality
                "gen_answer_length": res.answer_quality.get("length", 0),
                "gen_quality_assessment": res.answer_quality.get("assessment", ""),
                
                # Metadata for tracking
                "_batch_index": row_index,
                "_global_index": global_index
            }
            
            return result_entry
            
        except Exception as e:
            print(f"    ❌ Lỗi đánh giá dòng {global_index}: {e}")
            # Trả về entry với giá trị mặc định
            return {
                "question_id": row_data["question_id"],
                "question": row_data["question"],
                "reference_answer": row_data["reference_answer"],
                "generated_answer": row_data["generated_answer"],
                "supporting_facts": row_data["supporting_facts"],
                "gen_bleu_1": 0, "gen_bleu_2": 0, "gen_bleu_3": 0, "gen_bleu_4": 0,
                "gen_rouge_l": 0, "gen_f1": 0,
                "gen_overall_score": 0, "gen_relevance_score": 0, "gen_completeness_score": 0,
                "gen_missing_info": f"Error: {str(e)}", "gen_hallucinations": "",
                "gen_answer_length": 0, "gen_quality_assessment": f"Error: {str(e)}",
                "_batch_index": row_index,
                "_global_index": global_index
            }

    def _process_batch(
        self, 
        batch_data: List[Tuple[int, Dict[str, Any]]], 
        doc_map: Dict[str, Document],
        batch_id: int,
        progress_tracker: BatchProgressTracker
    ) -> List[Dict[str, Any]]:
        """
        Xử lý một batch dữ liệu.
        
        Args:
            batch_data: List các tuple (global_index, row_data)
            doc_map: Mapping từ doc_id đến Document
            batch_id: ID của batch
            progress_tracker: Tracker theo dõi tiến độ
        
        Returns:
            List kết quả đánh giá
        """
        thread_id = threading.get_ident()
        print(f"🔄 Batch {batch_id+1} bắt đầu (Thread {thread_id}) - {len(batch_data)} dòng")
        
        # Tạo evaluator riêng cho batch này
        evaluator = self._create_evaluator()
        
        batch_results = []
        batch_start_time = time.time()
        
        for row_index, (global_index, row_data) in enumerate(batch_data):
            result = self._process_single_row(
                evaluator=evaluator,
                row_data=row_data,
                doc_map=doc_map,
                row_index=row_index,
                global_index=global_index
            )
            batch_results.append(result)
        
        batch_time = time.time() - batch_start_time
        avg_time_per_row = batch_time / len(batch_data)
        
        print(f"✅ Batch {batch_id+1} hoàn thành (Thread {thread_id}) - "
              f"{batch_time:.1f}s ({avg_time_per_row:.2f}s/dòng)")
        
        # Cập nhật tiến độ
        progress_tracker.update_progress(len(batch_data))
        
        return batch_results

    def evaluate_excel(
        self,
        input_path: Path,
        output_path: Path,
        sheet_name: str,
        start_row: Optional[int] = None,
        end_row: Optional[int] = None
    ) -> None:
        """
        Đánh giá generation từ file Excel với batch processing.
        
        Args:
            input_path: Đường dẫn file Excel đầu vào
            output_path: Đường dẫn file Excel đầu ra
            sheet_name: Tên sheet chứa dữ liệu
            start_row: Dòng bắt đầu (0-based, inclusive)
            end_row: Dòng kết thúc (0-based, exclusive)
        """
        print(f"📖 Đọc file: {input_path}")
        print(f"📄 Sheet: {sheet_name}")
        
        # Kiểm tra file tồn tại
        if not input_path.exists():
            raise FileNotFoundError(f"Không tìm thấy file: {input_path}")
        
        # Đọc sheet generation
        try:
            df = pd.read_excel(input_path, sheet_name=sheet_name)
        except ValueError as e:
            if "Worksheet" in str(e):
                # Liệt kê các sheet có sẵn
                xl_file = pd.ExcelFile(input_path)
                available_sheets = xl_file.sheet_names
                raise ValueError(
                    f"Không tìm thấy sheet '{sheet_name}' trong file.\n"
                    f"Các sheet có sẵn: {available_sheets}"
                )
            raise
        
        print(f"📊 Tổng số dòng trong sheet: {len(df)}")
        
        # Giới hạn dòng theo tham số
        original_len = len(df)
        if start_row is not None:
            df = df.iloc[start_row:]
        if end_row is not None:
            if start_row is not None:
                df = df.iloc[:end_row-start_row]
            else:
                df = df.iloc[:end_row]
        
        print(f"▶️ Đánh giá {len(df)} dòng từ sheet '{sheet_name}' (từ dòng {start_row or 0} đến {end_row or original_len})")

        # Kiểm tra cột bắt buộc
        required_cols = {"question_id", "question", "answer", "ai_answer", "supporting_facts"}
        missing_cols = required_cols - set(df.columns)
        if missing_cols:
            available_cols = list(df.columns)
            raise ValueError(
                f"❌ Thiếu cột bắt buộc trong sheet '{sheet_name}': {missing_cols}\n"
                f"Các cột có sẵn: {available_cols}\n"
                f"Cần có đủ các cột: {required_cols}"
            )

        # Rename cột để phù hợp với GenerationEvaluator
        df = df.rename(columns={
            "answer": "reference_answer",
            "ai_answer": "generated_answer"
        })
        
        print("✅ Đã mapping cột: answer -> reference_answer, ai_answer -> generated_answer")

        # Tạo map doc_id -> Document từ supporting_facts
        print("🔄 Xây dựng document mapping từ supporting_facts...")
        doc_map: Dict[str, Document] = {}
        
        for idx, row in df.iterrows():
            try:
                # Parse supporting_facts: "[['doc1', 'content1'], ['doc2', 'content2']]"
                facts = ast.literal_eval(row["supporting_facts"])
                for item in facts:
                    if len(item) >= 2:
                        doc_id, content = item[0], item[1]
                        if doc_id not in doc_map:
                            doc_map[doc_id] = Document(
                                page_content=str(content),
                                metadata={"source": f"supporting_facts_row_{idx}"}
                            )
            except Exception as e:
                print(f"⚠️ Lỗi parse supporting_facts tại dòng {idx}: {e}")
                continue
        
        print(f"📚 Đã tạo {len(doc_map)} documents từ supporting_facts")

        # Parse supporting_facts thành danh sách doc_id
        def parse_supporting_facts(sf_str: str) -> List[str]:
            try:
                facts = ast.literal_eval(sf_str)
                return [item[0] for item in facts if len(item) >= 1]
            except:
                return []
        
        df["relevant_docs"] = df["supporting_facts"].apply(parse_supporting_facts)

        # Chuẩn bị dữ liệu cho batch processing
        print("🚀 Chuẩn bị batch processing...")
        
        # Chuyển đổi DataFrame thành list các dict
        all_data = []
        for global_idx, (_, row) in enumerate(df.iterrows()):
            row_data = {
                "question_id": row["question_id"],
                "question": row["question"],
                "reference_answer": row["reference_answer"],
                "generated_answer": row["generated_answer"],
                "supporting_facts": row["supporting_facts"],
                "relevant_docs": row["relevant_docs"]
            }
            all_data.append((global_idx, row_data))
        
        # Chia thành các batch
        batches = []
        for i in range(0, len(all_data), self.batch_size):
            batch = all_data[i:i + self.batch_size]
            batches.append(batch)
        
        total_batches = len(batches)
        print(f"📦 Chia thành {total_batches} batch (mỗi batch {self.batch_size} dòng)")
        print(f"⚡ Sử dụng {self.max_workers} worker song song")
        
        # Khởi tạo progress tracker
        progress_tracker = BatchProgressTracker(total_batches, len(all_data))
        
        # Xử lý batch song song
        all_results = []
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit tất cả batch
            future_to_batch = {
                executor.submit(
                    self._process_batch, 
                    batch_data, 
                    doc_map, 
                    batch_id,
                    progress_tracker
                ): batch_id 
                for batch_id, batch_data in enumerate(batches)
            }
            
            # Thu thập kết quả theo thứ tự hoàn thành
            batch_results = {}
            for future in as_completed(future_to_batch):
                batch_id = future_to_batch[future]
                try:
                    results = future.result()
                    batch_results[batch_id] = results
                except Exception as e:
                    print(f"❌ Lỗi xử lý batch {batch_id + 1}: {e}")
                    batch_results[batch_id] = []
        
        # Sắp xếp kết quả theo thứ tự batch gốc
        for batch_id in sorted(batch_results.keys()):
            all_results.extend(batch_results[batch_id])
        
        # Sắp xếp lại theo global_index để đảm bảo thứ tự
        all_results.sort(key=lambda x: x.get("_global_index", 0))
        
        # Xóa metadata columns
        for result in all_results:
            result.pop("_batch_index", None)
            result.pop("_global_index", None)
        
        total_time = time.time() - start_time
        avg_time_per_row = total_time / len(all_data) if all_data else 0
        
        print(f"\n⏱️ Hoàn thành trong {total_time:.1f}s ({avg_time_per_row:.2f}s/dòng)")

        # Tạo DataFrame kết quả và xuất Excel
        print("💾 Lưu kết quả...")
        df_output = pd.DataFrame(all_results)
        
        # Tạo thư mục output nếu chưa tồn tại
        output_path.parent.mkdir(exist_ok=True, parents=True)
        
        # Ghi file Excel
        with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
            df_output.to_excel(writer, sheet_name="generation_evaluated", index=False)
        
        print(f"✅ Kết quả đã được lưu vào: {output_path}")
        print(f"📊 Tổng số dòng đã đánh giá: {len(all_results)}")
        
        # In thống kê tóm tắt
        if all_results:
            avg_llm_score = sum(r.get("gen_overall_score", 0) for r in all_results) / len(all_results)
            avg_bleu1 = sum(r.get("gen_bleu_1", 0) for r in all_results) / len(all_results)
            avg_rouge_l = sum(r.get("gen_rouge_l", 0) for r in all_results) / len(all_results)
            
            print("\n📈 THỐNG KÊ TỔNG KẾT:")
            print(f"  • LLM Score trung bình: {avg_llm_score:.2f}")
            print(f"  • BLEU-1 trung bình: {avg_bleu1:.3f}")
            print(f"  • Rouge-L trung bình: {avg_rouge_l:.3f}")
            print(f"  • Thời gian xử lý: {total_time:.1f}s")
            print(f"  • Tốc độ: {avg_time_per_row:.2f}s/dòng")

def main():
    """Hàm main với argument parsing."""
    # Xác định đường dẫn mặc định
    script_dir = Path(__file__).parent
    default_input = script_dir.parent / "input" / "main_vimqa_dev_300lines.xlsx"
    default_output = script_dir / "outputs" / "main_vimqa_dev_300lines_generation_evaluated.xlsx"
    
    parser = argparse.ArgumentParser(
        description="Đánh giá generation từ Excel với LLM và các metrics tự động (có batch processing)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ví dụ sử dụng:
  python evaluator_generation_for_xlsx.py --start_row 0 --end_row 5
  python evaluator_generation_for_xlsx.py -i data.xlsx -o result.xlsx -s my_sheet
  python evaluator_generation_for_xlsx.py --model gpt-4 --temperature 0.1
  python evaluator_generation_for_xlsx.py --batch_size 20 --max_workers 5
        """
    )
    
    parser.add_argument(
        "--input", "-i", 
        default=str(default_input),
        help=f"Đường dẫn file Excel đầu vào (mặc định: {default_input})"
    )
    parser.add_argument(
        "--output", "-o", 
        default=str(default_output),
        help=f"Đường dẫn file Excel đầu ra (mặc định: {default_output})"
    )
    parser.add_argument(
        "--sheet", "-s", 
        default="baseline_result_QA_raw",
        help="Tên sheet chứa dữ liệu generation (mặc định: baseline_result_QA_raw)"
    )
    parser.add_argument(
        "--start_row", 
        type=int,
        help="Dòng bắt đầu đánh giá (tính từ 0, mặc định: đánh giá từ đầu)"
    )
    parser.add_argument(
        "--end_row", 
        type=int,
        help="Dòng kết thúc đánh giá (không bao gồm, mặc định: đánh giá đến cuối)"
    )
    parser.add_argument(
        "--model", "-m", 
        default="gpt-4o-mini",
        help="Tên model LLM đánh giá (mặc định: gpt-4o-mini)"
    )
    parser.add_argument(
        "--temperature", "-t", 
        type=float, 
        default=0.0,
        help="Temperature cho LLM (mặc định: 0.0)"
    )
    parser.add_argument(
        "--batch_size", "-b",
        type=int,
        default=10,
        help="Kích thước mỗi batch (mặc định: 10)"
    )
    parser.add_argument(
        "--max_workers", "-w",
        type=int,
        default=3,
        help="Số worker song song tối đa (mặc định: 3)"
    )
    
    args = parser.parse_args()
    
    print("🚀 GENERATION EVALUATOR WITH BATCH PROCESSING")
    print("=" * 60)
    print(f"📁 Input: {args.input}")
    print(f"📁 Output: {args.output}")
    print(f"📄 Sheet: {args.sheet}")
    print(f"🤖 Model: {args.model}")
    print(f"🌡️ Temperature: {args.temperature}")
    print(f"📦 Batch size: {args.batch_size}")
    print(f"⚡ Max workers: {args.max_workers}")
    if args.start_row is not None or args.end_row is not None:
        print(f"📍 Phạm vi: dòng {args.start_row or 0} đến {args.end_row or 'cuối'}")
    print("=" * 60)

    try:
        evaluator = ExcelGenerationEvaluator(
            model_name=args.model,
            temperature=args.temperature,
            batch_size=args.batch_size,
            max_workers=args.max_workers
        )
        
        evaluator.evaluate_excel(
            input_path=Path(args.input),
            output_path=Path(args.output),
            sheet_name=args.sheet,
            start_row=args.start_row,
            end_row=args.end_row
        )
        
        print("\n🎉 Đánh giá hoàn thành thành công!")
        
    except Exception as e:
        print(f"\n❌ Lỗi trong quá trình đánh giá: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
