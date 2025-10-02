#!/usr/bin/env python3
"""
🧠 HOME AI BRAIN NETWORK - QUICK START LAUNCHER
Complete distributed AI system across laptop + Jetson devices
"""
import os
import sys
import subprocess
import time
import json
from pathlib import Path
from datetime import datetime

class BrainNetworkLauncher:
    def __init__(self):
        self.script_dir = Path(__file__).parent
        self.python_exe = self.script_dir / ".venv" / "Scripts" / "python.exe"
        
    def print_banner(self):
        print("╔" + "═" * 58 + "╗")
        print("║" + " " * 58 + "║")
        print("║" + "  🧠 HOME AI BRAIN NETWORK - COMPLETE SYSTEM  ".center(58) + "║")
        print("║" + " " * 58 + "║")
        print("║" + "  Your Personal Distributed AI Network        ".center(58) + "║")
        print("║" + "  💻 Laptop + 🔥 Jetson Orin + 📱 Jetson 2GB  ".center(58) + "║")
        print("║" + " " * 58 + "║")
        print("╚" + "═" * 58 + "╝")
        print()
        
    def check_system_status(self):
        """Check system components"""
        print("🔍 System Status Check:")
        print("-" * 40)
        
        # Check Python environment
        if self.python_exe.exists():
            print("✅ Python virtual environment: Ready")
        else:
            print("❌ Python virtual environment: Missing")
            return False
        
        # Check core files
        core_files = [
            "launch_autonomous_brain.py",
            "launch_brain_fixed.py", 
            "network_coordinator.py",
            "enhanced_dashboard.py",
            "newborn_brain_core.py"
        ]
        
        for file in core_files:
            if (self.script_dir / file).exists():
                print(f"✅ {file}: Ready")
            else:
                print(f"❌ {file}: Missing")
                return False
        
        print("✅ All core components available")
        return True
    
    def launch_component(self, script_name, description, background=True):
        """Launch a system component"""
        script_path = self.script_dir / script_name
        
        try:
            print(f"🚀 Starting {description}...")
            
            if background:
                # Start in background
                process = subprocess.Popen(
                    [str(self.python_exe), str(script_path)],
                    cwd=str(self.script_dir),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == "win32" else 0
                )
                time.sleep(2)  # Give it time to start
                
                if process.poll() is None:
                    print(f"✅ {description} started successfully (PID: {process.pid})")
                    return process
                else:
                    print(f"❌ {description} failed to start")
                    return None
            else:
                # Start in foreground
                result = subprocess.run(
                    [str(self.python_exe), str(script_path)],
                    cwd=str(self.script_dir)
                )
                return result
                
        except Exception as e:
            print(f"❌ Failed to start {description}: {e}")
            return None
    
    def show_quick_commands(self):
        """Show quick command reference"""
        print("\n📋 QUICK COMMANDS:")
        print("-" * 40)
        print("🧠 Test Brain:          python launch_brain_fixed.py --test")
        print("🚀 Start Brain:         python launch_brain_fixed.py")
        print("🌐 Network Coordinator: python network_coordinator.py")
        print("📊 Dashboard:           python enhanced_dashboard.py")
        print("🤖 LLM Setup:          python setup_local_llm.py")
        print("📖 View Guide:         type HOME_AI_BRAIN_NETWORK_GUIDE.md")
        print()
    
    def run_full_system_test(self):
        """Run complete system test"""
        print("🧪 RUNNING FULL SYSTEM TEST")
        print("=" * 40)
        
        # Test 1: Brain core functionality
        print("\n🧠 Testing Brain Core...")
        brain_test = self.launch_component("launch_brain_fixed.py --test", "Brain Test", background=False)
        
        if brain_test and brain_test.returncode == 0:
            print("✅ Brain core test PASSED")
        else:
            print("❌ Brain core test FAILED")
            return False
        
        # Test 2: Dashboard availability
        print("\n📊 Testing Dashboard...")
        try:
            import streamlit
            print("✅ Dashboard dependencies available")
        except ImportError:
            print("❌ Dashboard dependencies missing")
            print("   Run: pip install streamlit plotly pandas")
            return False
        
        print("✅ All system tests PASSED!")
        return True
    
    def launch_full_system(self):
        """Launch the complete brain network"""
        print("🚀 LAUNCHING COMPLETE BRAIN NETWORK")
        print("=" * 40)
        
        processes = []
        
        # 1. Start Network Coordinator
        coord_process = self.launch_component(
            "network_coordinator.py", 
            "Network Coordinator", 
            background=True
        )
        if coord_process:
            processes.append(("Network Coordinator", coord_process))
        
        time.sleep(3)
        
        # 2. Start Enhanced Dashboard
        print("📊 Starting Enhanced Dashboard...")
        print("   Dashboard will open in your web browser")
        print("   URL: http://localhost:8501")
        
        dashboard_process = subprocess.Popen([
            "streamlit", "run", "enhanced_dashboard.py",
            "--server.port", "8501",
            "--server.headless", "true"
        ], cwd=str(self.script_dir))
        
        if dashboard_process:
            processes.append(("Enhanced Dashboard", dashboard_process))
        
        time.sleep(5)
        
        # 3. Start Main Brain
        brain_process = self.launch_component(
            "launch_brain_fixed.py",
            "Main Brain System",
            background=True
        )
        if brain_process:
            processes.append(("Main Brain", brain_process))
        
        # Show status
        print("\n🎉 BRAIN NETWORK LAUNCHED!")
        print("=" * 40)
        print("Active Components:")
        for name, process in processes:
            if process.poll() is None:
                print(f"✅ {name} (PID: {process.pid})")
            else:
                print(f"❌ {name} (Failed)")
        
        print("\n🌐 Access Points:")
        print("📊 Dashboard:    http://localhost:8501")
        print("🌐 Coordinator:  ws://localhost:8768")
        print("🧠 Brain Logs:   autonomous_brain.log")
        
        print("\n⚠️  Press Ctrl+C to stop all components")
        
        try:
            # Keep launcher running
            while True:
                time.sleep(10)
                # Check if processes are still running
                active_count = sum(1 for _, p in processes if p.poll() is None)
                print(f"🔄 {active_count}/{len(processes)} components active - {datetime.now().strftime('%H:%M:%S')}")
        
        except KeyboardInterrupt:
            print("\n🛑 Shutting down brain network...")
            for name, process in processes:
                try:
                    process.terminate()
                    print(f"🔚 Stopped {name}")
                except:
                    pass
            print("👋 Brain network shutdown complete")

def main():
    launcher = BrainNetworkLauncher()
    launcher.print_banner()
    
    if not launcher.check_system_status():
        print("❌ System check failed. Please fix the issues above.")
        return
    
    print("\n🎯 CHOOSE OPERATION:")
    print("1. 🧪 Run System Test")
    print("2. 🧠 Test Brain Only")
    print("3. 📊 Launch Dashboard Only")
    print("4. 🚀 Launch Full Network")
    print("5. 📋 Show Quick Commands")
    print("6. 🏃 Exit")
    
    try:
        choice = input("\nEnter choice (1-6): ").strip()
        
        if choice == "1":
            launcher.run_full_system_test()
            
        elif choice == "2":
            print("\n🧠 Testing Brain System...")
            launcher.launch_component("launch_brain_fixed.py --test", "Brain Test", background=False)
            
        elif choice == "3":
            print("\n📊 Launching Dashboard...")
            print("Opening dashboard at http://localhost:8501")
            subprocess.run([
                "streamlit", "run", "enhanced_dashboard.py",
                "--server.port", "8501"
            ], cwd=str(launcher.script_dir))
            
        elif choice == "4":
            launcher.launch_full_system()
            
        elif choice == "5":
            launcher.show_quick_commands()
            
        elif choice == "6":
            print("👋 Goodbye! Your brain network is ready when you are.")
            
        else:
            print("❌ Invalid choice")
            
    except KeyboardInterrupt:
        print("\n👋 Launcher interrupted")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()