"""
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
        formatted = response.replace('[DRAFT]', '\n📝 [DRAFT]')
        formatted = formatted.replace('[REFLECT]', '\n🤔 [REFLECT]')
        formatted = formatted.replace('[REVISE]', '\n✏️ [REVISE]')
        formatted = formatted.replace('[LEARNED]', '\n🎓 [LEARNED]')
        
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
            print("\n✅ Test Response:")
            print(connector.format_pb2s_response(test_response["response"]))
        else:
            print(f"❌ Test failed: {test_response['error']}")
    else:
        print("❌ Please start LM Studio and load a model first.")
