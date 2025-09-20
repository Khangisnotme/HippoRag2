(.venv) PS D:\GIT\ResearchProject_Memory-AugmentedAIAgents_GraduationProject\src\system\baselineRAG\layers\_05_generation> python .\model\test_model.py
🤖 Vietnamese Model Tester
Choose an option:
1. Test all Vietnamese models
2. Quick test single model
3. Test with RAG format
4. Exit

Enter your choice (1-4): 1
🚀 Starting Vietnamese Model Test Suite
Testing 7 models...

============================================================      
Testing model: AITeamVN/Vi-Qwen2-1.5B-RAG
============================================================      
🔄 Testing text generation...
❌ Text generation failed: 
🔄 Testing chat completion...
❌ Chat completion failed:
❌ AITeamVN/Vi-Qwen2-1.5B-RAG - FAILED

============================================================      
Testing model: AITeamVN/Vi-Qwen2-3B-RAG
============================================================      
🔄 Testing text generation...
❌ Text generation failed: 
🔄 Testing chat completion...
❌ Chat completion failed:
❌ AITeamVN/Vi-Qwen2-3B-RAG - FAILED

============================================================      
Testing model: AITeamVN/GRPO-VI-Qwen2-3B-RAG
============================================================      
🔄 Testing text generation...
❌ Text generation failed: 
🔄 Testing chat completion...
❌ Chat completion failed:
❌ AITeamVN/GRPO-VI-Qwen2-3B-RAG - FAILED

============================================================      
Testing model: Qwen/Qwen2.5-1.5B-Instruct
============================================================      
🔄 Testing text generation...
❌ Text generation failed: Model Qwen/Qwen2.5-1.5B-Instruct is not supported for task text-generation and provider nebius. Supported task: conversational.
🔄 Testing chat completion...
✅ Chat completion works:
Response: Xin chào! Tôi là một trợ lý AI và tôi không thể cảm nhận được sức khỏe thực sự. Tuy nhiên, tôi luôn sẵn sàng giúp đỡ bạn với bất kỳ câu hỏi hoặc vấn đề nào bạn có.
✅ Qwen/Qwen2.5-1.5B-Instruct - WORKING

============================================================      
Testing model: Qwen/Qwen2.5-3B-Instruct
============================================================      
🔄 Testing text generation...
❌ Text generation failed: 
🔄 Testing chat completion...
❌ Chat completion failed:
❌ Qwen/Qwen2.5-3B-Instruct - FAILED

============================================================      
Testing model: microsoft/DialoGPT-small
============================================================      
🔄 Testing text generation...
❌ Text generation failed: 
🔄 Testing chat completion...
❌ Chat completion failed:
❌ microsoft/DialoGPT-small - FAILED

============================================================      
Testing model: gpt2
============================================================      
🔄 Testing text generation...
❌ Text generation failed: 
🔄 Testing chat completion...
❌ Chat completion failed:
❌ gpt2 - FAILED

============================================================      
📊 TEST SUMMARY
============================================================      
✅ Working models (1):
   - Qwen/Qwen2.5-1.5B-Instruct

❌ Failed models (6):
   - AITeamVN/Vi-Qwen2-1.5B-RAG
   - AITeamVN/Vi-Qwen2-3B-RAG
   - AITeamVN/GRPO-VI-Qwen2-3B-RAG
   - Qwen/Qwen2.5-3B-Instruct
   - microsoft/DialoGPT-small
   - gpt2

🎉 Recommended model to use: Qwen/Qwen2.5-1.5B-Instruct
(.venv) PS D:\GIT\ResearchProject_Memory-AugmentedAIAgents_GraduationProject\src\system\baselineRAG\layers\_05_generation>