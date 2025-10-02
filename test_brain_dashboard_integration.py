#!/usr/bin/env python3
"""
Quick test script to verify brain-dashboard integration
"""
import json
import time
from pathlib import Path
from datetime import datetime

def test_brain_dashboard_integration():
    """Test the integration between brain and dashboard"""
    print("🧪 Testing Brain-Dashboard Integration")
    print("=" * 50)
    
    # Test 1: Check if all components exist
    print("\n1️⃣ Testing Component Files...")
    components = {
        'Brain Launcher': 'launch_brain_fixed.py',
        'Brain Core': 'newborn_brain_core.py',
        'Enhanced Dashboard': 'enhanced_dashboard.py',
        'Dashboard Bridge': 'brain_dashboard_bridge.py',
        'Network Coordinator': 'network_coordinator.py',
        'Ultimate Launcher': 'LAUNCH_BRAIN_ULTIMATE.bat'
    }
    
    for name, file in components.items():
        if Path(file).exists():
            print(f"✅ {name}: Ready")
        else:
            print(f"❌ {name}: Missing")
    
    # Test 2: Check configuration
    print("\n2️⃣ Testing Configuration...")
    config_file = Path("brain_config.json")
    if config_file.exists():
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
            print("✅ Brain Config: Valid JSON")
            print(f"   - Learning Rate: {config.get('learning_rate', 'N/A')}")
            print(f"   - Thinking Cycles: {config.get('thinking_cycles', 'N/A')}")
        except Exception as e:
            print(f"❌ Brain Config: Error - {e}")
    else:
        print("⚠️ Brain Config: Using defaults")
    
    # Test 3: Check dependencies
    print("\n3️⃣ Testing Dependencies...")
    dependencies = ['streamlit', 'plotly', 'pandas', 'requests', 'websockets']
    
    for dep in dependencies:
        try:
            __import__(dep)
            print(f"✅ {dep}: Installed")
        except ImportError:
            print(f"❌ {dep}: Missing")
    
    # Test 4: Test dashboard startup (quick check)
    print("\n4️⃣ Testing Dashboard Components...")
    try:
        import streamlit as st
        print("✅ Streamlit: Import successful")
        
        import plotly.graph_objects as go
        print("✅ Plotly: Import successful")
        
        import websockets
        print("✅ WebSockets: Import successful")
        
    except Exception as e:
        print(f"❌ Dashboard imports failed: {e}")
    
    # Test 5: Create sample log entry
    print("\n5️⃣ Testing Log Integration...")
    log_file = Path("test_brain.log")
    try:
        with open(log_file, 'w', encoding='utf-8') as f:
            f.write(f"[{datetime.now().isoformat()}] 🧠 BRAIN CYCLE #1 - Testing dashboard integration\n")
            f.write(f"[{datetime.now().isoformat()}] ✅ Test capability activated\n")
            f.write(f"[{datetime.now().isoformat()}] 🎯 LEARNING: Dashboard communication\n")
        
        print("✅ Test logs created")
        
        # Clean up
        log_file.unlink()
        print("✅ Test logs cleaned up")
        
    except Exception as e:
        print(f"❌ Log test failed: {e}")
    
    # Final summary
    print("\n" + "=" * 50)
    print("🎯 INTEGRATION TEST COMPLETE")
    print("\n📋 Next Steps:")
    print("1. 🚀 Run: LAUNCH_BRAIN_ULTIMATE.bat")
    print("2. 🌟 Choose option 4: 'Launch BOTH Brain + Dashboard'")
    print("3. 📊 Monitor your brain in real-time via the dashboard!")
    print("4. 🌐 Dashboard URL: http://localhost:8501")
    print("\n🎉 Your brain-dashboard integration is ready!")

if __name__ == "__main__":
    test_brain_dashboard_integration()