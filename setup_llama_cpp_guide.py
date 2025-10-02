#!/usr/bin/env python3
"""
llama.cpp Build and Setup Guide for PB2S Integration
==================================================

This guide helps you build llama.cpp from source and integrate it with the PB2S framework.
Built from the official repository: https://github.com/ggerganov/llama.cpp

Author: PB2S Framework Team
Date: 2025-01-23
License: Apache-2.0
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path

class LlamaCPPSetupGuide:
    def __init__(self):
        self.system = platform.system()
        self.repo_path = Path("llama.cpp")
        self.build_path = self.repo_path / "build"
        
    def print_header(self, title):
        """Print a formatted header"""
        print("\n" + "="*60)
        print(f"🦙 {title}")
        print("="*60)
        
    def print_step(self, step, description):
        """Print a formatted step"""
        print(f"\n📋 Step {step}: {description}")
        print("-" * 40)
        
    def check_prerequisites(self):
        """Check if required tools are installed"""
        self.print_header("Checking Prerequisites")
        
        required_tools = {}
        
        if self.system == "Windows":
            required_tools = {
                "git": "git --version",
                "cmake": "cmake --version", 
                "MSBuild": "where msbuild",
                "Visual Studio": "where cl"
            }
        elif self.system == "Linux":
            required_tools = {
                "git": "git --version",
                "cmake": "cmake --version",
                "gcc/g++": "gcc --version",
                "make": "make --version"
            }
        elif self.system == "Darwin":  # macOS
            required_tools = {
                "git": "git --version",
                "cmake": "cmake --version",
                "clang": "clang --version",
                "make": "make --version"
            }
            
        missing_tools = []
        for tool, check_cmd in required_tools.items():
            try:
                result = subprocess.run(check_cmd.split(), 
                                     capture_output=True, 
                                     text=True, 
                                     timeout=10)
                if result.returncode == 0:
                    print(f"✅ {tool}: Available")
                else:
                    print(f"❌ {tool}: Not found")
                    missing_tools.append(tool)
            except (subprocess.TimeoutExpired, FileNotFoundError):
                print(f"❌ {tool}: Not found")
                missing_tools.append(tool)
                
        if missing_tools:
            print(f"\n⚠️  Missing tools: {', '.join(missing_tools)}")
            self.print_installation_instructions(missing_tools)
            return False
        else:
            print("\n✅ All prerequisites are satisfied!")
            return True
            
    def print_installation_instructions(self, missing_tools):
        """Print installation instructions for missing tools"""
        print("\n📥 Installation Instructions:")
        
        if self.system == "Windows":
            print("\nFor Windows:")
            if "cmake" in missing_tools:
                print("- CMake: Download from https://cmake.org/download/")
            if "MSBuild" in missing_tools or "Visual Studio" in missing_tools:
                print("- Visual Studio: Install Visual Studio 2019/2022 with C++ workload")
                print("  OR install Build Tools for Visual Studio")
                
        elif self.system == "Linux":
            print("\nFor Ubuntu/Debian:")
            print("sudo apt update")
            print("sudo apt install git cmake build-essential")
            
            print("\nFor CentOS/RHEL/Fedora:")
            print("sudo yum install git cmake gcc-c++ make")
            print("# OR for newer versions:")
            print("sudo dnf install git cmake gcc-c++ make")
            
        elif self.system == "Darwin":
            print("\nFor macOS:")
            print("# Install Xcode Command Line Tools:")
            print("xcode-select --install")
            print("\n# Install CMake via Homebrew:")
            print("brew install cmake")
            
    def show_build_instructions(self):
        """Show platform-specific build instructions"""
        self.print_header("Build Instructions")
        
        if not self.repo_path.exists():
            print("❌ llama.cpp repository not found!")
            print("Please ensure you've cloned the repository first:")
            print("git clone https://github.com/ggerganov/llama.cpp")
            return False
            
        print(f"📁 Repository found at: {self.repo_path.absolute()}")
        
        if self.system == "Windows":
            self.show_windows_build()
        elif self.system == "Linux":
            self.show_linux_build()
        elif self.system == "Darwin":
            self.show_macos_build()
            
        return True
        
    def show_windows_build(self):
        """Show Windows build instructions"""
        self.print_step(1, "Windows Build Process")
        
        print("🪟 Building llama.cpp on Windows:")
        print()
        print("# Navigate to llama.cpp directory")
        print(f"cd {self.repo_path}")
        print()
        print("# Create build directory")
        print("mkdir build")
        print("cd build")
        print()
        print("# Configure with CMake (CPU version)")
        print("cmake .. -DCMAKE_BUILD_TYPE=Release")
        print()
        print("# For CUDA support (if you have NVIDIA GPU):")
        print("# cmake .. -DCMAKE_BUILD_TYPE=Release -DLLAMA_CUBLAS=ON")
        print()
        print("# Build the project")
        print("cmake --build . --config Release")
        print()
        print("# Alternatively, if you have Visual Studio:")
        print("# Open the generated .sln file and build in Release mode")
        
    def show_linux_build(self):
        """Show Linux build instructions"""
        self.print_step(1, "Linux Build Process")
        
        print("🐧 Building llama.cpp on Linux:")
        print()
        print("# Navigate to llama.cpp directory")
        print(f"cd {self.repo_path}")
        print()
        print("# Create build directory")
        print("mkdir -p build")
        print("cd build")
        print()
        print("# Configure with CMake")
        print("cmake .. -DCMAKE_BUILD_TYPE=Release")
        print()
        print("# For CUDA support (if you have NVIDIA GPU):")
        print("# cmake .. -DCMAKE_BUILD_TYPE=Release -DLLAMA_CUBLAS=ON")
        print()
        print("# Build the project (using all CPU cores)")
        print("make -j$(nproc)")
        
    def show_macos_build(self):
        """Show macOS build instructions"""
        self.print_step(1, "macOS Build Process")
        
        print("🍎 Building llama.cpp on macOS:")
        print()
        print("# Navigate to llama.cpp directory")
        print(f"cd {self.repo_path}")
        print()
        print("# Create build directory")
        print("mkdir -p build")
        print("cd build")
        print()
        print("# Configure with CMake")
        print("cmake .. -DCMAKE_BUILD_TYPE=Release")
        print()
        print("# For Apple Silicon Metal support:")
        print("# cmake .. -DCMAKE_BUILD_TYPE=Release -DLLAMA_METAL=ON")
        print()
        print("# Build the project")
        print("make -j$(sysctl -n hw.ncpu)")
        
    def show_model_setup(self):
        """Show model download and setup instructions"""
        self.print_header("Model Setup")
        
        self.print_step(2, "Download a Model")
        
        print("🤖 You need a GGUF model file to run llama.cpp")
        print()
        print("Recommended models for PB2S (300-word vocabulary focus):")
        print()
        print("1. 📦 Small Models (good for Jetson Orin 8GB):")
        print("   - TinyLlama-1.1B-Chat-v1.0.Q4_K_M.gguf (~700MB)")
        print("   - Phi-2.Q4_K_M.gguf (~1.6GB)")
        print("   - StableLM-Zephyr-3B.Q4_K_M.gguf (~1.9GB)")
        print()
        print("2. 🔗 Download from Hugging Face:")
        print("   https://huggingface.co/TheBloke")
        print("   https://huggingface.co/microsoft/DialoGPT-medium")
        print()
        print("3. 📁 Place your model file in:")
        print(f"   {self.repo_path / 'models'} (create this directory)")
        print()
        print("Example download commands:")
        print("# Create models directory")
        print(f"mkdir -p {self.repo_path / 'models'}")
        print()
        print("# Download TinyLlama (example)")
        print("wget -O models/tinyllama-1.1b-chat-v1.0.q4_k_m.gguf \\")
        print("https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF/resolve/main/tinyllama-1.1b-chat-v1.0.q4_k_m.gguf")
        
    def show_server_setup(self):
        """Show server startup instructions"""
        self.print_header("Starting llama.cpp Server")
        
        self.print_step(3, "Run the Server")
        
        executable_name = "server.exe" if self.system == "Windows" else "server"
        server_path = self.build_path / "bin" / executable_name
        
        print(f"🚀 Starting llama.cpp server for PB2S integration:")
        print()
        print("# Basic startup command:")
        print(f"{server_path} \\")
        print("  --port 8080 \\")
        print("  --host 127.0.0.1 \\")
        print("  -m models/your_model.gguf \\")
        print("  --ctx-size 2048 \\")
        print("  --threads 4")
        print()
        print("# Optimized for PB2S (300-word responses):")
        print(f"{server_path} \\")
        print("  --port 8080 \\")
        print("  --host 127.0.0.1 \\")
        print("  -m models/tinyllama-1.1b-chat-v1.0.q4_k_m.gguf \\")
        print("  --ctx-size 1024 \\")
        print("  --threads 4 \\")
        print("  --n-predict 300 \\")
        print("  --temp 0.7 \\")
        print("  --top-p 0.9")
        print()
        print("# For Jetson Orin 8GB optimization:")
        print(f"{server_path} \\")
        print("  --port 8080 \\")
        print("  --host 127.0.0.1 \\")
        print("  -m models/tinyllama-1.1b-chat-v1.0.q4_k_m.gguf \\")
        print("  --ctx-size 512 \\")
        print("  --threads 6 \\")
        print("  --n-predict 200 \\")
        print("  --memory-f32 \\")
        print("  --mlock")
        
    def show_pb2s_integration(self):
        """Show PB2S integration instructions"""
        self.print_header("PB2S Integration")
        
        self.print_step(4, "Connect to PB2S Dashboard")
        
        print("🔗 Integrating llama.cpp with PB2S:")
        print()
        print("1. 📋 Ensure llama.cpp server is running on port 8080")
        print("2. 🚀 Start your PB2S dashboard:")
        print("   streamlit run pb2s_dashboard.py --server.port 8502")
        print()
        print("3. 🌐 Open dashboard at: http://localhost:8502")
        print("4. 🦙 You should see 'Local Model (llama.cpp)' node")
        print("5. ✅ Test connection with a simple prompt")
        print()
        print("📝 PB2S Structure Testing:")
        print("Try these prompts to test PB2S format:")
        print()
        print("• DRAFT: What is artificial intelligence?")
        print("• REFLECT on: The definition of AI")
        print("• REVISE: AI explanation for beginners")
        print("• ACT on: Implementing AI safety measures")
        print()
        print("🔧 API Endpoints available:")
        print("- http://localhost:8080/v1/chat/completions (OpenAI compatible)")
        print("- http://localhost:8080/completion (llama.cpp native)")
        print("- http://localhost:8080/health (health check)")
        
    def show_troubleshooting(self):
        """Show troubleshooting guide"""
        self.print_header("Troubleshooting")
        
        print("🔧 Common Issues and Solutions:")
        print()
        print("1. ❌ Build fails with 'CMake not found':")
        print("   → Install CMake and ensure it's in your PATH")
        print()
        print("2. ❌ 'CUDA not found' (if trying CUDA build):")
        print("   → Install CUDA Toolkit from NVIDIA")
        print("   → Or build CPU version without -DLLAMA_CUBLAS=ON")
        print()
        print("3. ❌ Server won't start:")
        print("   → Check if port 8080 is already in use")
        print("   → Try different port: --port 8081")
        print("   → Verify model file exists and is valid GGUF format")
        print()
        print("4. ❌ PB2S dashboard shows 'offline':")
        print("   → Ensure server is running on correct port")
        print("   → Check firewall settings")
        print("   → Verify llama_cpp_connector.py is in same directory")
        print()
        print("5. ❌ Out of memory errors:")
        print("   → Use smaller model (Q4_K_M or Q5_K_M quantization)")
        print("   → Reduce --ctx-size parameter")
        print("   → For Jetson: add --memory-f32 and --mlock flags")
        print()
        print("6. ❌ Slow responses:")
        print("   → Adjust --threads parameter (try CPU core count)")
        print("   → Use hardware acceleration (CUDA/Metal if available)")
        print("   → Reduce --n-predict for shorter responses")
        
    def run_complete_guide(self):
        """Run the complete setup guide"""
        self.print_header("llama.cpp Build & Setup Guide for PB2S")
        
        print("🦙 Welcome to the llama.cpp build and integration guide!")
        print("This will help you build llama.cpp from source and integrate it with PB2S.")
        print()
        print(f"📍 Detected system: {self.system}")
        print(f"📁 Working directory: {os.getcwd()}")
        
        # Check prerequisites
        if not self.check_prerequisites():
            print("\n⚠️  Please install missing prerequisites before continuing.")
            return False
            
        # Show build instructions
        self.show_build_instructions()
        
        # Show model setup
        self.show_model_setup()
        
        # Show server setup
        self.show_server_setup()
        
        # Show PB2S integration
        self.show_pb2s_integration()
        
        # Show troubleshooting
        self.show_troubleshooting()
        
        print("\n" + "="*60)
        print("🎉 Setup guide complete!")
        print("Follow the steps above to build and integrate llama.cpp with PB2S.")
        print("For questions, check the troubleshooting section.")
        print("="*60)
        
        return True

def main():
    """Main function to run the setup guide"""
    if len(sys.argv) > 1 and sys.argv[1] in ["-h", "--help"]:
        print("llama.cpp Setup Guide for PB2S")
        print("Usage: python setup_llama_cpp_guide.py")
        print()
        print("This script provides a comprehensive guide for:")
        print("- Building llama.cpp from source")
        print("- Setting up models")
        print("- Integrating with PB2S framework")
        print("- Troubleshooting common issues")
        return
        
    guide = LlamaCPPSetupGuide()
    guide.run_complete_guide()

if __name__ == "__main__":
    main()