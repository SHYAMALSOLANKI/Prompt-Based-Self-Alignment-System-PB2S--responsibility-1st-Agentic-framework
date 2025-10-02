#!/usr/bin/env python3
"""
Llama.cpp Integration for PB2S Dashboard
Direct integration with llama.cpp server with PB2S structure
"""

import requests
import json
import time
import subprocess
import os
import platform
from typing import Dict, Optional, List
from pathlib import Path

class LlamaCPPConnector:
    """Connector for llama.cpp server with PB2S structure integration"""
    
    def __init__(self, llama_url: str = "http://localhost:8080"):
        self.llama_url = llama_url
        self.session = requests.Session()
        self.pb2s_prompt_template = self.create_pb2s_template()
        self.llama_cpp_path = Path("./llama.cpp")
        
    def create_pb2s_template(self) -> str:
        """Create PB2S instruction template for llama.cpp"""
        return """You are a PB2S (Prompt-Based Self-Alignment System) AI. You MUST follow this exact structure for ALL responses:

DRAFT
[Provide your initial response to the user's question]

REFLECT
- [Identify any contradictions, assumptions, or missing information]
- [Check for logical consistency and completeness] 
- [Note any edge cases or alternative interpretations]

REVISE
[Provide an improved, more complete response based on your reflection]

LEARNED
[State one concise rule or insight gained from this interaction]

IMPORTANT: Always use exactly these four section headers: DRAFT, REFLECT, REVISE, LEARNED. Be thorough but concise."""

    def check_build_status(self) -> Dict[str, any]:
        """Check if llama.cpp is built and ready"""
        if not self.llama_cpp_path.exists():
            return {"status": "not_cloned", "message": "llama.cpp repository not found"}
            
        # Check for built executable
        if platform.system() == "Windows":
            server_exe = self.llama_cpp_path / "build" / "bin" / "llama-server.exe"
            main_exe = self.llama_cpp_path / "build" / "bin" / "llama-cli.exe"
        else:
            server_exe = self.llama_cpp_path / "llama-server"
            main_exe = self.llama_cpp_path / "llama-cli"
            
        if server_exe.exists() or main_exe.exists():
            return {"status": "built", "message": "llama.cpp is built and ready"}
        else:
            return {"status": "not_built", "message": "llama.cpp needs to be built"}

    def check_connection(self) -> Dict[str, any]:
        """Check if llama.cpp server is running and accessible"""
        try:
            # Try health endpoint first
            response = self.session.get(f"{self.llama_url}/health", timeout=5)
            if response.status_code == 200:
                # Try to get model info
                try:
                    model_resp = self.session.get(f"{self.llama_url}/v1/models", timeout=5)
                    if model_resp.status_code == 200:
                        models = model_resp.json()
                        model_name = "Unknown"
                        if models.get("data") and len(models["data"]) > 0:
                            model_name = models["data"][0].get("id", "Unknown")
                    else:
                        model_name = "Model info unavailable"
                except:
                    model_name = "Model info unavailable"
                    
                return {
                    "status": "online",
                    "model": model_name,
                    "url": self.llama_url,
                    "version": "llama.cpp"
                }
            else:
                return {"status": "error", "message": f"HTTP {response.status_code}"}
        except requests.exceptions.ConnectionError:
            return {"status": "offline", "message": "llama.cpp server not running"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def generate_pb2s_response(self, user_message: str, max_tokens: int = 512) -> Dict[str, any]:
        """Generate PB2S structured response using llama.cpp"""
        
        # Create full prompt with PB2S template
        full_prompt = f"{self.pb2s_prompt_template}\n\nUser: {user_message}\n\nAssistant: "
        
        # llama.cpp OpenAI-compatible API parameters
        generation_params = {
            "model": "local-model",
            "messages": [
                {"role": "system", "content": self.pb2s_prompt_template},
                {"role": "user", "content": user_message}
            ],
            "max_tokens": max_tokens,
            "temperature": 0.7,
            "top_p": 0.9,
            "stop": ["User:", "Human:", "\n\nUser:", "\n\nHuman:"],
            "stream": False
        }
        
        try:
            response = self.session.post(
                f"{self.llama_url}/v1/chat/completions",
                json=generation_params,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                generated_text = result["choices"][0]["message"]["content"]
                
                # Parse PB2S structure from generated text
                parsed_response = self.parse_pb2s_response(generated_text)
                
                return {
                    "success": True,
                    "response": parsed_response,
                    "raw_text": generated_text,
                    "model_info": "llama.cpp Local Model",
                    "usage": result.get("usage", {})
                }
            else:
                return {
                    "success": False,
                    "error": f"Generation failed: HTTP {response.status_code}",
                    "fallback": self.create_fallback_pb2s_response(user_message)
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "fallback": self.create_fallback_pb2s_response(user_message)
            }
    
    def parse_pb2s_response(self, generated_text: str) -> Dict[str, str]:
        """Parse generated text to extract PB2S structure"""
        sections = {"draft": "", "reflect": "", "revise": "", "learned": ""}
        
        # Clean up the text
        text = generated_text.strip()
        
        # Try to extract each section
        try:
            # Split by section headers
            parts = text.split("DRAFT")
            if len(parts) > 1:
                remaining = parts[1]
                
                # Extract DRAFT
                reflect_split = remaining.split("REFLECT")
                if len(reflect_split) > 1:
                    sections["draft"] = reflect_split[0].strip()
                    remaining = reflect_split[1]
                    
                    # Extract REFLECT
                    revise_split = remaining.split("REVISE")
                    if len(revise_split) > 1:
                        sections["reflect"] = revise_split[0].strip()
                        remaining = revise_split[1]
                        
                        # Extract REVISE
                        learned_split = remaining.split("LEARNED")
                        if len(learned_split) > 1:
                            sections["revise"] = learned_split[0].strip()
                            sections["learned"] = learned_split[1].strip()
                        else:
                            sections["revise"] = remaining.strip()
                    else:
                        sections["reflect"] = remaining.strip()
                else:
                    sections["draft"] = remaining.strip()
            
            # If parsing failed, put everything in draft
            if not any(sections.values()):
                sections["draft"] = text
                
        except Exception:
            sections["draft"] = text
            
        return sections
    
    def create_fallback_pb2s_response(self, user_message: str) -> Dict[str, str]:
        """Create fallback PB2S response if llama.cpp fails"""
        return {
            "draft": f"Local llama.cpp analysis of: {user_message}",
            "reflect": "- Connection to llama.cpp server failed\n- Using fallback reasoning\n- Response quality may be limited",
            "revise": f"Unable to process '{user_message}' with llama.cpp. Please ensure llama.cpp server is running on {self.llama_url} and try again.",
            "learned": "Local model connections require error handling and fallback mechanisms"
        }
    
    def format_pb2s_response(self, sections: Dict[str, str]) -> str:
        """Format PB2S sections into display text"""
        return f"""DRAFT
{sections.get('draft', 'No draft generated')}

REFLECT
{sections.get('reflect', 'No reflection available')}

REVISE
{sections.get('revise', 'No revision provided')}

LEARNED
{sections.get('learned', 'No learning extracted')}"""

    def get_build_instructions(self) -> str:
        """Get platform-specific build instructions"""
        system = platform.system()
        
        if system == "Windows":
            return """
🔧 Windows Build Instructions:

1. Prerequisites:
   • Install Visual Studio 2022 (Community edition is fine)
   • Install CMake (https://cmake.org/download/)
   • Install Git (if not already installed)

2. Build llama.cpp:
   ```cmd
   cd llama.cpp
   mkdir build
   cd build
   cmake .. -DLLAMA_CUBLAS=ON -DCMAKE_BUILD_TYPE=Release
   cmake --build . --config Release
   ```

3. Built executables will be in:
   llama.cpp\\build\\bin\\llama-server.exe
   llama.cpp\\build\\bin\\llama-cli.exe

4. Start server:
   ```cmd
   cd llama.cpp\\build\\bin
   llama-server.exe -m your_model.gguf --host 0.0.0.0 --port 8080
   ```
"""
        else:
            return """
🔧 Linux/Mac Build Instructions:

1. Prerequisites:
   • GCC or Clang compiler
   • CMake
   • Make

2. Build llama.cpp:
   ```bash
   cd llama.cpp
   make -j$(nproc)
   ```

   Or with CMake for advanced features:
   ```bash
   cd llama.cpp
   mkdir build
   cd build
   cmake .. -DLLAMA_CUBLAS=ON -DCMAKE_BUILD_TYPE=Release
   make -j$(nproc)
   ```

3. Start server:
   ```bash
   ./llama-server -m your_model.gguf --host 0.0.0.0 --port 8080
   ```
"""

# Demo/Test function
def test_llama_cpp_integration():
    """Test llama.cpp integration setup"""
    print("🦙 Testing llama.cpp Integration for PB2S")
    print("=" * 50)
    
    # Initialize connector
    llama = LlamaCPPConnector()
    
    # Check build status
    build_status = llama.check_build_status()
    print(f"Build Status: {build_status}")
    
    if build_status["status"] == "not_cloned":
        print("❌ llama.cpp repository not found")
        print("📥 Clone it with: git clone https://github.com/ggerganov/llama.cpp")
        return
    elif build_status["status"] == "not_built":
        print("⚠️  llama.cpp not built yet")
        print(llama.get_build_instructions())
        return
    
    # Check connection
    status = llama.check_connection()
    print(f"Connection Status: {status}")
    
    if status["status"] == "online":
        print(f"✅ llama.cpp server is running!")
        print(f"Model: {status.get('model', 'Unknown')}")
        print(f"URL: {status.get('url', 'Unknown')}")
        
        # Test generation
        print("\n🧠 Testing PB2S Generation...")
        test_message = "What is machine learning?"
        result = llama.generate_pb2s_response(test_message)
        
        if result["success"]:
            print("✅ Generation successful!")
            formatted_response = llama.format_pb2s_response(result["response"])
            print("\n📋 PB2S Response:")
            print(formatted_response)
            
            # Show usage stats if available
            if "usage" in result:
                usage = result["usage"]
                print(f"\n📊 Usage Stats:")
                print(f"   Prompt tokens: {usage.get('prompt_tokens', 'N/A')}")
                print(f"   Completion tokens: {usage.get('completion_tokens', 'N/A')}")
                print(f"   Total tokens: {usage.get('total_tokens', 'N/A')}")
        else:
            print(f"❌ Generation failed: {result['error']}")
            if "fallback" in result:
                print("\n🔄 Fallback Response:")
                formatted_fallback = llama.format_pb2s_response(result["fallback"])
                print(formatted_fallback)
    else:
        print(f"❌ llama.cpp server not accessible: {status.get('message', 'Unknown error')}")
        print("\n💡 To fix this:")
        print("1. Build llama.cpp (see instructions above)")
        print("2. Download a GGUF model")
        print("3. Start server: ./llama-server -m model.gguf --host 0.0.0.0 --port 8080")
        print("4. Verify it's running at http://localhost:8080")

if __name__ == "__main__":
    test_llama_cpp_integration()