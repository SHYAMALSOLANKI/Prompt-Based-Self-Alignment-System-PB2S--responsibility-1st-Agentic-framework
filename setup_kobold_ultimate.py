#!/usr/bin/env python3
"""
Ultimate KoboldCpp + Brain Integration
Optimized for your GGUF models with no-CUDA reliability
"""
import subprocess
import time
import requests
import json
import os
import sys
from pathlib import Path
import threading
import asyncio

class UltimateKoboldBrainSetup:
    def __init__(self):
        self.script_dir = Path(__file__).parent
        self.models_available = self.scan_available_models()
        self.kobold_process = None
        self.kobold_url = "http://localhost:5001"
        
    def scan_available_models(self):
        """Scan for available GGUF models"""
        models = []
        for file in self.script_dir.glob("*.gguf"):
            size_mb = file.stat().st_size / (1024 * 1024)
            models.append({
                'name': file.name,
                'path': str(file),
                'size_mb': size_mb,
                'recommended': self.get_model_recommendation(file.name, size_mb)
            })
        return sorted(models, key=lambda x: x['size_mb'])
    
    def get_model_recommendation(self, name, size_mb):
        """Get recommendation for each model"""
        if 'gemma-3-4b' in name.lower():
            return "🌟 EXCELLENT - Fast, smart, great for conversation"
        elif 'qwen2.5-vl-7b' in name.lower():
            return "👁️ VISION - Can see and understand images"
        elif 'qwen2-vl-2b' in name.lower():
            return "⚡ FAST VISION - Lightweight with vision capabilities"
        elif 'llama-13b' in name.lower():
            return "🧠 POWERFUL - Best reasoning, needs more RAM"
        elif 'llama3-8b' in name.lower():
            return "⚖️ BALANCED - Good performance and capability"
        elif size_mb < 500:
            return "🚀 ULTRA FAST - Minimal resource usage"
        elif size_mb < 1500:
            return "⚡ FAST - Good balance of speed and capability"
        elif size_mb < 3000:
            return "🎯 RECOMMENDED - Best overall performance"
        else:
            return "🧠 POWERFUL - Maximum capability, needs good hardware"
    
    def print_models_menu(self):
        """Display available models with recommendations"""
        print("\n" + "="*80)
        print("🤖 AVAILABLE GGUF MODELS")
        print("="*80)
        
        for i, model in enumerate(self.models_available, 1):
            size_str = f"{model['size_mb']:.1f} MB"
            print(f"{i:2d}. {model['name']:<40} [{size_str:>10}]")
            print(f"    {model['recommended']}")
            print()
        
        return len(self.models_available)
    
    def start_koboldcpp(self, model_path, use_gpu=False):
        """Start KoboldCpp with the selected model"""
        print(f"\n🚀 Starting KoboldCpp with {Path(model_path).name}")
        print("=" * 60)
        
        # Find KoboldCpp executable
        kobold_exe = None
        for exe_name in ["koboldcpp.exe", "koboldcpp_rocm_b2.exe"]:
            exe_path = self.script_dir / exe_name
            if exe_path.exists():
                kobold_exe = exe_path
                break
        
        if not kobold_exe:
            print("❌ KoboldCpp executable not found!")
            return False
        
        # Build command
        cmd = [
            str(kobold_exe),
            "--model", model_path,
            "--port", "5001",
            "--host", "0.0.0.0",
            "--contextsize", "4096",
            "--blasbatchsize", "512",
            "--threads", "6"  # Adjust based on your CPU
        ]
        
        # Add GPU flags if requested and available
        if use_gpu:
            if "rocm" in str(kobold_exe).lower():
                cmd.extend(["--useclblast", "0", "0"])  # Use first GPU
                print("🔥 Using AMD GPU acceleration (ROCm)")
            else:
                cmd.extend(["--usecublas"])  # NVIDIA GPU
                print("⚡ Using NVIDIA GPU acceleration")
        else:
            print("💻 Using CPU-only mode (recommended for stability)")
        
        # Add memory optimization
        cmd.extend([
            "--smartcontext",  # Smart context management
            "--unbantokens",   # Allow all tokens
            "--usemirostat"    # Better text generation
        ])
        
        print(f"🔧 Command: {' '.join(cmd)}")
        print("\n⏳ Starting KoboldCpp... (this may take 30-60 seconds)")
        
        try:
            # Start KoboldCpp
            self.kobold_process = subprocess.Popen(
                cmd,
                cwd=str(self.script_dir),
                creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == "win32" else 0
            )
            
            # Wait for server to start
            print("⏳ Waiting for KoboldCpp to initialize...")
            for attempt in range(60):  # Wait up to 60 seconds
                try:
                    response = requests.get(f"{self.kobold_url}/api/v1/model", timeout=2)
                    if response.status_code == 200:
                        model_info = response.json()
                        print(f"✅ KoboldCpp is ready!")
                        print(f"📝 Model loaded: {model_info.get('result', 'Unknown')}")
                        print(f"🌐 Server URL: {self.kobold_url}")
                        return True
                except:
                    pass
                
                time.sleep(1)
                if attempt % 10 == 0:
                    print(f"   Still waiting... ({attempt + 1}/60 seconds)")
            
            print("❌ KoboldCpp failed to start within 60 seconds")
            return False
            
        except Exception as e:
            print(f"❌ Failed to start KoboldCpp: {e}")
            return False
    
    def test_kobold_connection(self):
        """Test connection to KoboldCpp"""
        try:
            # Test basic connection
            response = requests.get(f"{self.kobold_url}/api/v1/model", timeout=5)
            if response.status_code != 200:
                return False
            
            # Test text generation
            test_prompt = "Hello, how are you today?"
            gen_data = {
                "prompt": test_prompt,
                "max_length": 50,
                "temperature": 0.7
            }
            
            response = requests.post(f"{self.kobold_url}/api/v1/generate", 
                                   json=gen_data, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                generated_text = result.get('results', [{}])[0].get('text', '')
                print(f"✅ KoboldCpp test successful!")
                print(f"🧠 Test response: {generated_text[:100]}...")
                return True
            
        except Exception as e:
            print(f"❌ KoboldCpp test failed: {e}")
            return False
        
        return False
    
    def update_brain_llm_config(self):
        """Update brain configuration to use KoboldCpp"""
        config = {
            "llm_endpoints": [
                {
                    "name": "KoboldCpp",
                    "url": f"{self.kobold_url}/api/v1",
                    "type": "openai_compatible",
                    "priority": 1,
                    "enabled": True,
                    "model": "loaded_model"
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
            "timeout": 30,
            "retry_attempts": 3,
            "koboldcpp_active": True
        }
        
        config_path = self.script_dir / "brain_llm_config.json"
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"✅ Brain configuration updated: {config_path}")
        return config_path
    
    def launch_brain_with_kobold(self):
        """Launch the brain system with KoboldCpp"""
        print("\n🧠 LAUNCHING BRAIN WITH KOBOLDCPP")
        print("=" * 50)
        
        # Update brain config
        self.update_brain_llm_config()
        
        # Launch enhanced brain
        python_exe = self.script_dir / ".venv" / "Scripts" / "python.exe"
        brain_script = self.script_dir / "launch_brain_fixed.py"
        
        if not python_exe.exists():
            python_exe = "python"  # Use system Python
        
        try:
            print("🚀 Starting enhanced brain system...")
            brain_process = subprocess.Popen([
                str(python_exe), str(brain_script), "--test"
            ], cwd=str(self.script_dir))
            
            print("✅ Brain system started!")
            print("🌐 KoboldCpp endpoint configured")
            print("📊 Monitor brain activity in the logs")
            
            return brain_process
            
        except Exception as e:
            print(f"❌ Failed to start brain: {e}")
            return None
    
    def run_complete_setup(self):
        """Run the complete setup process"""
        print("🧠 ULTIMATE KOBOLDCPP + BRAIN SETUP")
        print("=" * 60)
        print("🎯 Setting up your autonomous brain with KoboldCpp")
        print("💪 Using no-CUDA for maximum stability")
        print()
        
        if not self.models_available:
            print("❌ No GGUF models found in current directory!")
            return False
        
        # Show available models
        model_count = self.print_models_menu()
        
        print("🎯 SETUP OPTIONS:")
        print("1. 🚀 Quick Start (Auto-select best model)")
        print("2. 🎯 Choose specific model")
        print("3. 🧪 Test existing KoboldCpp")
        print("4. 🔧 Advanced configuration")
        print("5. ❌ Exit")
        
        while True:
            try:
                choice = input("\nEnter choice (1-5): ").strip()
                
                if choice == "1":
                    # Auto-select best model (Gemma 3 4B if available, otherwise smallest)
                    best_model = None
                    for model in self.models_available:
                        if 'gemma-3-4b' in model['name'].lower():
                            best_model = model
                            break
                    
                    if not best_model:
                        best_model = self.models_available[0]  # Smallest model
                    
                    print(f"\n🎯 Auto-selected: {best_model['name']}")
                    print(f"💡 {best_model['recommended']}")
                    
                    if self.start_koboldcpp(best_model['path']):
                        if self.test_kobold_connection():
                            brain_process = self.launch_brain_with_kobold()
                            if brain_process:
                                print("\n🎉 SETUP COMPLETE!")
                                print("🧠 Your brain is now running with KoboldCpp!")
                                print("📊 Check autonomous_brain.log for activity")
                                return True
                    
                elif choice == "2":
                    model_choice = input(f"\nSelect model (1-{model_count}): ").strip()
                    try:
                        model_idx = int(model_choice) - 1
                        if 0 <= model_idx < len(self.models_available):
                            selected_model = self.models_available[model_idx]
                            print(f"\n🎯 Selected: {selected_model['name']}")
                            
                            use_gpu = input("Use GPU acceleration? (y/N): ").lower().startswith('y')
                            
                            if self.start_koboldcpp(selected_model['path'], use_gpu):
                                if self.test_kobold_connection():
                                    brain_process = self.launch_brain_with_kobold()
                                    if brain_process:
                                        print("\n🎉 SETUP COMPLETE!")
                                        return True
                        else:
                            print("❌ Invalid model selection")
                    except ValueError:
                        print("❌ Invalid input")
                
                elif choice == "3":
                    print("\n🧪 Testing existing KoboldCpp connection...")
                    if self.test_kobold_connection():
                        print("✅ KoboldCpp is working!")
                        brain_process = self.launch_brain_with_kobold()
                        if brain_process:
                            return True
                    else:
                        print("❌ No working KoboldCpp found")
                
                elif choice == "4":
                    print("\n🔧 Advanced Configuration")
                    print("Current KoboldCpp URL:", self.kobold_url)
                    new_url = input("Enter custom URL (or press Enter to keep current): ").strip()
                    if new_url:
                        self.kobold_url = new_url
                    
                    if self.test_kobold_connection():
                        brain_process = self.launch_brain_with_kobold()
                        if brain_process:
                            return True
                
                elif choice == "5":
                    print("👋 Setup cancelled")
                    return False
                
                else:
                    print("❌ Invalid choice")
                    
            except KeyboardInterrupt:
                print("\n👋 Setup interrupted")
                return False
        
        return False
    
    def cleanup(self):
        """Clean up processes"""
        if self.kobold_process:
            try:
                self.kobold_process.terminate()
                print("🔚 KoboldCpp stopped")
            except:
                pass

def main():
    setup = UltimateKoboldBrainSetup()
    
    try:
        success = setup.run_complete_setup()
        
        if success:
            print("\n" + "="*60)
            print("🎉 YOUR BRAIN IS NOW ENHANCED WITH KOBOLDCPP!")
            print("="*60)
            print("🧠 Brain system: Running with enhanced cognition")
            print("🤖 KoboldCpp: Providing powerful AI responses")
            print("📊 Monitor: Check autonomous_brain.log for activity")
            print("🌐 Access: Brain automatically uses KoboldCpp for thinking")
            print("\n🎯 Next steps:")
            print("1. Watch the brain logs for enhanced thinking")
            print("2. Test with: python launch_brain_fixed.py --test")
            print("3. Run dashboard: streamlit run enhanced_dashboard.py")
            print("\nPress Ctrl+C to stop all services")
            
            # Keep running
            try:
                while True:
                    time.sleep(10)
            except KeyboardInterrupt:
                print("\n🛑 Stopping services...")
                
    except Exception as e:
        print(f"❌ Setup failed: {e}")
    finally:
        setup.cleanup()

if __name__ == "__main__":
    main()