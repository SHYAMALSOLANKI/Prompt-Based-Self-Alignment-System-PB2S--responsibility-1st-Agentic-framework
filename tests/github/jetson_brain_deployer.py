#!/usr/bin/env python3
"""
PB2S Jetson Orin 8GB Brain Deployment Package
Auto-deploying AI brain with CUDA acceleration
"""

import os
import sys
import subprocess
import json
from pathlib import Path

class JetsonBrainDeployer:
    def __init__(self):
        self.jetson_ip = "10.143.230.228"
        self.home_dir = Path("/home/jetson")
        self.brain_dir = self.home_dir / "pb2s_brain"
        self.models_dir = self.home_dir / "models"
        
    def setup_environment(self):
        """Setup Python environment for brain"""
        print("🐍 Setting up Python environment...")
        
        # Create virtual environment
        subprocess.run([
            "python3", "-m", "venv", 
            str(self.brain_dir / "venv")
        ])
        
        # Install dependencies
        pip_path = self.brain_dir / "venv" / "bin" / "pip"
        subprocess.run([
            str(pip_path), "install",
            "torch", "torchvision", "torchaudio",
            "transformers", "accelerate",
            "streamlit", "fastapi", "uvicorn",
            "websockets", "aiohttp", "opencv-python"
        ])
        
    def enable_cuda(self):
        """Enable CUDA acceleration"""
        print("⚡ Configuring CUDA acceleration...")
        
        # Check CUDA availability
        result = subprocess.run([
            "nvidia-smi"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ NVIDIA GPU detected and ready")
            return True
        else:
            print("⚠️ NVIDIA GPU not detected, using CPU mode")
            return False
    
    def deploy_brain_core(self):
        """Deploy the PB2S brain core"""
        print("🧠 Deploying PB2S brain core...")
        
        # Brain will be transferred via SCP after SSH is enabled
        brain_config = {
            "device": "jetson_orin_8gb",
            "ip": self.jetson_ip,
            "cuda_available": self.enable_cuda(),
            "model_storage": str(self.models_dir),
            "capabilities": [
                "large_language_models",
                "computer_vision", 
                "autonomous_reasoning",
                "distributed_processing"
            ],
            "status": "ready_for_connection"
        }
        
        # Save configuration
        config_file = self.brain_dir / "jetson_config.json"
        with open(config_file, 'w') as f:
            json.dump(brain_config, f, indent=2)
            
        print(f"✅ Brain configuration saved: {config_file}")
        return brain_config
    
    def start_brain_server(self):
        """Start brain communication server"""
        print("🚀 Starting brain server...")
        
        # This will start the actual brain once files are transferred
        print("Waiting for brain core files from laptop...")
        print("Ready to receive:")
        print("- newborn_brain_core.py")
        print("- GGUF models")
        print("- Configuration files")

if __name__ == "__main__":
    print("🧠 PB2S Jetson Orin 8GB Brain Deployment")
    print("=" * 50)
    
    deployer = JetsonBrainDeployer()
    deployer.setup_environment()
    config = deployer.deploy_brain_core()
    deployer.start_brain_server()
    
    print("\n✅ Jetson Orin 8GB ready for AI brain deployment!")
    print(f"IP: {config['ip']}")
    print("SSH from laptop: ssh jetson@10.143.230.228")