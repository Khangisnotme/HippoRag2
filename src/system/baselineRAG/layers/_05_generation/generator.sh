# # Sử dụng GPT-4o-mini (mặc định)
# python generator.py

# # Sử dụng GPT-4o-mini với câu hỏi cụ thể
# python generator.py --model gpt-4o-mini --question "What is RAG?"

# # Sử dụng Vi-Qwen2-3B-RAG cho tiếng Việt
# python generator.py --model AITeamVN/Vi-Qwen2-3B-RAG --question "RAG là gì?"

# # Sử dụng Vi-Qwen2-1.5B-RAG với tham số tùy chỉnh
# python generator.py --model AITeamVN/Vi-Qwen2-1.5B-RAG --temperature 0.1 --max-tokens 2048

# # Sử dụng GPT-4 với nhiệt độ cao hơn
# python generator.py --model gpt-4 --temperature 0.5 --question "Explain quantum computing"


# Test with working Vietnamese model
python generator.py --model Qwen/Qwen2.5-1.5B-Instruct --question "Machine learning là gì?"

# Test with English
python generator.py --model Qwen/Qwen2.5-1.5B-Instruct --question "What is machine learning?" --language en

# Test with OpenAI (if you have API key)
python generator.py --model gpt-4o-mini --question "What is RAG?"
