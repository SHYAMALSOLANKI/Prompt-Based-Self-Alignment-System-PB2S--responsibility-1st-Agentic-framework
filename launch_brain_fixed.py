#!/usr/bin/env python3
"""
Fixed launcher for Autonomous Brain with proper Unicode support
"""
import os
import sys
import subprocess
import asyncio

def setup_windows_unicode():
    """Configure Windows console for proper Unicode display"""
    if sys.platform == "win32":
        # Set console to UTF-8
        os.system("chcp 65001 > nul 2>&1")
        
        # Set environment variables for Python
        os.environ["PYTHONIOENCODING"] = "utf-8"
        os.environ["PYTHONUTF8"] = "1"
        
        # Enable virtual terminal processing for emoji support
        try:
            import ctypes
            kernel32 = ctypes.windll.kernel32
            handle = kernel32.GetStdHandle(-11)  # STD_OUTPUT_HANDLE
            kernel32.SetConsoleMode(handle, 7)   # Enable VT processing
        except:
            pass

def main():
    """Main launcher with Unicode support"""
    print("🧠 Autonomous Brain Launcher v2.0")
    print("=" * 40)
    
    # Setup Unicode support
    setup_windows_unicode()
    
    # Get script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    brain_script = os.path.join(script_dir, "launch_autonomous_brain.py")
    venv_python = os.path.join(script_dir, ".venv", "Scripts", "python.exe")
    
    # Check if virtual environment exists
    if not os.path.exists(venv_python):
        print("❌ Virtual environment not found!")
        print(f"Expected: {venv_python}")
        sys.exit(1)
    
    # Parse command line arguments
    mode = "test" if len(sys.argv) > 1 and sys.argv[1] == "--test" else "autonomous"
    
    print(f"🚀 Starting brain in {mode} mode...")
    print(f"📍 Using Python: {venv_python}")
    print(f"🧠 Script: {brain_script}")
    print()
    
    # Build command
    cmd = [venv_python, brain_script]
    if mode == "test":
        cmd.append("--mode")
        cmd.append("test")
    
    # Set environment for subprocess
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONUTF8"] = "1"
    
    try:
        # Run the brain
        result = subprocess.run(
            cmd,
            cwd=script_dir,
            env=env,
            text=True,
            encoding='utf-8'
        )
        
        print(f"\n🏁 Brain session ended with code: {result.returncode}")
        
    except KeyboardInterrupt:
        print("\n⚠️  Brain session interrupted by user")
    except Exception as e:
        print(f"\n❌ Error running brain: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()