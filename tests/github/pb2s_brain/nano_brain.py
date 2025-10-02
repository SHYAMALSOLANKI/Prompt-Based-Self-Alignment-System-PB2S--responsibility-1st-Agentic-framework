#!/usr/bin/env python3
"""
PB2S Nano Brain - Optimized for Jetson Nano 2GB
Resource-conscious version with memory management
"""

import os
import sys
import json
import time
import logging
import gc
from pathlib import Path
import threading
import psutil

class NanoBrain:
    def __init__(self):
        self.setup_logging()
        self.brain_path = self.find_brain_location()
        self.models_path = self.brain_path.parent / "models"
        self.config = self.load_nano_config()
        self.logger.info("🧠 PB2S Nano Brain initializing...")
        
    def setup_logging(self):
        """Set up logging for Nano brain"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - NANO - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('/tmp/nano_brain_detailed.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def find_brain_location(self):
        """Find brain location on SD card with multiple attempts"""
        possible_paths = [
            Path("/media/jetson"),
            Path("/mnt"),
            Path("/media"),
            Path("/")
        ]
        
        for base_path in possible_paths:
            if base_path.exists():
                # Look for brain in subdirectories
                for item in base_path.iterdir():
                    if item.is_dir():
                        brain_dir = item / "pb2s_brain"
                        if brain_dir.exists() and (brain_dir / "nano_brain.py").exists():
                            self.logger.info(f"📁 Found brain at: {brain_dir}")
                            return brain_dir
                            
                # Also check direct path
                brain_dir = base_path / "pb2s_brain"
                if brain_dir.exists():
                    self.logger.info(f"📁 Found brain at: {brain_dir}")
                    return brain_dir
                    
        # Fallback to current directory
        current = Path(__file__).parent
        self.logger.warning(f"⚠️ Using fallback path: {current}")
        return current
        
    def load_nano_config(self):
        """Load configuration optimized for Nano"""
        return {
            "device_type": "jetson_nano_2gb",
            "max_memory_mb": 1500,  # Leave 500MB for system
            "model_priority": ["gemma-3-4b-it-Q4_K_M.gguf"],  # Smallest model first
            "threads": 2,  # Limited for Nano
            "context_length": 512,  # Reduced context
            "batch_size": 8,  # Small batches
            "monitoring_interval": 30,
            "auto_gc": True
        }
        
    def check_system_resources(self):
        """Monitor system resources"""
        try:
            memory = psutil.virtual_memory()
            cpu_percent = psutil.cpu_percent(interval=1)
            
            self.logger.info(f"📊 Memory: {memory.percent:.1f}% used ({memory.available/1024/1024:.0f}MB free)")
            self.logger.info(f"📊 CPU: {cpu_percent:.1f}% used")
            
            # Memory management
            if memory.percent > 85:
                self.logger.warning("⚠️ High memory usage, running garbage collection")
                gc.collect()
                
            return {
                "memory_percent": memory.percent,
                "memory_free_mb": memory.available / 1024 / 1024,
                "cpu_percent": cpu_percent
            }
        except Exception as e:
            self.logger.error(f"❌ Resource check failed: {e}")
            return None
            
    def load_model(self, model_name):
        """Load model with memory constraints"""
        model_path = self.models_path / model_name
        
        if not model_path.exists():
            self.logger.error(f"❌ Model not found: {model_path}")
            return None
            
        # Check if we have enough memory
        resources = self.check_system_resources()
        if resources and resources["memory_free_mb"] < 500:
            self.logger.warning("⚠️ Insufficient memory to load model")
            return None
            
        try:
            self.logger.info(f"🔄 Loading model: {model_name}")
            # Simulate model loading (replace with actual model loading)
            time.sleep(2)
            self.logger.info(f"✅ Model loaded: {model_name}")
            return f"mock_model_{model_name}"
        except Exception as e:
            self.logger.error(f"❌ Model loading failed: {e}")
            return None
            
    def start_brain_services(self):
        """Start brain services optimized for Nano"""
        self.logger.info("🚀 Starting Nano brain services...")
        
        # Load primary model
        primary_model = self.load_model(self.config["model_priority"][0])
        if not primary_model:
            self.logger.error("❌ Failed to load primary model")
            return False
            
        # Start monitoring thread
        monitor_thread = threading.Thread(target=self.monitor_system, daemon=True)
        monitor_thread.start()
        
        # Main brain loop
        self.run_brain_loop()
        
    def monitor_system(self):
        """Background system monitoring"""
        while True:
            try:
                resources = self.check_system_resources()
                if resources:
                    # Log to status file
                    status = {
                        "timestamp": time.time(),
                        "device": "jetson_nano_2gb",
                        "status": "running",
                        "resources": resources
                    }
                    
                    with open("/tmp/nano_brain_status.json", "w") as f:
                        json.dump(status, f, indent=2)
                        
                time.sleep(self.config["monitoring_interval"])
            except Exception as e:
                self.logger.error(f"❌ Monitoring error: {e}")
                time.sleep(60)
                
    def run_brain_loop(self):
        """Main brain processing loop"""
        self.logger.info("🧠 Nano brain main loop started")
        
        try:
            while True:
                # Lightweight processing
                self.logger.info("💭 Nano brain thinking...")
                
                # Simulate brain processing
                time.sleep(10)
                
                # Periodic cleanup
                if self.config["auto_gc"]:
                    gc.collect()
                    
        except KeyboardInterrupt:
            self.logger.info("⏹️ Nano brain stopping...")
        except Exception as e:
            self.logger.error(f"❌ Brain loop error: {e}")
            
def main():
    """Main entry point"""
    try:
        # Create brain instance
        nano_brain = NanoBrain()
        
        # Start brain services
        nano_brain.start_brain_services()
        
    except Exception as e:
        logging.error(f"❌ Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()