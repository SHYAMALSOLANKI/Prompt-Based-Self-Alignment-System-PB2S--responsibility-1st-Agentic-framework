#!/usr/bin/env python3
"""
KoboldAI CPP Integration for PB2S Dashboard
Connects to KoboldAI CPP 1.98.1 running locally while maintaining PB2S structure
"""

import requests
import json
import time
from typing import Dict, Optional, List

class KoboldAICPPConnector:
    """Connector for KoboldAI CPP with PB2S structure integration"""
    
    def __init__(self, kobold_url: str = "http://localhost:5001"):
        self.kobold_url = kobold_url
        self.session = requests.Session()
        self.pb2s_prompt_template = self.create_pb2s_template()
        
    def create_pb2s_template(self) -> str:
        """Create PB2S instruction template for KoboldAI"""
        return """You are a PB2S (Prompt-Based Self-Alignment System) AI. Follow this exact structure for ALL responses:

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

Remember: Always use this DRAFT→REFLECT→REVISE→LEARNED structure. Be thorough but concise."""

    def check_connection(self) -> Dict[str, any]:
        """Check if KoboldAI CPP is running and accessible"""
        try:
            response = self.session.get(f"{self.kobold_url}/api/v1/info", timeout=5)
            if response.status_code == 200:
                info = response.json()
                return {
                    "status": "online",
                    "model": info.get("result", {}).get("model", "Unknown"),
                    "version": info.get("result", {}).get("version", "Unknown"),
                    "url": self.kobold_url
                }
            else:
                return {"status": "error", "message": f"HTTP {response.status_code}"}
        except requests.exceptions.ConnectionError:
            return {"status": "offline", "message": "KoboldAI CPP not running"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def generate_pb2s_response(self, user_message: str, max_length: int = 512) -> Dict[str, any]:
        """Generate PB2S structured response using KoboldAI CPP"""
        
        # Create full prompt with PB2S template
        full_prompt = f"{self.pb2s_prompt_template}\n\nUser: {user_message}\n\nAssistant: "
        
        # KoboldAI CPP generation parameters
        generation_params = {
            "prompt": full_prompt,
            "max_context_length": 2048,
            "max_length": max_length,
            "temperature": 0.7,
            "top_p": 0.9,
            "top_k": 40,
            "rep_pen": 1.1,
            "rep_pen_range": 1024,
            "stop_sequence": ["User:", "Human:", "\n\nUser", "\n\nHuman"]
        }
        
        try:
            response = self.session.post(
                f"{self.kobold_url}/api/v1/generate",
                json=generation_params,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                generated_text = result.get("results", [{}])[0].get("text", "")
                
                # Parse PB2S structure from generated text
                parsed_response = self.parse_pb2s_response(generated_text)
                
                return {
                    "success": True,
                    "response": parsed_response,
                    "raw_text": generated_text,
                    "model_info": "KoboldAI CPP Local Model"
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
        """Create fallback PB2S response if KoboldAI fails"""
        return {
            "draft": f"Local model analysis of: {user_message}",
            "reflect": "- Connection to local model failed\n- Using fallback reasoning\n- Response quality may be limited",
            "revise": f"Unable to process '{user_message}' with local model. Please ensure KoboldAI CPP is running on {self.kobold_url} and try again.",
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

    def get_model_info(self) -> Dict[str, any]:
        """Get detailed information about the loaded model"""
        try:
            response = self.session.get(f"{self.kobold_url}/api/v1/model", timeout=5)
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"Failed to get model info: HTTP {response.status_code}"}
        except Exception as e:
            return {"error": str(e)}

# Demo/Test function
def test_kobold_connection():
    """Test KoboldAI CPP connection and PB2S integration"""
    print("🤖 Testing KoboldAI CPP Connection for PB2S Integration")
    print("=" * 60)
    
    # Initialize connector
    kobold = KoboldAICPPConnector()
    
    # Check connection
    status = kobold.check_connection()
    print(f"Connection Status: {status}")
    
    if status["status"] == "online":
        print(f"✅ KoboldAI CPP is running!")
        print(f"Model: {status.get('model', 'Unknown')}")
        print(f"Version: {status.get('version', 'Unknown')}")
        
        # Test generation
        print("\n🧠 Testing PB2S Generation...")
        test_message = "What is artificial intelligence?"
        result = kobold.generate_pb2s_response(test_message)
        
        if result["success"]:
            print("✅ Generation successful!")
            formatted_response = kobold.format_pb2s_response(result["response"])
            print("\n📋 PB2S Response:")
            print(formatted_response)
        else:
            print(f"❌ Generation failed: {result['error']}")
            if "fallback" in result:
                print("\n🔄 Fallback Response:")
                formatted_fallback = kobold.format_pb2s_response(result["fallback"])
                print(formatted_fallback)
    else:
        print(f"❌ KoboldAI CPP not accessible: {status.get('message', 'Unknown error')}")
        print("\n💡 To fix this:")
        print("1. Download KoboldAI CPP 1.98.1")
        print("2. Load a model (GGML/GGUF format recommended)")
        print("3. Start server: ./koboldcpp --port 5001 your_model.gguf")
        print("4. Verify it's running at http://localhost:5001")

if __name__ == "__main__":
    test_kobold_connection()