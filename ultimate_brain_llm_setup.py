#!/usr/bin/env python3
"""
🧠 ULTIMATE BRAIN LLM SETUP
Multi-server support with automatic model detection
"""
import subprocess
import sys
import os
import time
import requests
import json
from pathlib import Path
import psutil

class UltimateBrainLLMSetup:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.models = self._detect_models()
        self.servers = {
            'lm_studio': {'port': 1234, 'status': 'stopped'},
            'koboldcpp': {'port': 5001, 'status': 'stopped'},
            'koboldcpp_rocm': {'port': 5002, 'status': 'stopped'}
        }
        
    def _detect_models(self):
        """Detect available GGUF models"""
        models = []
        gguf_files = list(self.base_dir.glob("*.gguf"))
        
        for model_file in gguf_files:
            size_mb = model_file.stat().st_size / (1024 * 1024)
            
            # Determine model type and capabilities
            name = model_file.name.lower()
            capabilities = []
            
            if 'vision' in name or 'vl' in name or 'mmproj' in name:
                capabilities.append('vision')
            if 'qwen' in name:
                capabilities.append('multilingual')
            if 'gemma' in name:
                capabilities.append('reasoning')
            if 'llama' in name:
                capabilities.append('general')
                
            models.append({
                'name': model_file.stem,
                'file': model_file.name,
                'path': str(model_file),
                'size_mb': round(size_mb),
                'capabilities': capabilities
            })
        
        return sorted(models, key=lambda x: x['size_mb'])
    
    def print_banner(self):
        print("╔" + "═" * 60 + "╗")
        print("║" + "🧠 ULTIMATE BRAIN LLM SETUP".center(60) + "║")
        print("║" + "Multiple Servers + 5 Models Available".center(60) + "║")
        print("╚" + "═" * 60 + "╝")
        print()
    
    def show_available_models(self):
        """Show all detected models"""
        print("📚 AVAILABLE MODELS:")
        print("-" * 50)
        
        for i, model in enumerate(self.models, 1):
            print(f"{i}. 🤖 {model['name']}")
            print(f"   📁 File: {model['file']}")
            print(f"   💾 Size: {model['size_mb']} MB")
            print(f"   🎯 Capabilities: {', '.join(model['capabilities']) if model['capabilities'] else 'General'}")
            print()
    
    def check_server_status(self, port):
        """Check if a server is running on specified port"""
        try:
            response = requests.get(f"http://localhost:{port}/api/v1/model", timeout=2)
            return True
        except:
            try:
                response = requests.get(f"http://localhost:{port}/v1/models", timeout=2)
                return True
            except:
                return False
    
    def start_lm_studio(self):
        """Start LM Studio"""
        print("🎯 Starting LM Studio...")
        
        # Check if LM Studio is already running
        if self.check_server_status(1234):
            print("✅ LM Studio is already running on port 1234")
            self.servers['lm_studio']['status'] = 'running'
            return True
        
        # Try to start LM Studio via shortcut
        lm_studio_shortcut = self.base_dir / "LM Studio.lnk"
        if lm_studio_shortcut.exists():
            try:
                subprocess.Popen([str(lm_studio_shortcut)], shell=True)
                print("🚀 LM Studio launching...")
                print("📋 Manual steps needed:")
                print("   1. Go to 'Chat' tab")
                print("   2. Load a model from the list")
                print("   3. Go to 'Server' tab") 
                print("   4. Start local server on port 1234")
                print("   5. Come back here and test connection")
                return 'manual'
            except Exception as e:
                print(f"❌ Failed to start LM Studio: {e}")
                return False
        else:
            print("❌ LM Studio shortcut not found")
            return False
    
    def start_koboldcpp(self, use_rocm=False, model_path=None):
        """Start KoboldCpp server"""
        exe_name = "koboldcpp_rocm_b2.exe" if use_rocm else "koboldcpp.exe"
        port = 5002 if use_rocm else 5001
        server_name = "KoboldCpp (ROCm)" if use_rocm else "KoboldCpp"
        
        print(f"🔥 Starting {server_name}...")
        
        # Check if already running
        if self.check_server_status(port):
            print(f"✅ {server_name} is already running on port {port}")
            return True
        
        kobold_exe = self.base_dir / exe_name
        if not kobold_exe.exists():
            print(f"❌ {exe_name} not found")
            return False
        
        # Build command
        cmd = [str(kobold_exe)]
        
        if model_path:
            cmd.extend(["--model", model_path])
        
        cmd.extend([
            "--host", "0.0.0.0",
            "--port", str(port),
            "--contextsize", "4096",
            "--threads", "8"
        ])
        
        if use_rocm:
            cmd.extend(["--useclblast", "0", "0"])  # Use GPU acceleration
        
        try:
            print(f"🚀 Command: {' '.join(cmd)}")
            process = subprocess.Popen(
                cmd,
                cwd=str(self.base_dir),
                creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == "win32" else 0
            )
            
            print(f"✅ {server_name} started (PID: {process.pid})")
            print(f"🌐 Server will be available at: http://localhost:{port}")
            
            # Wait a moment for server to start
            time.sleep(3)
            
            if self.check_server_status(port):
                print(f"🎉 {server_name} is responding!")
                self.servers['koboldcpp_rocm' if use_rocm else 'koboldcpp']['status'] = 'running'
                return True
            else:
                print(f"⏳ {server_name} is still starting up...")
                return 'starting'
                
        except Exception as e:
            print(f"❌ Failed to start {server_name}: {e}")
            return False
    
    def test_all_servers(self):
        """Test connectivity to all possible servers"""
        print("🔍 TESTING ALL SERVERS:")
        print("-" * 40)
        
        test_ports = [
            (1234, "LM Studio"),
            (5001, "KoboldCpp"),
            (5002, "KoboldCpp ROCm"),
            (8080, "llama.cpp"),
            (11434, "Ollama")
        ]
        
        working_servers = []
        
        for port, name in test_ports:
            if self.check_server_status(port):
                print(f"✅ {name}: Online (port {port})")
                working_servers.append((name, port))
            else:
                print(f"❌ {name}: Offline (port {port})")
        
        return working_servers
    
    def create_brain_config(self, working_servers):
        """Create optimized brain configuration"""
        config = {
            "llm_endpoints": [],
            "default_model": "auto",
            "timeout": 30,
            "retry_attempts": 3,
            "fallback_to_internal": True
        }
        
        # Add working servers to config
        priority = 1
        for name, port in working_servers:
            endpoint = {
                "name": name,
                "url": f"http://localhost:{port}/v1",
                "type": "openai_compatible",
                "priority": priority,
                "enabled": True
            }
            
            # Special handling for KoboldCpp
            if "KoboldCpp" in name:
                endpoint["url"] = f"http://localhost:{port}/api/v1"
            
            config["llm_endpoints"].append(endpoint)
            priority += 1
        
        # Save configuration
        config_path = self.base_dir / "brain_llm_config.json"
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"✅ Brain configuration saved: {config_path}")
        return config_path
    
    def quick_setup_recommended(self):
        """Quick setup with recommended model"""
        print("🚀 QUICK SETUP - RECOMMENDED CONFIGURATION")
        print("=" * 50)
        
        # Recommend best model for current setup
        recommended_model = None
        for model in self.models:
            if model['size_mb'] < 3000:  # Under 3GB for good performance
                recommended_model = model
                break
        
        if recommended_model:
            print(f"🎯 Recommended model: {recommended_model['name']}")
            print(f"   Size: {recommended_model['size_mb']} MB")
            print(f"   Capabilities: {', '.join(recommended_model['capabilities'])}")
            
            # Try to start KoboldCpp with recommended model
            success = self.start_koboldcpp(
                use_rocm=True,  # Try ROCm first for better performance
                model_path=recommended_model['path']
            )
            
            if success == 'starting':
                print("⏳ Waiting for server to fully start...")
                time.sleep(10)
                
                # Test again
                if self.check_server_status(5002):
                    print("🎉 KoboldCpp ROCm is now online!")
                    working_servers = [("KoboldCpp ROCm", 5002)]
                    self.create_brain_config(working_servers)
                    return True
        
        return False
    
    def interactive_setup(self):
        """Interactive setup menu"""
        while True:
            print("\n🎯 CHOOSE SETUP OPTION:")
            print("1. 🚀 Quick Setup (Recommended)")
            print("2. 🎯 Start LM Studio")
            print("3. 🔥 Start KoboldCpp (Regular)")
            print("4. ⚡ Start KoboldCpp (ROCm GPU)")
            print("5. 📚 Show Available Models") 
            print("6. 🔍 Test All Servers")
            print("7. ⚙️  Create Brain Config")
            print("8. 🏃 Exit")
            
            choice = input("\nEnter choice (1-8): ").strip()
            
            if choice == "1":
                if self.quick_setup_recommended():
                    print("🎉 Quick setup complete! Your brain can now use enhanced LLM cognition.")
                    break
                else:
                    print("❌ Quick setup failed. Try manual options.")
                    
            elif choice == "2":
                self.start_lm_studio()
                
            elif choice == "3":
                # Select model for KoboldCpp
                self.show_available_models()
                try:
                    model_idx = int(input("Select model number: ")) - 1
                    if 0 <= model_idx < len(self.models):
                        model = self.models[model_idx]
                        self.start_koboldcpp(use_rocm=False, model_path=model['path'])
                    else:
                        print("❌ Invalid model selection")
                except ValueError:
                    print("❌ Invalid input")
                    
            elif choice == "4":
                # Select model for KoboldCpp ROCm
                self.show_available_models()
                try:
                    model_idx = int(input("Select model number: ")) - 1
                    if 0 <= model_idx < len(self.models):
                        model = self.models[model_idx]
                        self.start_koboldcpp(use_rocm=True, model_path=model['path'])
                    else:
                        print("❌ Invalid model selection")
                except ValueError:
                    print("❌ Invalid input")
                    
            elif choice == "5":
                self.show_available_models()
                
            elif choice == "6":
                working_servers = self.test_all_servers()
                if working_servers:
                    print(f"\n🎉 Found {len(working_servers)} working servers!")
                else:
                    print("\n⚠️  No servers are currently running")
                    
            elif choice == "7":
                working_servers = self.test_all_servers()
                if working_servers:
                    self.create_brain_config(working_servers)
                else:
                    print("❌ No working servers found. Start a server first.")
                    
            elif choice == "8":
                print("👋 Setup complete!")
                break
                
            else:
                print("❌ Invalid choice")

def main():
    setup = UltimateBrainLLMSetup()
    setup.print_banner()
    setup.show_available_models()
    setup.interactive_setup()

if __name__ == "__main__":
    main()