#!/usr/bin/env python3
"""
REAL AI ACTIVATION - Your 800 Euro Investment Working NOW!
Using PyTorch to run models on CPU while we fix Jetson access
"""

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import os
import json
from pathlib import Path

class RealAIRunner:
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.device = "cpu"  # Start with CPU
        
    def list_available_models(self):
        """Find what we can actually run"""
        print("🔍 Scanning for usable AI models...")
        
        # Check for local models that transformers can load
        small_models = [
            "microsoft/DialoGPT-small",
            "gpt2",
            "distilgpt2",
            "microsoft/DialoGPT-medium"
        ]
        
        print("📦 Available models to download and run:")
        for i, model in enumerate(small_models, 1):
            print(f"{i}. {model}")
        
        return small_models
    
    def load_model(self, model_name):
        """Load and run a real AI model"""
        try:
            print(f"🧠 Loading {model_name}...")
            
            # Load tokenizer and model
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForCausalLM.from_pretrained(model_name)
            
            # Add pad token if missing
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            print(f"✅ {model_name} loaded successfully!")
            print(f"🖥️  Running on: {self.device}")
            print(f"💾 Model parameters: {self.model.num_parameters():,}")
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to load {model_name}: {e}")
            return False
    
    def generate_response(self, prompt, max_length=100):
        """Generate actual AI response"""
        if not self.model or not self.tokenizer:
            return "❌ No model loaded"
        
        try:
            # Encode input
            inputs = self.tokenizer.encode(prompt, return_tensors="pt")
            
            # Generate response
            with torch.no_grad():
                outputs = self.model.generate(
                    inputs,
                    max_length=max_length,
                    num_return_sequences=1,
                    temperature=0.7,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id
                )
            
            # Decode response
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Remove the input prompt from response
            if response.startswith(prompt):
                response = response[len(prompt):].strip()
            
            return response
            
        except Exception as e:
            return f"❌ Generation error: {e}"
    
    def interactive_mode(self):
        """Chat with your AI"""
        print("\n🤖 INTERACTIVE AI MODE - Your 800 euros at work!")
        print("Type 'quit' to exit, 'info' for model info")
        print("=" * 50)
        
        while True:
            try:
                user_input = input("\n👤 You: ").strip()
                
                if user_input.lower() in ['quit', 'exit']:
                    print("👋 Goodbye!")
                    break
                
                if user_input.lower() == 'info':
                    print(f"🧠 Model: {self.model.__class__.__name__}")
                    print(f"💾 Parameters: {self.model.num_parameters():,}")
                    print(f"🖥️  Device: {self.device}")
                    continue
                
                if not user_input:
                    continue
                
                print("🤖 AI: ", end="", flush=True)
                response = self.generate_response(user_input, max_length=150)
                print(response)
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")

def main():
    """GET YOUR AI WORKING NOW!"""
    print("🚀 ACTIVATING YOUR 800 EURO AI INVESTMENT")
    print("🧠 Real AI models running on your hardware!")
    print("=" * 60)
    
    ai = RealAIRunner()
    
    # Show available models
    models = ai.list_available_models()
    
    print("\n🎯 Which model do you want to run?")
    try:
        choice = input("Enter number (1-4) or press Enter for GPT-2: ").strip()
        
        if choice == "":
            model_choice = "gpt2"
        elif choice.isdigit() and 1 <= int(choice) <= len(models):
            model_choice = models[int(choice) - 1]
        else:
            model_choice = "gpt2"  # Default
        
        print(f"\n🔄 Selected: {model_choice}")
        
        # Load and run the model
        if ai.load_model(model_choice):
            print("\n🎉 SUCCESS! Your AI is running!")
            
            # Test it
            test_prompt = "Hello, I invested 800 euros in AI hardware."
            print(f"\n🧪 Testing with: '{test_prompt}'")
            response = ai.generate_response(test_prompt)
            print(f"🤖 AI Response: {response}")
            
            # Interactive mode
            ai.interactive_mode()
        else:
            print("❌ Failed to load any model")
            
    except KeyboardInterrupt:
        print("\n👋 Cancelled by user")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()