#!/usr/bin/env python3
"""
Local LLM Server Setup Guide and Quick Installer
Supports LM Studio, Ollama, and llama.cpp
"""
import subprocess
import sys
import os
import requests
import zipfile
import json
from pathlib import Path

class LLMServerInstaller:
    def __init__(self):
        self.home_dir = Path.home()
        self.llm_dir = self.home_dir / "ai_llm_servers"
        self.llm_dir.mkdir(exist_ok=True)
        
    def print_header(self, title):
        print(f"\n{'='*60}")
        print(f"🚀 {title}")
        print(f"{'='*60}")
    
    def install_lm_studio(self):
        """Install LM Studio (Recommended for beginners)"""
        self.print_header("LM Studio Installation")
        
        print("🎯 LM Studio - Best for Beginners")
        print("   ✅ Easy GUI interface")
        print("   ✅ Automatic model management")
        print("   ✅ Built-in API server")
        print("   ✅ Windows/Mac/Linux support")
        print()
        
        print("📥 Installation Steps:")
        print("1. Download from: https://lmstudio.ai/")
        print("2. Install the application")
        print("3. Launch LM Studio")
        print("4. Go to 'Discover' tab")
        print("5. Download a model (recommended: 'llama-2-7b-chat.Q4_K_M.gguf')")
        print("6. Go to 'Chat' tab and load the model")
        print("7. Go to 'Server' tab and start local server on port 1234")
        print()
        
        print("⚙️  Server Configuration:")
        print("   - Host: localhost")
        print("   - Port: 1234")
        print("   - API: OpenAI Compatible")
        print()
        
        # Test if LM Studio is already running
        try:
            response = requests.get("http://localhost:1234/v1/models", timeout=2)
            if response.status_code == 200:
                print("✅ LM Studio server is already running!")
                models = response.json().get('data', [])
                print(f"📚 Available models: {len(models)}")
                for model in models:
                    print(f"   - {model.get('id', 'Unknown')}")
        except:
            print("❌ LM Studio server not detected")
            print("   Please install and start LM Studio manually")
    
    def install_ollama(self):
        """Install Ollama (Good for intermediate users)"""
        self.print_header("Ollama Installation")
        
        print("🔥 Ollama - Command Line LLM Runner")
        print("   ✅ Simple command line interface")
        print("   ✅ Easy model management")
        print("   ✅ Good performance")
        print("   ✅ Multiple model support")
        print()
        
        if sys.platform == "win32":
            print("📥 Windows Installation:")
            print("1. Download from: https://ollama.ai/download")
            print("2. Run the installer")
            print("3. Open Command Prompt or PowerShell")
            print("4. Run: ollama pull llama2:7b-chat")
            print("5. Run: ollama serve")
            print()
        else:
            print("📥 Linux/Mac Installation:")
            print("curl https://ollama.ai/install.sh | sh")
            print("ollama pull llama2:7b-chat")
            print("ollama serve")
            print()
        
        print("⚙️  Server Configuration:")
        print("   - Host: localhost")
        print("   - Port: 11434")
        print("   - API: Ollama API")
        print()
        
        # Test if Ollama is running
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=2)
            if response.status_code == 200:
                print("✅ Ollama server is running!")
                models = response.json().get('models', [])
                print(f"📚 Available models: {len(models)}")
                for model in models:
                    print(f"   - {model.get('name', 'Unknown')}")
        except:
            print("❌ Ollama server not detected")
    
    def install_llamacpp_server(self):
        """Install llama.cpp server (Advanced users)"""
        self.print_header("llama.cpp Server Installation")
        
        print("⚡ llama.cpp - Maximum Performance")
        print("   ✅ Fastest inference")
        print("   ✅ Minimal resource usage")
        print("   ✅ Full control over parameters")
        print("   ❌ More complex setup")
        print()
        
        llamacpp_dir = self.llm_dir / "llama.cpp"
        
        if not llamacpp_dir.exists():
            print("📥 Downloading llama.cpp...")
            try:
                if sys.platform == "win32":
                    # Download pre-compiled Windows binary
                    url = "https://github.com/ggerganov/llama.cpp/releases/latest/download/llama-b1834-bin-win-avx2-x64.zip"
                    response = requests.get(url)
                    
                    zip_path = self.llm_dir / "llamacpp.zip"
                    with open(zip_path, 'wb') as f:
                        f.write(response.content)
                    
                    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                        zip_ref.extractall(llamacpp_dir)
                    
                    zip_path.unlink()  # Remove zip file
                    print("✅ llama.cpp downloaded and extracted")
                else:
                    # Linux/Mac - compile from source
                    subprocess.run(["git", "clone", "https://github.com/ggerganov/llama.cpp.git", str(llamacpp_dir)])
                    subprocess.run(["make", "-C", str(llamacpp_dir)])
                    print("✅ llama.cpp compiled")
                    
            except Exception as e:
                print(f"❌ Failed to install llama.cpp: {e}")
                return
        
        print("\n📚 Model Setup:")
        print("1. Download a GGUF model (e.g., from HuggingFace)")
        print("2. Place model file in:", llamacpp_dir / "models")
        print("3. Start server:")
        
        if sys.platform == "win32":
            server_cmd = f"{llamacpp_dir}/server.exe"
        else:
            server_cmd = f"{llamacpp_dir}/server"
            
        print(f"   {server_cmd} -m models/your-model.gguf -c 2048 --host 0.0.0.0 --port 8080")
        print()
        
        print("⚙️  Server Configuration:")
        print("   - Host: localhost")
        print("   - Port: 8080")
        print("   - API: OpenAI Compatible")
    
    def create_brain_llm_config(self):
        """Create configuration for brain to connect to LLM servers"""
        config = {
            "llm_endpoints": [
                {
                    "name": "LM Studio",
                    "url": "http://localhost:1234/v1",
                    "type": "openai_compatible",
                    "priority": 1,
                    "enabled": True
                },
                {
                    "name": "llama.cpp",
                    "url": "http://localhost:8080/v1",
                    "type": "openai_compatible", 
                    "priority": 2,
                    "enabled": True
                },
                {
                    "name": "Ollama",
                    "url": "http://localhost:11434/v1",
                    "type": "ollama",
                    "priority": 3,
                    "enabled": True
                }
            ],
            "default_model": "auto",
            "timeout": 30,
            "retry_attempts": 3
        }
        
        config_path = Path("brain_llm_config.json")
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"✅ Brain LLM configuration saved to: {config_path}")
        return config_path
    
    def test_all_servers(self):
        """Test connectivity to all LLM servers"""
        self.print_header("Testing LLM Server Connectivity")
        
        servers = [
            ("LM Studio", "http://localhost:1234/v1/models"),
            ("llama.cpp", "http://localhost:8080/v1/models"),
            ("Ollama", "http://localhost:11434/api/tags")
        ]
        
        working_servers = []
        
        for name, url in servers:
            try:
                response = requests.get(url, timeout=3)
                if response.status_code == 200:
                    print(f"✅ {name}: Online")
                    working_servers.append(name)
                else:
                    print(f"❌ {name}: HTTP {response.status_code}")
            except requests.exceptions.RequestException:
                print(f"❌ {name}: Not responding")
        
        print(f"\n📊 Summary: {len(working_servers)}/3 servers online")
        
        if working_servers:
            print("🎉 Your brain can now use enhanced LLM cognition!")
        else:
            print("⚠️  No LLM servers detected. Brain will use internal cognition.")
        
        return working_servers
    
    def show_recommended_models(self):
        """Show recommended models for different use cases"""
        self.print_header("Recommended Models")
        
        models = [
            {
                "name": "Llama 2 7B Chat",
                "file": "llama-2-7b-chat.Q4_K_M.gguf",
                "size": "3.8 GB",
                "ram": "6 GB",
                "use_case": "General conversation, coding help",
                "performance": "Fast"
            },
            {
                "name": "Code Llama 7B",
                "file": "codellama-7b-instruct.Q4_K_M.gguf", 
                "size": "3.8 GB",
                "ram": "6 GB",
                "use_case": "Programming, code generation",
                "performance": "Fast"
            },
            {
                "name": "Llama 2 13B Chat",
                "file": "llama-2-13b-chat.Q4_K_M.gguf",
                "size": "7.3 GB", 
                "ram": "10 GB",
                "use_case": "Better reasoning, complex tasks",
                "performance": "Medium"
            },
            {
                "name": "Mixtral 8x7B",
                "file": "mixtral-8x7b-instruct-v0.1.Q4_K_M.gguf",
                "size": "26 GB",
                "ram": "32 GB", 
                "use_case": "Advanced reasoning, research",
                "performance": "Slow but very capable"
            }
        ]
        
        print("💾 Model Recommendations:")
        print()
        
        for model in models:
            print(f"🤖 {model['name']}")
            print(f"   📁 File: {model['file']}")
            print(f"   💾 Size: {model['size']} | RAM: {model['ram']}")
            print(f"   🎯 Use: {model['use_case']}")
            print(f"   ⚡ Speed: {model['performance']}")
            print()
        
        print("📥 Download sources:")
        print("   - HuggingFace: https://huggingface.co/models?search=gguf")
        print("   - LM Studio: Built-in model browser")
        print("   - Ollama: ollama pull <model-name>")

def main():
    installer = LLMServerInstaller()
    
    print("🧠 Local LLM Server Setup for Enhanced Brain Cognition")
    print("=" * 60)
    
    while True:
        print("\n🎯 Choose installation option:")
        print("1. Install LM Studio (Recommended for beginners)")
        print("2. Install Ollama (Command line)")
        print("3. Install llama.cpp (Advanced)")
        print("4. Test all servers")
        print("5. Show recommended models")
        print("6. Create brain configuration")
        print("7. Exit")
        
        choice = input("\nEnter your choice (1-7): ").strip()
        
        if choice == "1":
            installer.install_lm_studio()
        elif choice == "2":
            installer.install_ollama()
        elif choice == "3":
            installer.install_llamacpp_server()
        elif choice == "4":
            installer.test_all_servers()
        elif choice == "5":
            installer.show_recommended_models()
        elif choice == "6":
            installer.create_brain_llm_config()
        elif choice == "7":
            print("👋 Setup complete! Your brain is ready for enhanced cognition.")
            break
        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main()