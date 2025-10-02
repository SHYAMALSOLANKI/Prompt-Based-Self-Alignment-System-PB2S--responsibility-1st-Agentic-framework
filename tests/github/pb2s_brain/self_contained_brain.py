#!/usr/bin/env python3
"""
PB2S Self-Contained Brain - Complete Autonomous System
Everything needed for distributed AI consciousness on single SD card

This is the EXPERT approach - each Jetson is completely self-sufficient!
"""

import os
import sys
import json
import asyncio
import logging
import subprocess
from pathlib import Path
from datetime import datetime

class SelfContainedBrain:
    def __init__(self):
        # Detect if we're on SD card or main system
        self.sd_path = Path("/media") if Path("/media").exists() else Path("/boot")
        self.home_path = Path.home()
        
        # Brain locations
        self.brain_source = self.sd_path / "pb2s_brain"
        self.models_source = self.sd_path / "models"
        
        # Runtime locations
        self.brain_runtime = self.home_path / "pb2s_brain"
        self.models_runtime = self.home_path / "models"
        
        # Device identification
        self.device_config = self.detect_device()
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.home_path / 'brain_startup.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('SelfContainedBrain')
        
    def detect_device(self):
        """Auto-detect which Jetson device this is"""
        try:
            # Try to get device info
            with open('/proc/device-tree/model', 'r') as f:
                model = f.read().strip()
                
            if 'Orin' in model and '8GB' in model:
                return {
                    "type": "jetson_orin_8gb",
                    "role": "big_brain", 
                    "ip": "10.143.230.228",
                    "capabilities": ["large_models", "complex_reasoning", "vision_processing"]
                }
            elif 'Nano' in model and '2GB' in model:
                return {
                    "type": "jetson_nano_2gb",
                    "role": "edge_brain",
                    "ip": "10.143.230.90", 
                    "capabilities": ["edge_processing", "monitoring", "lightweight_models"]
                }
            else:
                return {
                    "type": "jetson_unknown",
                    "role": "general_brain",
                    "ip": "10.143.230.200",
                    "capabilities": ["general_processing"]
                }
        except:
            return {
                "type": "jetson_generic",
                "role": "brain_node",
                "ip": "10.143.230.250", 
                "capabilities": ["autonomous_processing"]
            }
    
    def setup_environment(self):
        """Setup complete environment from SD card"""
        self.logger.info(f"🧠 Setting up {self.device_config['type']} as {self.device_config['role']}")
        
        # Create runtime directories
        self.brain_runtime.mkdir(exist_ok=True)
        self.models_runtime.mkdir(exist_ok=True)
        
        # Copy brain files from SD card to runtime location
        if self.brain_source.exists():
            self.logger.info("📁 Copying brain core from SD card...")
            subprocess.run([
                "cp", "-r", str(self.brain_source / "*"), str(self.brain_runtime)
            ], shell=True)
        
        # Copy models if space allows
        if self.models_source.exists():
            self.logger.info("🤖 Setting up AI models...")
            # Copy appropriate models based on device capabilities
            self.setup_models()
    
    def setup_models(self):
        """Setup models based on device capabilities"""
        if self.device_config['role'] == 'big_brain':
            # Orin 8GB gets the heavy models
            models_to_copy = [
                "gemma-3-4b-it-Q4_K_M.gguf",
                "qwen2.5-vl-7b-vision-mmproj-f16.gguf",
                "llama-13b-mmproj-v1.5.Q4_1.gguf"
            ]
        elif self.device_config['role'] == 'edge_brain':
            # Nano 2GB gets lightweight models
            models_to_copy = [
                "Qwen2-VL-2B-mmproj-q5_1.gguf",
                "LLaMA3-8B_mmproj-Q4_1.gguf"
            ]
        else:
            # Generic setup
            models_to_copy = ["gemma-3-4b-it-Q4_K_M.gguf"]
        
        for model in models_to_copy:
            src = self.models_source / model
            dst = self.models_runtime / model
            if src.exists() and not dst.exists():
                self.logger.info(f"📦 Installing model: {model}")
                subprocess.run(["cp", str(src), str(dst)])
    
    def install_dependencies(self):
        """Install Python dependencies"""
        self.logger.info("📦 Installing dependencies...")
        
        requirements_file = self.brain_runtime / "requirements_autonomous_brain.txt"
        if requirements_file.exists():
            subprocess.run([
                sys.executable, "-m", "pip", "install", "-r", str(requirements_file)
            ])
        
        # Install additional Jetson-specific packages
        jetson_packages = [
            "torch", "torchvision", "torchaudio",
            "opencv-python", "numpy", "scipy"
        ]
        
        for package in jetson_packages:
            try:
                subprocess.run([
                    sys.executable, "-m", "pip", "install", package
                ], check=False)
            except:
                self.logger.warning(f"Could not install {package}, continuing...")
    
    def start_brain(self):
        """Start the autonomous brain"""
        self.logger.info("🚀 Starting PB2S Brain...")
        
        # Set environment variables
        os.environ['PB2S_DEVICE_TYPE'] = self.device_config['type']
        os.environ['PB2S_DEVICE_ROLE'] = self.device_config['role']
        os.environ['PB2S_DEVICE_IP'] = self.device_config['ip']
        os.environ['PB2S_MODELS_PATH'] = str(self.models_runtime)
        
        # Start brain core
        brain_core = self.brain_runtime / "newborn_brain_core.py"
        if brain_core.exists():
            self.logger.info("✅ Brain core found, starting autonomous operation...")
            subprocess.run([sys.executable, str(brain_core)])
        else:
            self.logger.error("❌ Brain core not found!")
    
    def run_complete_setup(self):
        """Run complete setup and start brain"""
        try:
            self.logger.info("🌟 PB2S Self-Contained Brain Starting...")
            self.logger.info(f"Device: {self.device_config}")
            
            self.setup_environment()
            self.install_dependencies()
            self.start_brain()
            
        except Exception as e:
            self.logger.error(f"❌ Setup failed: {e}")
            raise

if __name__ == "__main__":
    print("🧠 PB2S Self-Contained Brain System")
    print("=" * 50)
    print("Expert approach: Complete AI brain on single SD card!")
    print()
    
    brain = SelfContainedBrain()
    brain.run_complete_setup()