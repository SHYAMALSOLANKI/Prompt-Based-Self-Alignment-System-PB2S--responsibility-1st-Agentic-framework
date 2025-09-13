#!/usr/bin/env python3
"""
Ultimate KoboldCpp + Brain Integration
Now that KoboldCpp is running, let's connect your brain!
"""
import requests
import json
import asyncio
import subprocess
from pathlib import Path

def test_koboldcpp_connection():
    """Test connection to your running KoboldCpp server"""
    print("🔗 Testing KoboldCpp Connection...")
    print("-" * 40)
    
    try:
        # Test the running server on port 5001
        response = requests.get("http://localhost:5001/api/v1/model", timeout=5)
        if response.status_code == 200:
            model_info = response.json()
            print("✅ KoboldCpp Server: ONLINE")
            print(f"📚 Model: {model_info.get('result', 'Gemma 3 4B')}")
            print(f"🔗 Endpoint: http://localhost:5001")
            print(f"🌐 API: OpenAI Compatible")
            return True
        else:
            print(f"❌ Server responded with status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

def test_chat_completion():
    """Test chat completion with your Gemma model"""
    print("\n🧠 Testing Chat Completion...")
    print("-" * 40)
    
    try:
        payload = {
            "model": "gemma-3-4b-it-Q4_K_M.gguf",
            "messages": [
                {
                    "role": "user", 
                    "content": "Hello! I'm testing my autonomous brain connection. Please respond briefly."
                }
            ],
            "max_tokens": 100,
            "temperature": 0.7
        }
        
        response = requests.post(
            "http://localhost:5001/v1/chat/completions",
            headers={"Content-Type": "application/json"},
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            message = result['choices'][0]['message']['content']
            print("✅ Chat Completion: SUCCESS")
            print(f"🤖 Gemma Response: {message.strip()}")
            return True
        else:
            print(f"❌ Chat completion failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Chat test failed: {e}")
        return False

def create_brain_config():
    """Create brain configuration for KoboldCpp"""
    config = {
        "brain_name": "Enhanced Autonomous Brain",
        "llm_servers": [
            {
                "name": "KoboldCpp_Gemma3",
                "url": "http://localhost:5001/v1",
                "type": "openai_compatible",
                "model": "gemma-3-4b-it-Q4_K_M.gguf",
                "priority": 1,
                "enabled": True,
                "max_tokens": 2048,
                "temperature": 0.8,
                "stream": True
            }
        ],
        "fallback_mode": "internal_cognition",
        "enhanced_capabilities": {
            "vision_models": [
                "qwen2.5-vl-7b-vision-mmproj-f16.gguf",
                "Qwen2-VL-2B-mmproj-q5_1.gguf"
            ],
            "multimodal_enabled": True,
            "autonomous_learning": True
        }
    }
    
    config_path = Path("enhanced_brain_config.json")
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"✅ Enhanced brain config saved: {config_path}")
    return config_path

def main():
    print("🧠 ULTIMATE BRAIN + KOBOLDCPP INTEGRATION")
    print("=" * 50)
    
    # Test KoboldCpp connection
    if not test_koboldcpp_connection():
        print("\n❌ KoboldCpp not responding. Please check:")
        print("   1. KoboldCpp is running on port 5001")
        print("   2. Model is loaded (Gemma 3 4B)")
        print("   3. No firewall blocking localhost:5001")
        return False
    
    # Test chat completion
    if not test_chat_completion():
        print("\n❌ Chat completion test failed")
        return False
    
    # Create enhanced brain config
    config_path = create_brain_config()
    
    print("\n🎉 INTEGRATION COMPLETE!")
    print("=" * 50)
    print("Your brain now has access to:")
    print("🤖 Gemma 3 4B model via KoboldCpp")
    print("🧠 Enhanced cognitive capabilities")
    print("🔗 OpenAI-compatible API")
    print("⚡ Optimized performance")
    
    print("\n🚀 READY TO LAUNCH ENHANCED BRAIN:")
    print("python launch_brain_fixed.py")
    
    return True

if __name__ == "__main__":
    main()