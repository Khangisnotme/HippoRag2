#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demo script để chạy phân tích VIMQA dataset
Sử dụng file vimqa_dev_300_vi.json
"""

from vimqa_analyzer import VIMQAAnalyzer
import os

def main():
    print("🚀 DEMO VIMQA ANALYZER")
    print("=" * 40)
    
    # Đường dẫn file input
    input_file = "vimqa_dev_300_vi.json"  # Thay đổi đường dẫn này nếu cần
    output_dir = "./analysis_output/"
    
    # Kiểm tra file tồn tại
    if not os.path.exists(input_file):
        print(f"❌ Không tìm thấy file: {input_file}")
        print("💡 Hãy đảm bảo file vimqa_dev_300_vi.json ở cùng thư mục với script này")
        print("💡 Hoặc thay đổi đường dẫn trong biến 'input_file'")
        return
    
    # Tạo thư mục output
    os.makedirs(output_dir, exist_ok=True)
    
    # Khởi tạo analyzer
    print(f"📁 Đọc file: {input_file}")
    analyzer = VIMQAAnalyzer(input_file)
    
    # Chạy phân tích đầy đủ
    success = analyzer.run_full_analysis(output_dir)
    
    if success:
        print("\n🎉 DEMO HOÀN THÀNH!")
        print(f"📂 Kết quả được lưu trong thư mục: {output_dir}")
        print("\n📋 Các file được tạo:")
        print(f"  📊 {output_dir}vimqa_analysis_charts.png")
        print(f"  📄 {output_dir}vimqa_analysis_report.md")
        print(f"  💾 {output_dir}vimqa_analysis_results.json")
        
        print("\n💡 Mở file report.md để xem báo cáo chi tiết!")
    else:
        print("\n❌ Demo thất bại!")

if __name__ == "__main__":
    main()

