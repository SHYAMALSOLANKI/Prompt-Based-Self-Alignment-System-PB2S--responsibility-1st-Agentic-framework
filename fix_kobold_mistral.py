#!/usr/bin/env python3
"""
KoboldAI Mistral Model Setup Fix
===============================

This script helps fix common issues when loading Mistral models in KoboldAI CPP.
The main issue is that KoboldAI expects GGUF format, not the LM Studio YAML format.

Author: PB2S Framework Team
Date: 2025-01-23
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

class KoboldMistralFixer:
    def __init__(self):
        self.lm_studio_path = Path("C:/Users/UnknwN/lmstudio/hub/models")
        self.mistral_path = self.lm_studio_path / "mistralai" / "mistral-7b-instruct-v0.3"
        
    def print_header(self, title):
        """Print a formatted header"""
        print("\n" + "="*60)
        print(f"🔧 {title}")
        print("="*60)
        
    def diagnose_issue(self):
        """Diagnose the KoboldAI model loading issue"""
        self.print_header("Diagnosing KoboldAI Mistral Issue")
        
        print("🔍 Issue Analysis:")
        print("- KoboldAI CPP expects GGUF format (.gguf files)")
        print("- LM Studio uses YAML + safetensors format")
        print("- KoboldAI cannot load model.yaml files directly")
        print()
        
        print("📁 Checking your LM Studio installation:")
        if self.lm_studio_path.exists():
            print(f"✅ LM Studio path found: {self.lm_studio_path}")
            
            if self.mistral_path.exists():
                print(f"✅ Mistral model found: {self.mistral_path}")
                
                # List files in the Mistral directory
                print("\n📋 Files in Mistral directory:")
                for file in self.mistral_path.rglob("*"):
                    if file.is_file():
                        size_mb = file.stat().st_size / (1024 * 1024)
                        print(f"   {file.name} ({size_mb:.1f} MB)")
                        
            else:
                print(f"❌ Mistral model not found at: {self.mistral_path}")
        else:
            print(f"❌ LM Studio path not found: {self.lm_studio_path}")
            
    def show_solutions(self):
        """Show different solutions to fix the issue"""
        self.print_header("Solutions to Fix KoboldAI + Mistral")
        
        print("🎯 Solution 1: Download GGUF Version (RECOMMENDED)")
        print("-" * 50)
        print("1. Go to Hugging Face: https://huggingface.co/TheBloke")
        print("2. Search for 'Mistral-7B-Instruct-v0.3-GGUF'")
        print("3. Download one of these quantized versions:")
        print("   • mistral-7b-instruct-v0.3.Q4_K_M.gguf (4.37 GB)")
        print("   • mistral-7b-instruct-v0.3.Q5_K_M.gguf (5.13 GB)")
        print("   • mistral-7b-instruct-v0.3.Q8_0.gguf (7.70 GB)")
        print()
        print("4. Place the .gguf file in a models folder")
        print("5. Start KoboldAI with the .gguf file")
        print()
        
        print("🎯 Solution 2: Use LM Studio Instead")
        print("-" * 50)
        print("Since you already have the model in LM Studio:")
        print("1. Open LM Studio")
        print("2. Load the Mistral 7B Instruct model")
        print("3. Start the local server in LM Studio")
        print("4. Use our LM Studio connector instead of KoboldAI")
        print()
        
        print("🎯 Solution 3: Convert LM Studio to GGUF")
        print("-" * 50)
        print("This is more complex but possible:")
        print("1. Use llama.cpp conversion scripts")
        print("2. Convert the safetensors to GGUF format")
        print("3. This requires Python and technical knowledge")
        print()
        
    def create_lmstudio_connector(self):
        """Create an LM Studio connector for PB2S"""
        self.print_header("Creating LM Studio Connector")
        
        connector_code = '''"""
LM Studio Connector for PB2S Framework
====================================

This connector interfaces with LM Studio's local server API.
LM Studio provides an OpenAI-compatible API when running models locally.

Usage:
1. Open LM Studio
2. Load your Mistral model
3. Start the local server
4. This connector will communicate with it

Author: PB2S Framework Team
Date: 2025-01-23
"""

import requests
import json
import time
from typing import Dict, Any, Optional

class LMStudioConnector:
    def __init__(self, base_url: str = "http://localhost:1234"):
        """
        Initialize LM Studio connector
        
        Args:
            base_url: LM Studio server URL (default: http://localhost:1234)
        """
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
        
    def check_connection(self) -> Dict[str, Any]:
        """Check if LM Studio server is running and responsive"""
        try:
            # Try to get model info
            response = self.session.get(f"{self.base_url}/v1/models", timeout=5)
            
            if response.status_code == 200:
                models_data = response.json()
                if models_data.get('data'):
                    model_info = models_data['data'][0]['id']
                    return {
                        "status": "online",
                        "message": "LM Studio server is running",
                        "model": model_info
                    }
                else:
                    return {
                        "status": "no_model",
                        "message": "LM Studio server running but no model loaded"
                    }
            else:
                return {
                    "status": "error",
                    "message": f"HTTP {response.status_code}: {response.text}"
                }
                
        except requests.exceptions.ConnectionError:
            return {
                "status": "offline",
                "message": "LM Studio server not running. Please start LM Studio and load a model."
            }
        except Exception as e:
            return {
                "status": "error", 
                "message": f"Connection error: {str(e)}"
            }
            
    def generate(self, prompt: str, max_tokens: int = 300, temperature: float = 0.7) -> Optional[str]:
        """
        Generate text using LM Studio
        
        Args:
            prompt: Input prompt
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            
        Returns:
            Generated text or None if error
        """
        try:
            payload = {
                "model": "local-model",
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": max_tokens,
                "temperature": temperature,
                "stream": False
            }
            
            response = self.session.post(
                f"{self.base_url}/v1/chat/completions",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                return data['choices'][0]['message']['content']
            else:
                print(f"LM Studio API error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"LM Studio generation error: {e}")
            return None
            
    def generate_pb2s_response(self, prompt: str) -> Dict[str, Any]:
        """
        Generate a response with PB2S structure enforcement
        
        Args:
            prompt: Input prompt
            
        Returns:
            Dictionary with success status, response, and metadata
        """
        try:
            # Enhance prompt with PB2S structure
            if not any(tag in prompt.upper() for tag in ['[DRAFT]', '[REFLECT]', '[REVISE]', '[LEARNED]']):
                structured_prompt = f"[DRAFT] {prompt} [/DRAFT]"
            else:
                structured_prompt = prompt
                
            # Add PB2S instruction
            enhanced_prompt = f"""You are part of the PB2S (Prompt-Based Self-Alignment System). Please respond using the PB2S structure:
[DRAFT] - Initial response
[REFLECT] - Self-reflection on the response
[REVISE] - Improved version based on reflection
[LEARNED] - Key takeaway or lesson

User request: {structured_prompt}

Please structure your response with these tags and keep it concise (under 300 words)."""

            response_text = self.generate(enhanced_prompt, max_tokens=300, temperature=0.7)
            
            if response_text:
                return {
                    "success": True,
                    "response": response_text,
                    "raw_text": response_text,
                    "model_info": "LM Studio - Mistral 7B Instruct",
                    "timestamp": time.time()
                }
            else:
                # Fallback response
                fallback = f"""[DRAFT] I understand you want to: {prompt}
[REFLECT] I should provide a helpful response even when the model isn't fully accessible.
[REVISE] Let me give you the best guidance I can with available resources.
[LEARNED] Sometimes fallback responses are better than no response."""
                
                return {
                    "success": False,
                    "error": "LM Studio model generation failed",
                    "fallback": fallback,
                    "model_info": "LM Studio - Connection Error"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"PB2S response generation error: {str(e)}",
                "model_info": "LM Studio - Error"
            }
            
    def format_pb2s_response(self, response: str) -> str:
        """Format response to highlight PB2S structure"""
        if not response:
            return "No response generated"
            
        # Add some basic formatting for PB2S tags
        formatted = response.replace('[DRAFT]', '\\n📝 [DRAFT]')
        formatted = formatted.replace('[REFLECT]', '\\n🤔 [REFLECT]')
        formatted = formatted.replace('[REVISE]', '\\n✏️ [REVISE]')
        formatted = formatted.replace('[LEARNED]', '\\n🎓 [LEARNED]')
        
        return formatted.strip()

# Test the connector
if __name__ == "__main__":
    print("🔌 Testing LM Studio Connector...")
    
    connector = LMStudioConnector()
    status = connector.check_connection()
    
    print(f"Connection Status: {status['status']}")
    print(f"Message: {status['message']}")
    
    if status["status"] == "online":
        print(f"Model: {status.get('model', 'Unknown')}")
        
        # Test generation
        test_response = connector.generate_pb2s_response("What is artificial intelligence?")
        if test_response["success"]:
            print("\\n✅ Test Response:")
            print(connector.format_pb2s_response(test_response["response"]))
        else:
            print(f"❌ Test failed: {test_response['error']}")
    else:
        print("❌ Please start LM Studio and load a model first.")
'''
        
        # Write the connector to a file
        connector_path = Path("lmstudio_connector.py")
        with open(connector_path, 'w', encoding='utf-8') as f:
            f.write(connector_code)
            
        print(f"✅ Created LM Studio connector: {connector_path.absolute()}")
        print()
        print("📋 To use this connector:")
        print("1. Open LM Studio")
        print("2. Load your Mistral model")
        print("3. Click 'Start Server' in LM Studio")
        print("4. Run: python lmstudio_connector.py")
        
    def show_kobold_fix_commands(self):
        """Show the exact commands to fix KoboldAI"""
        self.print_header("KoboldAI Quick Fix Commands")
        
        print("🚀 Quick Solution - Download GGUF Model:")
        print()
        print("# Create models directory")
        print("mkdir models")
        print()
        print("# Download Mistral 7B GGUF (choose one):")
        print()
        print("# Option 1: 4GB version (recommended for most systems)")
        print("curl -L -o models/mistral-7b-instruct-v0.3.q4_k_m.gguf \\")
        print("https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.3-GGUF/resolve/main/mistral-7b-instruct-v0.3.q4_k_m.gguf")
        print()
        print("# Option 2: 5GB version (better quality)")
        print("curl -L -o models/mistral-7b-instruct-v0.3.q5_k_m.gguf \\")
        print("https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.3-GGUF/resolve/main/mistral-7b-instruct-v0.3.q5_k_m.gguf")
        print()
        print("# Start KoboldAI with the downloaded model:")
        print("koboldcpp --port 5001 models/mistral-7b-instruct-v0.3.q4_k_m.gguf")
        print()
        print("⚡ Alternative - Use wget (if you have it):")
        print("wget -O models/mistral-7b-instruct-v0.3.q4_k_m.gguf \\")
        print("https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.3-GGUF/resolve/main/mistral-7b-instruct-v0.3.q4_k_m.gguf")
        
    def run_complete_fix(self):
        """Run the complete diagnostic and fix process"""
        print("🔧 KoboldAI + Mistral Model Fix Tool")
        print("===================================")
        
        self.diagnose_issue()
        self.show_solutions()
        self.show_kobold_fix_commands()
        self.create_lmstudio_connector()
        
        print("\n" + "="*60)
        print("✅ Fix Complete!")
        print("Choose one of the solutions above to resolve the KoboldAI issue.")
        print("The LM Studio connector has been created as an alternative.")
        print("="*60)

def main():
    """Main function"""
    fixer = KoboldMistralFixer()
    fixer.run_complete_fix()

if __name__ == "__main__":
    main()