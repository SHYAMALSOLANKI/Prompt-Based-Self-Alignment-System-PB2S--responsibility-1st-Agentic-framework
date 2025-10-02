#!/usr/bin/env python3
"""
KoboldCpp + Brain Integration Setup
Optimized for your specific GGUF models and hardware
"""
import subprocess
import sys
import os
import requests
import time
import json
from pathlib import Path
import psutil

class KoboldBrainSetup:
    def __init__(self):
        self.script_dir = Path(__file__).parent
        self.kobold_exe = self.script_dir / "koboldcpp_rocm_b2.exe"
        self.models_dir = self.script_dir
        
        # Your available models
        self.available_models = {
            "gemma-3-4b": {
                "file": "gemma-3-4b-it-Q4_K_M.gguf",
                "size_gb": 2.4,
                "ram_needed": 4,
                "description": "Google Gemma 3 4B - Excellent for conversation and reasoning",
                "recommended": True
            },
            "qwen2.5-vl-7b": {
                "file": "qwen2.5-vl-7b-vision-mmproj-f16.gguf", 
                "size_gb": 1.3,
                "ram_needed": 3,
                "description": "Qwen 2.5 VL 7B - Advanced vision + language model",
                "recommended": True
            },
            "qwen2-vl-2b": {
                "file": "Qwen2-VL-2B-mmproj-q5_1.gguf",
                "size_gb": 0.5,
                "ram_needed": 2,
                "description": "Qwen 2 VL 2B - Lightweight vision model",
                "recommended": False
            },
            "llama-13b-proj": {
                "file": "llama-13b-mmproj-v1.5.Q4_1.gguf",
                "size_gb": 0.2,
                "ram_needed": 1,
                "description": "LLaMA 13B projection layer",
                "recommended": False
            },
            "llama3-8b-proj": {
                "file": "LLaMA3-8B_mmproj-Q4_1.gguf",
                "size_gb": 0.2,
                "ram_needed": 1,
                "description": "LLaMA 3 8B projection layer", 
                "recommended": False
            }
        }
    
    def check_system_specs(self):
        """Analyze current system capabilities"""
        print("🔍 SYSTEM ANALYSIS")
        print("=" * 50)
        
        # RAM
        ram_gb = psutil.virtual_memory().total / (1024**3)
        print(f"💾 RAM: {ram_gb:.1f} GB")
        
        # CPU
        cpu_count = psutil.cpu_count()
        cpu_freq = psutil.cpu_freq()
        print(f"🧠 CPU: {cpu_count} cores @ {cpu_freq.max:.0f} MHz")
        
        # Storage
        disk = psutil.disk_usage(str(self.script_dir))
        free_gb = disk.free / (1024**3)
        print(f"💿 Free Storage: {free_gb:.1f} GB")
        
        # Recommendations
        print("\n🎯 MODEL RECOMMENDATIONS:")
        print("-" * 30)
        
        for model_id, info in self.available_models.items():
            model_file = self.models_dir / info["file"]
            exists = "✅" if model_file.exists() else "❌"
            
            if ram_gb >= info["ram_needed"]:
                ram_status = "✅"
            else:
                ram_status = "⚠️"
            
            if info["recommended"]:
                star = "⭐"
            else:
                star = "  "
            
            print(f"{star} {exists} {ram_status} {model_id}")
            print(f"     📁 {info['file']}")
            print(f"     💾 Needs {info['ram_needed']}GB RAM")
            print(f"     📝 {info['description']}")
            print()
        
        return {
            'ram_gb': ram_gb,
            'cpu_count': cpu_count,
            'free_storage_gb': free_gb,
            'can_run_gemma': ram_gb >= 4,
            'can_run_qwen_7b': ram_gb >= 3,
            'can_run_qwen_2b': ram_gb >= 2
        }
    
    def recommend_best_model(self, system_specs):
        """Recommend the best model for current system"""
        ram_gb = system_specs['ram_gb']
        
        if ram_gb >= 4:
            return "gemma-3-4b", "🌟 Excellent choice! Gemma 3 4B will run smoothly"
        elif ram_gb >= 3:
            return "qwen2.5-vl-7b", "🎯 Good choice! Qwen 2.5 VL 7B with vision capabilities"
        elif ram_gb >= 2:
            return "qwen2-vl-2b", "⚡ Lightweight option: Qwen 2 VL 2B"
        else:
            return None, "❌ Need at least 2GB RAM for AI models"
    
    def start_koboldcpp_server(self, model_choice, custom_params=None):
        """Start KoboldCpp server with optimal settings"""
        model_info = self.available_models[model_choice]
        model_path = self.models_dir / model_info["file"]
        
        if not model_path.exists():
            print(f"❌ Model file not found: {model_path}")
            return None
        
        print(f"🚀 Starting KoboldCpp with {model_choice}...")
        print(f"📁 Model: {model_path}")
        
        # Base command
        cmd = [
            str(self.kobold_exe),
            str(model_path),
            "--host", "127.0.0.1",
            "--port", "5001",  # Different from default to avoid conflicts
            "--contextsize", "2048",
            "--threads", str(min(psutil.cpu_count(), 8)),
        ]
        
        # Add GPU acceleration if available (ROCm for AMD)
        if "rocm" in str(self.kobold_exe).lower():
            cmd.extend(["--gpulayers", "99"])  # Use all GPU layers
            print("🔥 Using AMD ROCm GPU acceleration")
        
        # Custom parameters
        if custom_params:
            cmd.extend(custom_params)
        
        print(f"⚡ Command: {' '.join(cmd)}")
        print("🌐 Server will be available at: http://localhost:5001")
        print("⏳ Starting server (this may take a minute)...")
        
        try:
            # Start KoboldCpp
            process = subprocess.Popen(
                cmd,
                cwd=str(self.script_dir),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == "win32" else 0
            )
            
            # Wait for server to start
            print("⏳ Waiting for server to initialize...")
            for i in range(30):  # Wait up to 30 seconds
                try:
                    response = requests.get("http://localhost:5001/api/v1/model", timeout=2)
                    if response.status_code == 200:
                        print("✅ KoboldCpp server is running!")
                        print(f"🧠 Model loaded: {response.json().get('result', 'Unknown')}")
                        return process
                except:
                    pass
                
                time.sleep(1)
                print(f"⏳ Still starting... ({i+1}/30)")
            
            print("⚠️ Server may still be starting. Check the KoboldCpp window.")
            return process
            
        except Exception as e:
            print(f"❌ Failed to start KoboldCpp: {e}")
            return None
    
    def test_kobold_connection(self):
        """Test connection to KoboldCpp server"""
        print("🧪 Testing KoboldCpp connection...")
        
        try:
            # Test model endpoint
            response = requests.get("http://localhost:5001/api/v1/model", timeout=5)
            if response.status_code == 200:
                model_info = response.json()
                print("✅ KoboldCpp is responding!")
                print(f"📋 Model: {model_info.get('result', 'Unknown')}")
                
                # Test generation
                test_prompt = {
                    "prompt": "Hello! How are you today?",
                    "max_length": 50,
                    "temperature": 0.7
                }
                
                gen_response = requests.post(
                    "http://localhost:5001/api/v1/generate", 
                    json=test_prompt,
                    timeout=30
                )
                
                if gen_response.status_code == 200:
                    result = gen_response.json()
                    print("✅ Text generation working!")
                    print(f"🤖 Response: {result.get('results', [{}])[0].get('text', 'No response')[:100]}...")
                    return True
                else:
                    print(f"⚠️ Generation failed: {gen_response.status_code}")
                    return False
            else:
                print(f"❌ Server not responding: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False
    
    def configure_brain_for_kobold(self):
        """Configure brain to use KoboldCpp server"""
        config = {
            "llm_endpoints": [
                {
                    "name": "KoboldCpp",
                    "url": "http://localhost:5001/api/v1",
                    "type": "kobold_compatible",
                    "priority": 1,
                    "enabled": True
                },
                {
                    "name": "LM Studio",
                    "url": "http://localhost:1234/v1",
                    "type": "openai_compatible",
                    "priority": 2,
                    "enabled": True
                }
            ],
            "default_model": "auto",
            "timeout": 60,
            "retry_attempts": 3,
            "generation_params": {
                "max_length": 512,
                "temperature": 0.7,
                "top_p": 0.9,
                "rep_pen": 1.1
            }
        }
        
        config_path = self.script_dir / "brain_llm_config.json"
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"✅ Brain configured for KoboldCpp: {config_path}")
        return config_path
    
    def assess_hardware_needs(self, system_specs):
        """Assess if additional hardware is needed"""
        print("\n🏗️ HARDWARE ASSESSMENT")
        print("=" * 50)
        
        ram_gb = system_specs['ram_gb']
        
        if ram_gb >= 8:
            print("🎉 EXCELLENT SETUP!")
            print("✅ Your laptop can run large models smoothly")
            print("✅ Can handle Gemma 3 4B + system overhead")
            print("✅ No additional hardware needed")
            recommendation = "continue_current"
        elif ram_gb >= 4:
            print("🎯 GOOD SETUP!")
            print("✅ Can run medium models well")
            print("✅ Gemma 3 4B will work") 
            print("⚡ Consider 8GB+ for better performance")
            recommendation = "optional_upgrade"
        elif ram_gb >= 2:
            print("⚡ MINIMAL SETUP")
            print("⚠️ Limited to small models")
            print("✅ Qwen 2B models will work")
            print("🔄 Upgrade recommended for better AI")
            recommendation = "upgrade_recommended"
        else:
            print("❌ INSUFFICIENT RAM")
            print("❌ Cannot run modern AI models effectively")
            print("🛒 Upgrade required")
            recommendation = "upgrade_required"
        
        print("\n🛒 HARDWARE RECOMMENDATIONS:")
        print("-" * 30)
        
        if recommendation in ["upgrade_recommended", "upgrade_required"]:
            print("💻 Refurbished Options:")
            print("  • Intel N110 system: 8GB RAM + SSD")
            print("  • Intel N95 system: 16GB RAM + SSD")
            print("  • Expected cost: $300-600")
            print("  • Benefits: 3-5x better AI performance")
            print()
            print("⚡ Alternative: RAM upgrade current laptop")
            print("  • Add 8-16GB RAM if possible")
            print("  • Much cheaper option")
        else:
            print("✅ Your current laptop is sufficient!")
            print("💡 Optional: N95 system for dedicated AI server")
            print("🏠 Use current laptop + future Jetson setup")
        
        return recommendation

def main():
    setup = KoboldBrainSetup()
    
    print("🧠 KOBOLDCPP + BRAIN INTEGRATION SETUP")
    print("=" * 60)
    print("🎯 Optimizing your 5 GGUF models for maximum performance")
    print()
    
    # Check if KoboldCpp exists
    if not setup.kobold_exe.exists():
        print(f"❌ KoboldCpp not found: {setup.kobold_exe}")
        print("📥 Please ensure koboldcpp_rocm_b2.exe is in the current directory")
        return
    
    print("✅ KoboldCpp found!")
    print()
    
    # Analyze system
    system_specs = setup.check_system_specs()
    
    # Get hardware recommendation
    hardware_rec = setup.assess_hardware_needs(system_specs)
    
    # Get best model recommendation
    best_model, model_message = setup.recommend_best_model(system_specs)
    print(f"\n🎯 RECOMMENDED MODEL: {best_model}")
    print(f"💡 {model_message}")
    
    print("\n🚀 SETUP OPTIONS:")
    print("1. 🧪 Test best model with KoboldCpp")
    print("2. 🎯 Start KoboldCpp + configure brain")
    print("3. 🔧 Custom model selection")
    print("4. 🧠 Test brain with current setup")
    print("5. 💡 Hardware purchase advice")
    print("6. 🏃 Exit")
    
    choice = input("\nEnter choice (1-6): ").strip()
    
    if choice == "1" and best_model:
        # Test best model
        process = setup.start_koboldcpp_server(best_model)
        if process:
            time.sleep(5)
            setup.test_kobold_connection()
            
    elif choice == "2" and best_model:
        # Full setup
        process = setup.start_koboldcpp_server(best_model)
        if process:
            time.sleep(5)
            if setup.test_kobold_connection():
                setup.configure_brain_for_kobold()
                print("\n🎉 SETUP COMPLETE!")
                print("✅ KoboldCpp running with your best model")
                print("✅ Brain configured to use KoboldCpp")
                print("🚀 Run: python launch_brain_fixed.py")
                
    elif choice == "3":
        # Custom model selection
        print("\n🎯 Available models:")
        for i, (model_id, info) in enumerate(setup.available_models.items(), 1):
            exists = "✅" if (setup.models_dir / info["file"]).exists() else "❌"
            print(f"{i}. {exists} {model_id} - {info['description']}")
        
        try:
            model_choice = int(input("Select model (1-5): ")) - 1
            model_ids = list(setup.available_models.keys())
            if 0 <= model_choice < len(model_ids):
                selected_model = model_ids[model_choice]
                process = setup.start_koboldcpp_server(selected_model)
        except:
            print("❌ Invalid selection")
            
    elif choice == "4":
        # Test brain
        print("🧠 Testing brain with current configuration...")
        os.system("python launch_brain_fixed.py --test")
        
    elif choice == "5":
        # Hardware advice
        if hardware_rec == "upgrade_required":
            print("\n💻 HARDWARE PURCHASE RECOMMENDATION:")
            print("🎯 Intel N95 Mini PC (Recommended)")
            print("  • 16GB RAM + 512GB SSD")
            print("  • Price: ~$400-500 refurbished")
            print("  • Perfect for dedicated AI server")
            print("  • Can run larger models smoothly")
            print()
            print("⚡ Intel N110 Alternative")
            print("  • 8GB RAM + 256GB SSD") 
            print("  • Price: ~$250-350 refurbished")
            print("  • Good for medium AI models")
            print()
            print("🏠 Recommendation: Get N95 for future-proof AI lab")
        else:
            print("✅ Your current laptop should work well!")
            print("💡 Consider N95 only for dedicated AI server setup")
    
    elif choice == "6":
        print("👋 Setup complete!")
    
    else:
        print("❌ Invalid choice")

if __name__ == "__main__":
    main()