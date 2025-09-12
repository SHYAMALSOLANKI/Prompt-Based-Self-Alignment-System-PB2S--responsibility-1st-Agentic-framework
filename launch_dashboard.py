import subprocess
import sys
import os

def main():
    # Safe mode: block dangerous actions by default
    os.environ["PB2S_SAFE_MODE"] = "1"
    print("Launching PB2S Dashboard in SAFE MODE (no destructive actions allowed)...")
    subprocess.run([sys.executable, "-m", "streamlit", "run", "pb2s_dashboard.py"])

if __name__ == "__main__":
    main()
