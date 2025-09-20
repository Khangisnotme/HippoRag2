"""
Simple test script to check if InferenceClient works with small Vietnamese models
"""

from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os
import time

load_dotenv()

def test_model(model_name, test_prompt="Xin chào, bạn có khỏe không?"):
    """Test a single model"""
    print(f"\n{'='*60}")
    print(f"Testing model: {model_name}")
    print(f"{'='*60}")
    
    hf_token = os.getenv("HF_TOKEN") or os.getenv("HUGGINGFACE_TOKEN") or os.getenv("HUGGINGFACE_API_KEY")
    if not hf_token:
        print("❌ No HF_TOKEN found in environment variables")
        return False
    
    try:
        client = InferenceClient(token=hf_token)
        
        # Test 1: Basic text generation
        print("🔄 Testing text generation...")
        response = client.text_generation(
            prompt=test_prompt,
            model=model_name,
            max_new_tokens=100,
            temperature=0.1
        )
        print(f"✅ Text generation works:")
        print(f"Response: {response}")
        
        return True
        
    except Exception as e:
        print(f"❌ Text generation failed: {e}")
        
        # Test 2: Try chat completion if text generation fails
        try:
            print("🔄 Testing chat completion...")
            messages = [{"role": "user", "content": test_prompt}]
            response = client.chat_completion(
                messages=messages,
                model=model_name,
                max_tokens=100,
                temperature=0.1
            )
            print(f"✅ Chat completion works:")
            print(f"Response: {response.choices[0].message.content}")
            return True
            
        except Exception as e2:
            print(f"❌ Chat completion failed: {e2}")
            return False

def test_all_vietnamese_models():
    """Test all Vietnamese models"""
    models_to_test = [
        # Small models first
        "AITeamVN/Vi-Qwen2-1.5B-RAG",
        "AITeamVN/Vi-Qwen2-3B-RAG",
        "AITeamVN/GRPO-VI-Qwen2-3B-RAG",
        
        # Backup models
        "Qwen/Qwen2.5-1.5B-Instruct", 
        "Qwen/Qwen2.5-3B-Instruct",
        
        # Alternative small models
        "microsoft/DialoGPT-small",
        "gpt2",
    ]
    
    working_models = []
    failed_models = []
    
    print("🚀 Starting Vietnamese Model Test Suite")
    print(f"Testing {len(models_to_test)} models...")
    
    for model in models_to_test:
        try:
            success = test_model(model)
            if success:
                working_models.append(model)
                print(f"✅ {model} - WORKING")
            else:
                failed_models.append(model)
                print(f"❌ {model} - FAILED")
        except Exception as e:
            failed_models.append(model)
            print(f"❌ {model} - ERROR: {e}")
        
        # Small delay between tests
        time.sleep(2)
    
    # Summary
    print(f"\n{'='*60}")
    print("📊 TEST SUMMARY")
    print(f"{'='*60}")
    print(f"✅ Working models ({len(working_models)}):")
    for model in working_models:
        print(f"   - {model}")
    
    print(f"\n❌ Failed models ({len(failed_models)}):")
    for model in failed_models:
        print(f"   - {model}")
    
    if working_models:
        print(f"\n🎉 Recommended model to use: {working_models[0]}")
    else:
        print(f"\n😞 No models are working. Check your HF_TOKEN and internet connection.")

def quick_test_single_model():
    """Quick test for a single model"""
    model_name = input("Enter model name to test (or press Enter for default): ").strip()
    if not model_name:
        model_name = "AITeamVN/GRPO-VI-Qwen2-3B-RAG"
    
    test_question = input("Enter test question (or press Enter for default): ").strip()
    if not test_question:
        test_question = "Machine learning là gì?"
    
    print(f"\n🔍 Quick testing: {model_name}")
    test_model(model_name, test_question)

def test_with_rag_format():
    """Test with proper RAG format"""
    model_name = "AITeamVN/GRPO-VI-Qwen2-3B-RAG"
    
    rag_prompt = """Chú ý các yêu cầu sau:
- Câu trả lời phải chính xác và đầy đủ nếu ngữ cảnh có câu trả lời. 
- Chỉ sử dụng các thông tin có trong ngữ cảnh được cung cấp.
- Chỉ cần từ chối trả lời và không suy luận gì thêm nếu ngữ cảnh không có câu trả lời.
Hãy trả lời câu hỏi dựa trên ngữ cảnh:
### Ngữ cảnh :
Machine Learning là một nhánh của trí tuệ nhân tạo cho phép máy tính học từ dữ liệu.

### Câu hỏi :
Machine learning là gì?

### Trả lời :"""
    
    print(f"\n🎯 Testing RAG format with: {model_name}")
    test_model(model_name, rag_prompt)

if __name__ == "__main__":
    print("🤖 Vietnamese Model Tester")
    print("Choose an option:")
    print("1. Test all Vietnamese models")
    print("2. Quick test single model")
    print("3. Test with RAG format")
    print("4. Exit")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == "1":
        test_all_vietnamese_models()
    elif choice == "2":
        quick_test_single_model()
    elif choice == "3":
        test_with_rag_format()
    elif choice == "4":
        print("👋 Goodbye!")
    else:
        print("❌ Invalid choice. Running full test...")
        test_all_vietnamese_models()
