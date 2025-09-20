#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VIMQA Dataset Analysis Tool
Tạo báo cáo phân tích chi tiết từ file vimqa_dev_300_vi.json

Author: Doan Ngoc Cuong
Date: 2025-06-06
"""

import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter, defaultdict
import re
import numpy as np
import os
from datetime import datetime

class VIMQAAnalyzer:
    def __init__(self, data_file):
        """
        Khởi tạo analyzer với file dữ liệu VIMQA
        
        Args:
            data_file (str): Đường dẫn đến file JSON chứa dữ liệu VIMQA
        """
        self.data_file = data_file
        self.data = None
        self.subset_300 = None
        self.analysis_results = {}
        
    def load_data(self):
        """Đọc dữ liệu từ file JSON"""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
            
            # Lấy 300 câu đầu tiên
            self.subset_300 = self.data[:300]
            print(f"✅ Đã đọc {len(self.data)} câu hỏi, phân tích 300 câu đầu tiên")
            return True
        except Exception as e:
            print(f"❌ Lỗi đọc file: {e}")
            return False
    
    def classify_question_type(self, question):
        """Phân loại loại câu hỏi"""
        question_lower = question.lower()
        
        if question.endswith('?') and any(word in question_lower for word in ['phải không', 'có phải', 'đúng không', 'sai không']):
            return 'Yes/No'
        elif question_lower.startswith('ai '):
            return 'Who'
        elif question_lower.startswith('gì ') or 'gì?' in question_lower or question_lower.startswith('cái gì'):
            return 'What'
        elif question_lower.startswith('đâu ') or 'ở đâu' in question_lower:
            return 'Where'
        elif question_lower.startswith('khi nào') or 'năm nào' in question_lower or 'ngày nào' in question_lower:
            return 'When'
        elif question_lower.startswith('tại sao') or question_lower.startswith('vì sao'):
            return 'Why'
        elif question_lower.startswith('như thế nào') or question_lower.startswith('bằng cách nào'):
            return 'How'
        elif question_lower.startswith('bao nhiêu'):
            return 'How many/much'
        else:
            return 'Other'
    
    def classify_domain(self, title):
        """Phân loại domain dựa trên title"""
        title_lower = title.lower()
        
        if any(word in title_lower for word in ['f.c.', 'football', 'bóng đá', 'uefa', 'champions league', 'premier league', 'world cup']):
            return 'Thể thao'
        elif any(word in title_lower for word in ['tổng thống', 'chủ tịch', 'thủ tướng', 'hoàng đế', 'vua', 'nhà ', 'cách mạng', 'chiến tranh']):
            return 'Chính trị/Lịch sử'
        elif any(word in title_lower for word in ['nhiệt kế', 'mạch', 'điện', 'hóa học', 'vật lý', 'sinh học', 'toán học']):
            return 'Khoa học/Công nghệ'
        elif any(word in title_lower for word in ['phim', 'diễn viên', 'ca sĩ', 'nhạc', 'album', 'nghệ sĩ', 'cô gái lắm chiêu']):
            return 'Giải trí/Nghệ thuật'
        elif any(word in title_lower for word in ['hải cẩu', 'động vật', 'thực vật', 'sông', 'núi', 'biển']):
            return 'Địa lý/Tự nhiên'
        elif any(word in title_lower for word in ['giải nobel', 'giải thưởng', 'danh hiệu']):
            return 'Giải thưởng'
        elif len(title.split()) <= 3 and not any(char.islower() for char in title):
            return 'Nhân vật'
        else:
            return 'Khác'
    
    def classify_answer_type(self, answer):
        """Phân loại loại câu trả lời"""
        answer_lower = answer.lower().strip()
        
        if answer_lower in ['đúng', 'sai', 'có', 'không', 'yes', 'no']:
            return 'Yes/No'
        elif re.match(r'^\d+$', answer_lower):
            return 'Number'
        elif re.match(r'^\d{4}$', answer_lower):
            return 'Year'
        elif any(word in answer_lower for word in ['tháng', 'ngày', 'năm']):
            return 'Date/Time'
        elif len(answer.split()) == 1:
            return 'Single Word'
        elif len(answer.split()) <= 3:
            return 'Short Phrase'
        else:
            return 'Long Answer'
    
    def analyze_multihop_type(self, item):
        """Phân tích loại multi-hop reasoning"""
        num_facts = len(item['supporting_facts'])
        
        if num_facts == 1:
            return 'Single-hop'
        elif num_facts == 2:
            facts = item['supporting_facts']
            if len(set([fact[0] for fact in facts])) == 2:
                return 'Bridge entity (2-hop)'
            else:
                return 'Multiple properties (2-hop)'
        else:
            return 'Complex (3+ hop)'
    
    def get_question_domain(self, item):
        """Lấy domain chính của câu hỏi dựa trên supporting facts"""
        domains_in_question = []
        for fact in item['supporting_facts']:
            title = fact[0]
            domain = self.classify_domain(title)
            domains_in_question.append(domain)
        
        if domains_in_question:
            return Counter(domains_in_question).most_common(1)[0][0]
        return 'Khác'
    
    def basic_statistics(self):
        """Phân tích thống kê cơ bản"""
        print("\n=== PHÂN TÍCH THỐNG KÊ CƠ BẢN ===")
        
        # Độ dài câu hỏi
        question_lengths = [len(item['question'].split()) for item in self.subset_300]
        
        # Độ dài câu trả lời
        answer_lengths = [len(item['answer'].split()) for item in self.subset_300]
        
        # Số supporting facts
        supporting_facts_counts = [len(item['supporting_facts']) for item in self.subset_300]
        
        # Số context
        context_counts = [len(item['context']) for item in self.subset_300]
        
        stats = {
            'total_questions': len(self.subset_300),
            'avg_question_length': np.mean(question_lengths),
            'min_question_length': min(question_lengths),
            'max_question_length': max(question_lengths),
            'std_question_length': np.std(question_lengths),
            'avg_answer_length': np.mean(answer_lengths),
            'min_answer_length': min(answer_lengths),
            'max_answer_length': max(answer_lengths),
            'std_answer_length': np.std(answer_lengths),
            'avg_supporting_facts': np.mean(supporting_facts_counts),
            'min_supporting_facts': min(supporting_facts_counts),
            'max_supporting_facts': max(supporting_facts_counts),
            'avg_context_count': np.mean(context_counts),
            'supporting_facts_distribution': dict(Counter(supporting_facts_counts))
        }
        
        self.analysis_results['basic_stats'] = stats
        
        print(f"Tổng số câu hỏi: {stats['total_questions']}")
        print(f"Độ dài câu hỏi: TB={stats['avg_question_length']:.1f}, Min={stats['min_question_length']}, Max={stats['max_question_length']}")
        print(f"Độ dài câu trả lời: TB={stats['avg_answer_length']:.1f}, Min={stats['min_answer_length']}, Max={stats['max_answer_length']}")
        print(f"Số supporting facts: TB={stats['avg_supporting_facts']:.1f}, Min={stats['min_supporting_facts']}, Max={stats['max_supporting_facts']}")
        
        return stats
    
    def analyze_question_types(self):
        """Phân tích loại câu hỏi"""
        print("\n=== PHÂN TÍCH LOẠI CÂU HỎI ===")
        
        question_types = [self.classify_question_type(item['question']) for item in self.subset_300]
        qt_dist = Counter(question_types)
        
        self.analysis_results['question_types'] = dict(qt_dist)
        
        print("Phân bố loại câu hỏi:")
        for qtype, count in qt_dist.most_common():
            print(f"  {qtype}: {count} câu ({count/len(self.subset_300)*100:.1f}%)")
        
        return qt_dist
    
    def analyze_answer_types(self):
        """Phân tích loại câu trả lời"""
        print("\n=== PHÂN TÍCH LOẠI CÂU TRẢ LỜI ===")
        
        answer_types = [self.classify_answer_type(item['answer']) for item in self.subset_300]
        at_dist = Counter(answer_types)
        
        self.analysis_results['answer_types'] = dict(at_dist)
        
        print("Phân bố loại câu trả lời:")
        for atype, count in at_dist.most_common():
            print(f"  {atype}: {count} câu ({count/len(self.subset_300)*100:.1f}%)")
        
        return at_dist
    
    def analyze_domains(self):
        """Phân tích domain"""
        print("\n=== PHÂN TÍCH DOMAIN ===")
        
        # Phân tích tất cả titles
        all_titles = []
        for item in self.subset_300:
            for context_item in item['context']:
                title = context_item[0]
                all_titles.append(title)
        
        unique_titles = len(set(all_titles))
        title_counts = Counter(all_titles)
        
        # Phân tích domain cho từng câu hỏi
        question_domains = [self.get_question_domain(item) for item in self.subset_300]
        domain_dist = Counter(question_domains)
        
        # Phân tích domain cho tất cả titles
        domains = [self.classify_domain(title) for title in all_titles]
        title_domain_dist = Counter(domains)
        
        self.analysis_results['domains'] = {
            'unique_titles': unique_titles,
            'top_titles': dict(title_counts.most_common(20)),
            'question_domain_distribution': dict(domain_dist),
            'title_domain_distribution': dict(title_domain_dist)
        }
        
        print(f"Số title unique: {unique_titles}")
        print("\nTop 10 title phổ biến:")
        for title, count in title_counts.most_common(10):
            print(f"  {title}: {count} lần")
        
        print("\nPhân bố domain (theo câu hỏi):")
        for domain, count in domain_dist.most_common():
            print(f"  {domain}: {count} câu ({count/len(self.subset_300)*100:.1f}%)")
        
        return domain_dist, title_counts
    
    def analyze_multihop_reasoning(self):
        """Phân tích multi-hop reasoning"""
        print("\n=== PHÂN TÍCH MULTI-HOP REASONING ===")
        
        multihop_types = [self.analyze_multihop_type(item) for item in self.subset_300]
        mh_dist = Counter(multihop_types)
        
        # Phân tích type field
        if 'type' in self.subset_300[0]:
            types = [item['type'] for item in self.subset_300]
            type_dist = Counter(types)
            self.analysis_results['types'] = dict(type_dist)
        
        self.analysis_results['multihop_reasoning'] = dict(mh_dist)
        
        print("Phân bố loại multi-hop reasoning:")
        for mtype, count in mh_dist.most_common():
            print(f"  {mtype}: {count} câu ({count/len(self.subset_300)*100:.1f}%)")
        
        if 'type' in self.subset_300[0]:
            print("\nPhân bố type field:")
            for typ, count in type_dist.most_common():
                print(f"  {typ}: {count} câu ({count/len(self.subset_300)*100:.1f}%)")
        
        return mh_dist
    
    def create_visualizations(self, output_dir="./"):
        """Tạo các biểu đồ visualization"""
        print("\n=== TẠO BIỂU ĐỒ VISUALIZATION ===")
        
        # Set font cho tiếng Việt
        plt.rcParams['font.family'] = ['DejaVu Sans']
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # 1. Phân bố loại câu hỏi
        qt_dist = Counter([self.classify_question_type(item['question']) for item in self.subset_300])
        axes[0,0].pie(qt_dist.values(), labels=qt_dist.keys(), autopct='%1.1f%%')
        axes[0,0].set_title('Phan bo loai cau hoi')
        
        # 2. Phân bố domain
        domain_dist = Counter([self.get_question_domain(item) for item in self.subset_300])
        axes[0,1].pie(domain_dist.values(), labels=domain_dist.keys(), autopct='%1.1f%%')
        axes[0,1].set_title('Phan bo domain')
        
        # 3. Phân bố số supporting facts
        sf_counts = [len(item['supporting_facts']) for item in self.subset_300]
        sf_dist = Counter(sf_counts)
        axes[1,0].bar(sf_dist.keys(), sf_dist.values())
        axes[1,0].set_title('Phan bo so supporting facts')
        axes[1,0].set_xlabel('So supporting facts')
        axes[1,0].set_ylabel('So cau hoi')
        
        # 4. Phân bố độ dài câu hỏi
        question_lengths = [len(item['question'].split()) for item in self.subset_300]
        axes[1,1].hist(question_lengths, bins=20, alpha=0.7)
        axes[1,1].set_title('Phan bo do dai cau hoi')
        axes[1,1].set_xlabel('So tu')
        axes[1,1].set_ylabel('So cau hoi')
        
        plt.tight_layout()
        
        chart_path = os.path.join(output_dir, 'vimqa_analysis_charts.png')
        plt.savefig(chart_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✅ Đã lưu biểu đồ tại: {chart_path}")
        return chart_path
    
    def analyze_rag_kg_suitability(self):
        """Phân tích sự phù hợp với RAG-KG"""
        print("\n=== PHÂN TÍCH SỰ PHÙ HỢP VỚI RAG-KG ===")
        
        # Tính toán các chỉ số phù hợp
        bridge_entity_ratio = len([item for item in self.subset_300 if self.analyze_multihop_type(item) == 'Bridge entity (2-hop)']) / len(self.subset_300)
        multihop_ratio = len([item for item in self.subset_300 if len(item['supporting_facts']) >= 2]) / len(self.subset_300)
        domain_diversity = len(set([self.get_question_domain(item) for item in self.subset_300]))
        
        suitability_score = (
            bridge_entity_ratio * 4 +  # Bridge entity reasoning (trọng số cao)
            multihop_ratio * 3 +       # Multi-hop reasoning
            min(domain_diversity / 5, 1) * 2 +  # Domain diversity
            1  # Base score
        ) / 10 * 10  # Chuẩn hóa về thang 10
        
        suitability_analysis = {
            'bridge_entity_ratio': bridge_entity_ratio,
            'multihop_ratio': multihop_ratio,
            'domain_diversity': domain_diversity,
            'suitability_score': suitability_score,
            'assessment': 'Rất phù hợp' if suitability_score >= 8 else 'Phù hợp' if suitability_score >= 6 else 'Trung bình'
        }
        
        self.analysis_results['rag_kg_suitability'] = suitability_analysis
        
        print(f"Tỷ lệ bridge entity reasoning: {bridge_entity_ratio:.1%}")
        print(f"Tỷ lệ multi-hop reasoning: {multihop_ratio:.1%}")
        print(f"Số domain khác nhau: {domain_diversity}")
        print(f"Điểm phù hợp với RAG-KG: {suitability_score:.1f}/10 ({suitability_analysis['assessment']})")
        
        return suitability_analysis
    
    def generate_examples(self, num_examples=5):
        """Tạo các ví dụ minh họa"""
        print(f"\n=== {num_examples} VÍ DỤ MINH HỌA ===")
        
        examples = []
        for i in range(min(num_examples, len(self.subset_300))):
            item = self.subset_300[i]
            example = {
                'id': item['_id'],
                'question': item['question'],
                'answer': item['answer'],
                'supporting_facts': item['supporting_facts'],
                'type': item.get('type', 'N/A'),
                'question_type': self.classify_question_type(item['question']),
                'multihop_type': self.analyze_multihop_type(item),
                'domain': self.get_question_domain(item)
            }
            examples.append(example)
            
            print(f"\nVí dụ {i+1}:")
            print(f"  Question: {example['question']}")
            print(f"  Answer: {example['answer']}")
            print(f"  Supporting facts: {example['supporting_facts']}")
            print(f"  Type: {example['type']}")
            print(f"  Question type: {example['question_type']}")
            print(f"  Multi-hop type: {example['multihop_type']}")
            print(f"  Domain: {example['domain']}")
        
        self.analysis_results['examples'] = examples
        return examples
    
    def save_results(self, output_dir="./"):
        """Lưu kết quả phân tích"""
        # Lưu JSON
        json_path = os.path.join(output_dir, 'vimqa_analysis_results.json')
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(self.analysis_results, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Đã lưu kết quả JSON tại: {json_path}")
        return json_path
    
    def generate_markdown_report(self, output_dir="./"):
        """Tạo báo cáo Markdown chi tiết"""
        print("\n=== TẠO BÁO CÁO MARKDOWN ===")
        
        report_path = os.path.join(output_dir, 'vimqa_analysis_report.md')
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(f"# Báo cáo phân tích Dataset VIMQA - 300 câu đầu tiên\n\n")
            f.write(f"**Ngày tạo:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**File dữ liệu:** {os.path.basename(self.data_file)}\n\n")
            
            # Tóm tắt
            f.write("## Tóm tắt\n\n")
            stats = self.analysis_results['basic_stats']
            f.write(f"- **Tổng số câu hỏi phân tích:** {stats['total_questions']}\n")
            f.write(f"- **Độ dài câu hỏi trung bình:** {stats['avg_question_length']:.1f} từ\n")
            f.write(f"- **Độ dài câu trả lời trung bình:** {stats['avg_answer_length']:.1f} từ\n")
            f.write(f"- **Số supporting facts trung bình:** {stats['avg_supporting_facts']:.1f}\n")
            f.write(f"- **Số title unique:** {self.analysis_results['domains']['unique_titles']}\n\n")
            
            # Phân bố loại câu hỏi
            f.write("## Phân bố loại câu hỏi\n\n")
            f.write("| Loại câu hỏi | Số lượng | Tỷ lệ |\n")
            f.write("|--------------|----------|-------|\n")
            for qtype, count in sorted(self.analysis_results['question_types'].items(), key=lambda x: x[1], reverse=True):
                f.write(f"| {qtype} | {count} | {count/stats['total_questions']*100:.1f}% |\n")
            f.write("\n")
            
            # Phân bố domain
            f.write("## Phân bố domain\n\n")
            f.write("| Domain | Số lượng | Tỷ lệ |\n")
            f.write("|--------|----------|-------|\n")
            for domain, count in sorted(self.analysis_results['domains']['question_domain_distribution'].items(), key=lambda x: x[1], reverse=True):
                f.write(f"| {domain} | {count} | {count/stats['total_questions']*100:.1f}% |\n")
            f.write("\n")
            
            # Multi-hop reasoning
            f.write("## Phân bố Multi-hop Reasoning\n\n")
            f.write("| Loại reasoning | Số lượng | Tỷ lệ |\n")
            f.write("|----------------|----------|-------|\n")
            for mtype, count in sorted(self.analysis_results['multihop_reasoning'].items(), key=lambda x: x[1], reverse=True):
                f.write(f"| {mtype} | {count} | {count/stats['total_questions']*100:.1f}% |\n")
            f.write("\n")
            
            # Sự phù hợp với RAG-KG
            f.write("## Sự phù hợp với RAG-KG\n\n")
            suitability = self.analysis_results['rag_kg_suitability']
            f.write(f"- **Điểm phù hợp:** {suitability['suitability_score']:.1f}/10\n")
            f.write(f"- **Đánh giá:** {suitability['assessment']}\n")
            f.write(f"- **Tỷ lệ bridge entity reasoning:** {suitability['bridge_entity_ratio']:.1%}\n")
            f.write(f"- **Tỷ lệ multi-hop reasoning:** {suitability['multihop_ratio']:.1%}\n")
            f.write(f"- **Số domain khác nhau:** {suitability['domain_diversity']}\n\n")
            
            # Top titles
            f.write("## Top 10 titles phổ biến\n\n")
            f.write("| Title | Số lần xuất hiện |\n")
            f.write("|-------|------------------|\n")
            for title, count in list(self.analysis_results['domains']['top_titles'].items())[:10]:
                f.write(f"| {title} | {count} |\n")
            f.write("\n")
            
            # Ví dụ
            f.write("## Ví dụ minh họa\n\n")
            for i, example in enumerate(self.analysis_results['examples'][:3]):
                f.write(f"### Ví dụ {i+1}\n")
                f.write(f"- **Câu hỏi:** {example['question']}\n")
                f.write(f"- **Câu trả lời:** {example['answer']}\n")
                f.write(f"- **Supporting facts:** {example['supporting_facts']}\n")
                f.write(f"- **Loại câu hỏi:** {example['question_type']}\n")
                f.write(f"- **Loại reasoning:** {example['multihop_type']}\n")
                f.write(f"- **Domain:** {example['domain']}\n\n")
        
        print(f"✅ Đã tạo báo cáo Markdown tại: {report_path}")
        return report_path
    
    def run_full_analysis(self, output_dir="./"):
        """Chạy phân tích đầy đủ"""
        print("🚀 BẮT ĐẦU PHÂN TÍCH DATASET VIMQA")
        print("=" * 50)
        
        if not self.load_data():
            return False
        
        # Chạy các phân tích
        self.basic_statistics()
        self.analyze_question_types()
        self.analyze_answer_types()
        self.analyze_domains()
        self.analyze_multihop_reasoning()
        self.analyze_rag_kg_suitability()
        self.generate_examples()
        
        # Tạo outputs
        chart_path = self.create_visualizations(output_dir)
        json_path = self.save_results(output_dir)
        report_path = self.generate_markdown_report(output_dir)
        
        print("\n" + "=" * 50)
        print("✅ HOÀN THÀNH PHÂN TÍCH!")
        print(f"📊 Biểu đồ: {chart_path}")
        print(f"📄 Báo cáo: {report_path}")
        print(f"💾 Dữ liệu: {json_path}")
        
        return True

def main():
    """Hàm main để chạy phân tích"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Phân tích dataset VIMQA')
    parser.add_argument('input_file', help='Đường dẫn đến file vimqa_dev_300_vi.json')
    parser.add_argument('--output_dir', '-o', default='./', help='Thư mục output (mặc định: ./)')
    
    args = parser.parse_args()
    
    # Tạo thư mục output nếu chưa có
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Chạy phân tích
    analyzer = VIMQAAnalyzer(args.input_file)
    success = analyzer.run_full_analysis(args.output_dir)
    
    if success:
        print("\n🎉 Phân tích hoàn thành thành công!")
    else:
        print("\n❌ Có lỗi xảy ra trong quá trình phân tích!")

if __name__ == "__main__":
    main()

