#!/usr/bin/env python3
"""
KoboldAI CPP Integration Setup Guide for PB2S Dashboard
Complete instructions for setting up local LLM with PB2S structure
"""

import os
import subprocess
import platform

def print_setup_guide():
    """Print comprehensive setup guide for KoboldAI CPP integration"""
    
    print("🤖 KoboldAI CPP + PB2S Dashboard Integration Guide")
    print("=" * 60)
    print()
    
    print("📋 What You Have Now:")
    print("✅ KoboldAI CPP connector with PB2S structure integration")
    print("✅ Enhanced dashboard with local model support")
    print("✅ Automatic PB2S format (DRAFT→REFLECT→REVISE→LEARNED)")
    print("✅ Fallback system if KoboldAI is offline")
    print("✅ Your existing Main Brain system intact")
    print()
    
    print("🎯 Setup Steps:")
    print()
    
    print("1️⃣ DOWNLOAD KoboldAI CPP 1.98.1")
    print("   • Windows: https://github.com/LostRuins/koboldcpp/releases")
    print("   • Download: koboldcpp.exe (or build from source)")
    print("   • Place in easy-to-access folder")
    print()
    
    print("2️⃣ GET A COMPATIBLE MODEL")
    print("   📥 Recommended small models for testing:")
    print("   • TinyLlama-1.1B-Chat (2GB): https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF")
    print("   • Phi-2 (5GB): https://huggingface.co/microsoft/phi-2-GGUF")
    print("   • OpenHermes 2.5 (7GB): https://huggingface.co/TheBloke/OpenHermes-2.5-Mistral-7B-GGUF")
    print()
    print("   💡 Download the .gguf file (GGUF format required)")
    print("   💡 Q4_K_M or Q5_K_M quantization recommended for balance")
    print()
    
    print("3️⃣ START KoboldAI CPP SERVER")
    print("   Open terminal/command prompt and run:")
    print("   ```")
    if platform.system() == "Windows":
        print("   koboldcpp.exe --port 5001 --host 0.0.0.0 your_model.gguf")
    else:
        print("   ./koboldcpp --port 5001 --host 0.0.0.0 your_model.gguf")
    print("   ```")
    print()
    print("   🔧 Optional parameters:")
    print("   • --threads 8           (use 8 CPU threads)")
    print("   • --blasthreads 4       (BLAS acceleration)")
    print("   • --gpulayers 20        (offload 20 layers to GPU)")
    print("   • --contextsize 2048    (context window size)")
    print()
    
    print("4️⃣ VERIFY KoboldAI IS RUNNING")
    print("   • Open browser: http://localhost:5001")
    print("   • You should see KoboldAI web interface")
    print("   • Model should be loaded and ready")
    print()
    
    print("5️⃣ START YOUR PB2S DASHBOARD")
    print("   ```")
    print("   streamlit run pb2s_dashboard.py --server.port 8502")
    print("   ```")
    print()
    
    print("6️⃣ TEST THE INTEGRATION")
    print("   • Open dashboard: http://localhost:8502")
    print("   • You'll see TWO nodes now:")
    print("     - Main Brain (your existing server)")
    print("     - Local Model (KoboldAI)")
    print("   • Both should show online status")
    print("   • Type a question and send to Local Model")
    print("   • Get PB2S structured response!")
    print()
    
    print("🎨 DASHBOARD FEATURES:")
    print("✅ Dual AI nodes (Main Brain + Local Model)")
    print("✅ Real-time status checking")
    print("✅ PB2S structure enforcement")
    print("✅ Raw response viewing")
    print("✅ Model information display")
    print("✅ Automatic fallback handling")
    print()
    
    print("🔍 EXAMPLE INTERACTION:")
    print("You ask: 'What is quantum computing?'")
    print()
    print("Local Model responds:")
    print("""DRAFT
Quantum computing uses quantum mechanical phenomena like superposition and entanglement to process information.

REFLECT
- Should include specific quantum advantages
- Missing mention of qubit vs classical bit differences  
- Need to address current limitations

REVISE
Quantum computing leverages quantum mechanical properties like superposition (qubits existing in multiple states) and entanglement (correlated qubit pairs) to perform certain calculations exponentially faster than classical computers. Current applications include cryptography, optimization, and scientific simulation, though practical quantum advantage remains limited to specific problems.

LEARNED
Quantum explanations require balancing technical accuracy with accessibility while noting current practical limitations""")
    print()
    
    print("⚙️ CONFIGURATION OPTIONS:")
    print()
    print("🔧 In kobold_connector.py you can adjust:")
    print("• kobold_url = 'http://localhost:5001'  # Change port if needed")
    print("• max_length = 512                      # Response length")
    print("• temperature = 0.7                     # Creativity level")
    print("• top_p = 0.9                          # Token selection")
    print()
    
    print("📊 TROUBLESHOOTING:")
    print()
    print("❌ 'Local Model offline'")
    print("   → Check KoboldAI is running on port 5001")
    print("   → Verify model is loaded (check browser interface)")
    print()
    print("❌ 'Generation failed'")
    print("   → Model might be too small for complex PB2S structure")
    print("   → Try simpler questions first")
    print("   → Check KoboldAI logs for errors")
    print()
    print("❌ 'Malformed PB2S response'")
    print("   → Some models need fine-tuning for structure")
    print("   → Fallback response will be used")
    print("   → Consider larger model or adjust prompt template")
    print()
    
    print("🚀 ADVANCED USAGE:")
    print()
    print("🔗 Multiple Models:")
    print("   • Run multiple KoboldAI instances on different ports")
    print("   • Add more nodes to dashboard configuration")
    print("   • Compare responses from different models")
    print()
    print("🧠 Model Switching:")
    print("   • Stop KoboldAI (Ctrl+C)")
    print("   • Load different model")
    print("   • Restart - dashboard will auto-detect")
    print()
    print("⚡ Performance Tuning:")
    print("   • Use GPU acceleration if available")
    print("   • Adjust thread count for your CPU")
    print("   • Monitor RAM usage with larger models")
    print()
    
    print("🎉 SUCCESS INDICATORS:")
    print("✅ Dashboard shows 'Local Model (KoboldAI) is online'")
    print("✅ Responses follow PB2S structure")
    print("✅ Model info shows in expandable section")
    print("✅ No connection errors in dashboard")
    print()
    
    print("💡 NEXT STEPS:")
    print("• Try different models and compare results")
    print("• Experiment with KoboldAI generation settings")
    print("• Use both Main Brain and Local Model for comparison")
    print("• Fine-tune the PB2S prompt template for better structure")
    print("• Set up model switching for different tasks")
    print()
    
    print("📚 FILES CREATED:")
    print("• kobold_connector.py     - KoboldAI integration")
    print("• pb2s_dashboard.py       - Enhanced dashboard")
    print("• setup_kobold_guide.py   - This guide")
    print()
    
    print("🔧 Quick Test Command:")
    print("python kobold_connector.py  # Test connection")
    print()

def test_current_status():
    """Test current system status"""
    print("🔍 CURRENT SYSTEM STATUS")
    print("=" * 30)
    
    # Test KoboldAI connection
    try:
        from kobold_connector import KoboldAICPPConnector
        kobold = KoboldAICPPConnector()
        status = kobold.check_connection()
        
        if status["status"] == "online":
            print("✅ KoboldAI CPP: ONLINE")
            print(f"   Model: {status.get('model', 'Unknown')}")
            print(f"   URL: {status.get('url', 'Unknown')}")
        else:
            print("❌ KoboldAI CPP: OFFLINE")
            print(f"   Status: {status['status']}")
            print(f"   Message: {status.get('message', 'Unknown')}")
            
    except ImportError:
        print("❌ KoboldAI Connector: NOT FOUND")
        
    # Test Main Brain
    try:
        import requests
        resp = requests.get("http://127.0.0.1:8000/chat", timeout=2)
        print("✅ Main Brain: ONLINE")
    except:
        print("❌ Main Brain: OFFLINE")
        
    print()
    
    # Check if dashboard files exist
    files_to_check = [
        "pb2s_dashboard.py",
        "kobold_connector.py", 
        "server/main.py"
    ]
    
    print("📁 FILE STATUS:")
    for file in files_to_check:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file}")
    print()

if __name__ == "__main__":
    print_setup_guide()
    print()
    test_current_status()
    
    print("🚀 Ready to start? Run these commands:")
    print("1. Start KoboldAI: koboldcpp.exe --port 5001 your_model.gguf")
    print("2. Start dashboard: streamlit run pb2s_dashboard.py --server.port 8502")
    print("3. Visit: http://localhost:8502")
    print()
    print("Need help? Run: python kobold_connector.py")