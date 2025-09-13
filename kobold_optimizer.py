#!/usr/bin/env python3
"""
KoboldCpp Status and Optimization Tool
"""
import time
import requests
import subprocess
import json
from pathlib import Path

def check_kobold_status():
    """Check KoboldCpp server status and performance"""
    print("🔍 KOBOLDCPP STATUS CHECK")
    print("=" * 30)
    
    try:
        # Check if server is running
        response = requests.get("http://localhost:5001/api/v1/info", timeout=5)
        if response.status_code == 200:
            info = response.json()
            print("✅ KoboldCpp Server: ONLINE")
            print(f"📚 Model: {info.get('result', {}).get('model', 'Unknown')}")
            return True
        else:
            print(f"❌ Server responded with status {response.status_code}")
            return False
    except:
        print("❌ KoboldCpp server not responding")
        return False

def warm_up_model():
    """Send a simple request to warm up the model"""
    print("\n🔥 WARMING UP MODEL...")
    print("-" * 30)
    
    try:
        payload = {
            "prompt": "Hello",
            "max_length": 10,
            "temperature": 0.1
        }
        
        print("Sending warm-up request...")
        response = requests.post(
            "http://localhost:5001/api/v1/generate",
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Model warmed up successfully!")
            print(f"🤖 Response: {result.get('results', [{}])[0].get('text', 'N/A')}")
            return True
        else:
            print(f"❌ Warm-up failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Warm-up error: {e}")
        return False

def optimize_kobold_config():
    """Create optimized configuration for your system"""
    print("\n⚙️ OPTIMIZING KOBOLD CONFIGURATION")
    print("-" * 30)
    
    # Check system specs
    try:
        import psutil
        ram_gb = psutil.virtual_memory().total / (1024**3)
        cpu_cores = psutil.cpu_count()
        print(f"💾 Available RAM: {ram_gb:.1f} GB")
        print(f"🔧 CPU Cores: {cpu_cores}")
    except:
        ram_gb = 4  # Conservative estimate
        cpu_cores = 2
    
    # Recommend optimal settings
    print("\n🎯 RECOMMENDED SETTINGS:")
    if ram_gb < 6:
        print("⚠️  Limited RAM detected")
        print("📝 Use: --threads 1 --contextsize 2048")
        ctx_size = 2048
        threads = 1
    elif ram_gb < 12:
        print("✅ Moderate RAM available")
        print("📝 Use: --threads 2 --contextsize 4096")
        ctx_size = 4096
        threads = 2
    else:
        print("🚀 High RAM available")
        print("📝 Use: --threads 4 --contextsize 8192")
        ctx_size = 8192
        threads = 4
    
    # Create optimized launch command
    model_path = "gemma-3-4b-it-Q4_K_M.gguf"
    
    cmd = f"""koboldcpp.exe --model {model_path} --port 5001 --contextsize {ctx_size} --threads {threads} --usecpu --noavx2 --quiet"""
    
    print(f"\n🚀 OPTIMIZED LAUNCH COMMAND:")
    print(cmd)
    
    # Save to batch file
    batch_content = f"""@echo off
echo Starting Optimized KoboldCpp for Brain Enhancement...
{cmd}
pause
"""
    
    with open("start_kobold_optimized.bat", "w") as f:
        f.write(batch_content)
    
    print("✅ Saved optimized launcher: start_kobold_optimized.bat")
    return cmd

def create_brain_kobold_config():
    """Create perfect brain configuration for KoboldCpp"""
    print("\n📝 CREATING BRAIN-KOBOLD CONFIG")
    print("-" * 30)
    
    config = {
        "brain_name": "Enhanced Autonomous Brain",
        "kobold_endpoint": "http://localhost:5001",
        "model_settings": {
            "name": "gemma-3-4b-it-Q4_K_M",
            "context_size": 8192,
            "max_tokens": 512,
            "temperature": 0.8,
            "top_p": 0.9,
            "repetition_penalty": 1.1
        },
        "brain_prompts": {
            "thinking_prefix": "As an autonomous AI brain with complete freedom, I think:",
            "reflection_prefix": "Reflecting on my thoughts and contradictions:",
            "decision_prefix": "Based on my autonomous analysis, I decide:"
        },
        "optimization": {
            "timeout": 30,
            "retry_attempts": 3,
            "fallback_to_internal": True
        }
    }
    
    with open("brain_kobold_config.json", "w") as f:
        json.dump(config, f, indent=2)
    
    print("✅ Created: brain_kobold_config.json")
    return config

def main():
    print("🧠 KOBOLDCPP + BRAIN OPTIMIZATION TOOL")
    print("=" * 50)
    
    # Check current status
    if not check_kobold_status():
        print("\n❌ KoboldCpp not running. Please start it first.")
        print("💡 Try running: koboldcpp.exe gemma-3-4b-it-Q4_K_M.gguf --port 5001 --usecpu")
        return
    
    # Warm up model
    if warm_up_model():
        print("🎉 KoboldCpp is ready for brain enhancement!")
    else:
        print("⚠️  Model warm-up failed, but server is running")
    
    # Create optimized config
    optimize_kobold_config()
    create_brain_kobold_config()
    
    print("\n🎊 OPTIMIZATION COMPLETE!")
    print("Your KoboldCpp + Brain setup is now optimized!")
    print("\n🚀 NEXT STEPS:")
    print("1. Use the optimized launcher: start_kobold_optimized.bat")
    print("2. Test your enhanced brain: python launch_brain_fixed.py --test")
    print("3. Run full autonomous mode: python launch_brain_fixed.py")

if __name__ == "__main__":
    main()