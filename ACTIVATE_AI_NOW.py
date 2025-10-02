#!/usr/bin/env python3
"""
IMMEDIATE AI ACTIVATION - Get your 800 euro investment working NOW!
Run GGUF models with llama-cpp-python
"""

import subprocess
import sys
import os
from pathlib import Path

def install_llama_cpp_python():
    """Install llama-cpp-python if not available"""
    try:
        import llama_cpp
        print("✅ llama-cpp-python already installed")
        return True
    except ImportError:
        print("📦 Installing llama-cpp-python...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "llama-cpp-python"])
            print("✅ llama-cpp-python installed successfully")
            return True
        except Exception as e:
            print(f"❌ Failed to install llama-cpp-python: {e}")
            return False

def find_best_model():
    """Find the smallest/fastest model to start with"""
    base_path = Path(".")
    
    models = {
        "Gemma-3-4B": "gemma-3-4b-it-Q4_K_M.gguf",
        "Qwen2-VL-2B": "Qwen2-VL-2B-mmproj-q5_1.gguf", 
        "TinyLlama": "models/tinyllama-1.1b/"
    }
    
    for name, path in models.items():
        full_path = base_path / path
        if full_path.exists():
            print(f"✅ Found {name} at {full_path}")
            return str(full_path), name
    
    print("❌ No GGUF models found!")
    return None, None

def run_ai_model(model_path, model_name):
    """Actually run the AI model - MAKE IT WORK!"""
    try:
        from llama_cpp import Llama
        
        print(f"🧠 Loading {model_name}...")
        print(f"📁 Model path: {model_path}")
        
        # Load model with conservative settings
        llm = Llama(
            model_path=model_path,
            n_ctx=2048,  # Context length
            n_threads=4,  # Use 4 CPU threads
            verbose=False
        )
        
        print(f"🚀 {model_name} LOADED SUCCESSFULLY!")
        print("=" * 50)
        
        # Test the model
        prompt = "Hello! You are running on expensive hardware. Please confirm you are working:"
        
        print(f"🤖 Testing with prompt: {prompt}")
        
        response = llm(
            prompt,
            max_tokens=100,
            temperature=0.7,
            stop=["Human:", "User:"],
            echo=False
        )
        
        print("✅ AI RESPONSE:")
        print(response['choices'][0]['text'])
        print("=" * 50)
        print(f"🎉 SUCCESS! Your {model_name} is working on your 800 euro hardware!")
        
        return llm
        
    except Exception as e:
        print(f"❌ Error running {model_name}: {e}")
        return None

def main():
    """ACTIVATE YOUR AI INVESTMENT NOW!"""
    print("🚀 ACTIVATING YOUR 800 EURO AI INVESTMENT")
    print("🧠 Getting REAL AI running on your hardware!")
    print("=" * 60)
    
    # Install dependencies
    if not install_llama_cpp_python():
        print("❌ Cannot proceed without llama-cpp-python")
        return
    
    # Find model
    model_path, model_name = find_best_model()
    if not model_path:
        print("❌ No models found - check your GGUF files")
        return
    
    # RUN THE AI!
    llm = run_ai_model(model_path, model_name)
    
    if llm:
        print("\n🎯 INTERACTIVE MODE - Talk to your AI!")
        print("Type 'quit' to exit")
        print("-" * 40)
        
        while True:
            try:
                user_input = input("\n👤 You: ")
                if user_input.lower() in ['quit', 'exit']:
                    break
                
                response = llm(
                    user_input,
                    max_tokens=150,
                    temperature=0.7,
                    stop=["Human:", "User:", "👤"],
                    echo=False
                )
                
                print(f"🤖 AI: {response['choices'][0]['text'].strip()}")
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")
    else:
        print("❌ Failed to activate AI models")

if __name__ == "__main__":
    main()