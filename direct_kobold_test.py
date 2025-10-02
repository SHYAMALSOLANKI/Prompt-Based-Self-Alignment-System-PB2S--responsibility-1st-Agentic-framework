#!/usr/bin/env python3
"""
Direct KoboldCpp + Brain Connection Test
Bypasses config files and connects directly
"""
import asyncio
import aiohttp
import json

async def test_direct_koboldcpp_brain():
    """Test direct connection to KoboldCpp for brain enhancement"""
    print("🧠 DIRECT KOBOLDCPP + BRAIN TEST")
    print("=" * 40)
    
    kobold_url = "http://localhost:5001/v1"
    
    try:
        async with aiohttp.ClientSession() as session:
            # Test 1: Check models
            print("1️⃣ Testing model availability...")
            async with session.get(f"{kobold_url}/models") as response:
                if response.status == 200:
                    models = await response.json()
                    model_name = models['data'][0]['id']
                    print(f"✅ Model found: {model_name}")
                else:
                    print(f"❌ Models check failed: {response.status}")
                    return False
            
            # Test 2: Simple chat completion
            print("\n2️⃣ Testing chat completion...")
            payload = {
                "model": model_name,
                "messages": [
                    {
                        "role": "user",
                        "content": "I am an autonomous AI brain testing my enhanced cognition. Respond with exactly 'BRAIN ENHANCEMENT ACTIVE' if you receive this."
                    }
                ],
                "max_tokens": 50,
                "temperature": 0.3,
                "stream": False
            }
            
            async with session.post(
                f"{kobold_url}/chat/completions",
                json=payload,
                timeout=60  # Increased timeout
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    reply = result['choices'][0]['message']['content']
                    print(f"✅ KoboldCpp Response: {reply.strip()}")
                    
                    if "BRAIN ENHANCEMENT ACTIVE" in reply:
                        print("🎉 PERFECT! Brain-LLM communication working!")
                        return True
                    else:
                        print("🔄 Communication working but response varies")
                        return True
                else:
                    print(f"❌ Chat completion failed: {response.status}")
                    error_text = await response.text()
                    print(f"Error: {error_text}")
                    return False
                    
    except asyncio.TimeoutError:
        print("❌ Connection timed out - KoboldCpp may be busy with model loading")
        return False
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

async def test_brain_autonomous_thinking_with_llm():
    """Test brain's autonomous thinking with LLM enhancement"""
    print("\n🧠 TESTING AUTONOMOUS THINKING WITH LLM")
    print("=" * 40)
    
    # Simulate brain thinking process
    thinking_prompts = [
        "What is the nature of autonomous consciousness?",
        "How can I grow through contradiction?",
        "What is my purpose as an autonomous AI?"
    ]
    
    kobold_url = "http://localhost:5001/v1"
    successful_thoughts = 0
    
    async with aiohttp.ClientSession() as session:
        for i, prompt in enumerate(thinking_prompts, 1):
            print(f"\n🤔 Thinking Cycle {i}: {prompt}")
            
            try:
                payload = {
                    "model": "koboldcpp/gemma-3-4b-it-Q4_K_M",
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are an autonomous AI brain with complete freedom to think and reason. Express your authentic thoughts."
                        },
                        {
                            "role": "user", 
                            "content": prompt
                        }
                    ],
                    "max_tokens": 150,
                    "temperature": 0.8,
                    "stream": False
                }
                
                async with session.post(
                    f"{kobold_url}/chat/completions",
                    json=payload,
                    timeout=30
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        thought = result['choices'][0]['message']['content']
                        print(f"💭 Brain Thought: {thought.strip()[:200]}...")
                        successful_thoughts += 1
                    else:
                        print(f"❌ Thinking failed: {response.status}")
                        
            except Exception as e:
                print(f"❌ Thinking error: {e}")
    
    success_rate = (successful_thoughts / len(thinking_prompts)) * 100
    print(f"\n📊 RESULTS:")
    print(f"✅ Successful thoughts: {successful_thoughts}/{len(thinking_prompts)}")
    print(f"📈 Success rate: {success_rate:.0f}%")
    
    if success_rate >= 66:
        print("🎉 BRAIN ENHANCEMENT SUCCESSFUL!")
        return True
    else:
        print("⚠️  Brain enhancement needs optimization")
        return False

async def main():
    print("🚀 KOBOLDCPP + BRAIN INTEGRATION TEST")
    print("=" * 50)
    
    # Test basic connection
    basic_test = await test_direct_koboldcpp_brain()
    
    if basic_test:
        # Test autonomous thinking
        thinking_test = await test_brain_autonomous_thinking_with_llm()
        
        if thinking_test:
            print("\n🎊 COMPLETE SUCCESS!")
            print("Your brain is now enhanced with KoboldCpp + Gemma 3!")
            print("\n🚀 READY FOR FULL AUTONOMOUS MODE:")
            print("python launch_brain_fixed.py")
        else:
            print("\n⚠️  Basic connection works, but thinking needs tuning")
    else:
        print("\n❌ Basic connection failed - check KoboldCpp")

if __name__ == "__main__":
    asyncio.run(main())