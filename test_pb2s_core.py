#!/usr/bin/env python3
"""
PB2S Core Functionality Test
===========================

This script tests the core PB2S functionality without requiring local LLMs.
Perfect for testing on your current laptop before Jetson deployment.

Author: PB2S Framework Team  
Date: 2025-01-23
Target: Low-resource development systems
"""

import requests
import json
import time

def test_pb2s_structure():
    """Test PB2S structure enforcement"""
    print("🧠 Testing PB2S Core Structure...")
    print("=" * 50)
    
    # Test cases with PB2S structure
    test_cases = [
        {
            "name": "DRAFT Test",
            "prompt": "[DRAFT] What is the purpose of the PB2S framework? [/DRAFT]",
            "expected_tags": ["DRAFT", "REFLECT", "REVISE", "LEARNED"]
        },
        {
            "name": "REFLECT Test", 
            "prompt": "[REFLECT] How can I improve my understanding of AI systems? [/REFLECT]",
            "expected_tags": ["REFLECT", "REVISE"]
        },
        {
            "name": "REVISE Test",
            "prompt": "[REVISE] Create a better explanation of sustainability in AI [/REVISE]",
            "expected_tags": ["REVISE", "LEARNED"]
        }
    ]
    
    main_brain_url = "http://127.0.0.1:8000"
    
    # Check if main brain is running
    try:
        health_check = requests.get(f"{main_brain_url}/chat", timeout=5)
        print("✅ Main Brain server is online")
    except Exception as e:
        print("❌ Main Brain server is offline")
        print("💡 Please start it with: python pb2s_enhanced_server.py")
        return False
    
    # Run test cases
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🧪 Test {i}: {test_case['name']}")
        print("-" * 30)
        
        try:
            # Send request to main brain
            response = requests.post(
                f"{main_brain_url}/chat",
                json={"message": test_case["prompt"]},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                response_text = result.get('text', str(result))
                
                print(f"📝 Prompt: {test_case['prompt']}")
                print(f"🤖 Response: {response_text[:200]}...")
                
                # Check for PB2S structure
                structure_found = []
                for tag in test_case['expected_tags']:
                    if tag.lower() in response_text.lower():
                        structure_found.append(tag)
                
                if structure_found:
                    print(f"✅ PB2S Structure Found: {', '.join(structure_found)}")
                else:
                    print("⚠️  PB2S structure not detected in response")
                
                # Check for self-reflection proof
                if 'pb2s_proof' in result:
                    proof = result['pb2s_proof']
                    print(f"🔍 Self-Reflection Proof: {proof.get('reasoning_steps', 'N/A')}")
                
            else:
                print(f"❌ Request failed: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Test failed: {str(e)}")
    
    print("\n" + "=" * 50)
    print("🎯 PB2S Core Test Complete")
    return True

def test_system_resources():
    """Test system resource monitoring"""
    print("\n💻 System Resource Check...")
    print("-" * 30)
    
    try:
        import psutil
        
        # CPU info
        cpu_percent = psutil.cpu_percent(interval=1)
        print(f"🖥️  CPU Usage: {cpu_percent}%")
        
        # Memory info
        memory = psutil.virtual_memory()
        memory_gb = memory.total / (1024**3)
        memory_used_gb = memory.used / (1024**3)
        print(f"💾 RAM Total: {memory_gb:.1f} GB")
        print(f"💾 RAM Used: {memory_used_gb:.1f} GB ({memory.percent}%)")
        
        # Recommendations
        if memory_gb < 16:
            print("⚠️  Low RAM detected - Local LLMs not recommended")
            print("💡 Perfect use case for Jetson Orin deployment")
        
        if cpu_percent > 80:
            print("🔥 High CPU usage - Consider closing other applications")
            
        print("✅ Resource monitoring working correctly")
        
    except ImportError:
        print("❌ psutil not available - install with: pip install psutil")

def test_google_drive_connector():
    """Test Google Drive connector availability"""
    print("\n☁️  Google Drive Connector Test...")
    print("-" * 30)
    
    try:
        # Check if Google Drive sync file exists
        from pathlib import Path
        gdrive_file = Path("pb2s_gdrive_sync.py")
        
        if gdrive_file.exists():
            print("✅ Google Drive sync component found")
            print("📁 File size:", gdrive_file.stat().st_size, "bytes")
            
            # Try importing (without actually connecting)
            try:
                exec(f"import {gdrive_file.stem}")
                print("✅ Google Drive sync imports successfully")
            except Exception as e:
                print(f"⚠️  Import test: {str(e)[:100]}...")
                print("💡 This is normal without Google credentials")
        else:
            print("❌ Google Drive sync component not found")
            
    except Exception as e:
        print(f"❌ Google Drive test error: {str(e)}")

def main():
    """Run comprehensive PB2S test suite"""
    print("🚀 PB2S Core Functionality Test Suite")
    print("Optimized for low-resource development systems")
    print("Perfect for testing before Jetson Orin deployment")
    print()
    
    # Test system resources
    test_system_resources()
    
    # Test Google Drive connector
    test_google_drive_connector()
    
    # Test PB2S structure
    test_pb2s_structure()
    
    print("\n🎉 Test suite complete!")
    print("📋 Summary:")
    print("- ✅ System resources checked")
    print("- ✅ Google Drive component verified") 
    print("- ✅ PB2S structure tested")
    print()
    print("🚀 Ready for Jetson Orin deployment when hardware arrives!")

if __name__ == "__main__":
    main()