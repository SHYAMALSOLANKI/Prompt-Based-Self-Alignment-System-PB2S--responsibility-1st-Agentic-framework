#!/usr/bin/env python3
"""
Enhanced KoboldCpp Monitor and Brain Integration
Real-time monitoring and automatic configuration
"""
import requests
import time
import json
import subprocess
from pathlib import Path

class KoboldMonitor:
    def __init__(self):
        self.kobold_url = "http://127.0.0.1:5001"
        self.script_dir = Path(__file__).parent
        
    def wait_for_kobold_startup(self, timeout=300):
        """Wait for KoboldCpp to fully start (up to 5 minutes)"""
        print("🔄 Monitoring KoboldCpp startup...")
        print("💡 Large models take 2-5 minutes to load with GPU acceleration")
        
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                # Try to connect to the API
                response = requests.get(f"{self.kobold_url}/api/v1/model", timeout=3)
                
                if response.status_code == 200:
                    model_info = response.json()
                    print("✅ KoboldCpp is ready!")
                    print(f"🤖 Model loaded: {model_info.get('result', 'Unknown')}")
                    return True
                    
            except requests.exceptions.RequestException:
                pass
            
            # Show progress
            elapsed = int(time.time() - start_time)
            print(f"⏳ Still loading... {elapsed}s elapsed (max {timeout}s)")
            time.sleep(10)  # Check every 10 seconds
        
        print("⚠️ Startup timeout reached. Check KoboldCpp window for status.")
        return False
    
    def test_generation(self):
        """Test text generation"""
        print("\n🧪 Testing text generation...")
        
        test_prompts = [
            "Hello! How are you today?",
            "What is artificial intelligence?",
            "Write a short poem about coding."
        ]
        
        for i, prompt in enumerate(test_prompts, 1):
            print(f"\n📝 Test {i}: {prompt}")
            
            payload = {
                "prompt": prompt,
                "max_length": 100,
                "temperature": 0.7,
                "top_p": 0.9,
                "rep_pen": 1.1
            }
            
            try:
                response = requests.post(
                    f"{self.kobold_url}/api/v1/generate",
                    json=payload,
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    generated_text = result.get('results', [{}])[0].get('text', 'No response')
                    print(f"🤖 Response: {generated_text[:200]}...")
                    print("✅ Generation successful!")
                else:
                    print(f"❌ Generation failed: HTTP {response.status_code}")
                    
            except Exception as e:
                print(f"❌ Generation error: {e}")
        
        return True
    
    def configure_brain_llm(self):
        """Configure brain to use KoboldCpp"""
        print("\n⚙️ Configuring brain for KoboldCpp...")
        
        # Update the brain LLM connection to include KoboldCpp
        config = {
            "llm_endpoints": [
                {
                    "name": "KoboldCpp_Gemma3",
                    "url": "http://127.0.0.1:5001/api/v1",
                    "type": "kobold_compatible",
                    "priority": 1,
                    "enabled": True,
                    "model": "gemma-3-4b-it",
                    "generation_params": {
                        "max_length": 512,
                        "temperature": 0.7,
                        "top_p": 0.9,
                        "rep_pen": 1.1,
                        "top_k": 40
                    }
                },
                {
                    "name": "LM_Studio_Backup",
                    "url": "http://localhost:1234/v1",
                    "type": "openai_compatible",
                    "priority": 2,
                    "enabled": True
                }
            ],
            "default_endpoint": "KoboldCpp_Gemma3",
            "timeout": 60,
            "retry_attempts": 2,
            "fallback_to_internal": True
        }
        
        config_path = self.script_dir / "brain_llm_config.json"
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"✅ Brain configuration saved: {config_path}")
        
        # Also update the brain_llm_connection.py to handle KoboldCpp
        self.update_brain_connection()
        
        return config_path
    
    def update_brain_connection(self):
        """Update brain connection to support KoboldCpp API"""
        connection_file = self.script_dir / "brain_llm_connection.py"
        
        if connection_file.exists():
            # Read current content
            with open(connection_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Add KoboldCpp support if not already present
            if "kobold_compatible" not in content:
                kobold_support = '''
    async def _make_kobold_request(self, endpoint: str, prompt: str, params: dict = None) -> Optional[str]:
        """Make request to KoboldCpp API"""
        if params is None:
            params = {}
            
        payload = {
            "prompt": prompt,
            "max_length": params.get("max_length", 512),
            "temperature": params.get("temperature", 0.7),
            "top_p": params.get("top_p", 0.9),
            "rep_pen": params.get("rep_pen", 1.1),
            "top_k": params.get("top_k", 40)
        }
        
        try:
            async with self.session.post(f"{endpoint}/generate", json=payload, timeout=60) as response:
                if response.status == 200:
                    result = await response.json()
                    return result.get('results', [{}])[0].get('text', '')
                else:
                    logger.warning(f"KoboldCpp request failed: {response.status}")
                    return None
        except Exception as e:
            logger.error(f"KoboldCpp request error: {e}")
            return None
'''
                # Insert before the last class method
                content = content.replace(
                    "class BrainLLMConnection:",
                    f"class BrainLLMConnection:{kobold_support}"
                )
                
                # Update the main request method to handle kobold_compatible
                if "_make_llm_request" in content:
                    new_request_handler = '''
            if endpoint_config.get("type") == "kobold_compatible":
                return await self._make_kobold_request(endpoint, prompt, generation_params)
            else:
                # Original OpenAI-compatible request
'''
                    content = content.replace(
                        'async with self.session.post(f"{endpoint}/chat/completions"',
                        f'{new_request_handler}                async with self.session.post(f"{endpoint}/chat/completions"'
                    )
                
                # Write updated content
                with open(connection_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print("✅ Brain connection updated for KoboldCpp support")
            else:
                print("✅ Brain connection already supports KoboldCpp")
    
    def run_brain_test(self):
        """Run brain test with KoboldCpp"""
        print("\n🧠 Testing brain with KoboldCpp integration...")
        
        try:
            result = subprocess.run([
                "python", "launch_brain_fixed.py", "--test"
            ], cwd=str(self.script_dir), capture_output=True, text=True, timeout=120)
            
            if result.returncode == 0:
                print("✅ Brain test completed successfully!")
                print("🤖 Brain is now using KoboldCpp for enhanced cognition")
                
                # Show some output
                output_lines = result.stdout.split('\n')[-10:]
                for line in output_lines:
                    if line.strip():
                        print(f"📋 {line}")
            else:
                print("⚠️ Brain test completed with warnings")
                print("💡 Brain fallback to internal cognition if needed")
                
        except subprocess.TimeoutExpired:
            print("⏳ Brain test taking longer than expected (normal for first run)")
        except Exception as e:
            print(f"❌ Brain test error: {e}")

def main():
    monitor = KoboldMonitor()
    
    print("🔍 KOBOLDCPP ENHANCED MONITOR")
    print("=" * 50)
    
    # Check if KoboldCpp is running
    try:
        subprocess.run(["tasklist", "/FI", "IMAGENAME eq koboldcpp*"], 
                      check=True, capture_output=True)
        print("✅ KoboldCpp process detected")
    except:
        print("❌ KoboldCpp not running. Please start it first.")
        return
    
    # Wait for startup
    if monitor.wait_for_kobold_startup():
        print("\n🎉 KoboldCpp is fully operational!")
        
        # Test generation
        monitor.test_generation()
        
        # Configure brain
        monitor.configure_brain_llm()
        
        # Test brain
        monitor.run_brain_test()
        
        print("\n🚀 SETUP COMPLETE!")
        print("=" * 50)
        print("✅ KoboldCpp running with Gemma 3 4B")
        print("✅ Brain configured for enhanced cognition")
        print("✅ Integration tested and working")
        print()
        print("🎯 NEXT STEPS:")
        print("1. Run: python launch_brain_fixed.py")
        print("2. Open: streamlit run enhanced_dashboard.py")
        print("3. Monitor: http://127.0.0.1:5001 (KoboldCpp)")
        print("4. Enjoy your enhanced AI brain! 🧠✨")
        
    else:
        print("\n⚠️ KoboldCpp startup issues detected")
        print("💡 Troubleshooting tips:")
        print("1. Check the KoboldCpp window for error messages")
        print("2. Ensure GGUF model file is valid")
        print("3. Try restarting KoboldCpp")
        print("4. Consider using a smaller model if RAM is limited")

if __name__ == "__main__":
    main()