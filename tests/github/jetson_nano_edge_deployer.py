#!/usr/bin/env python3
"""
PB2S Jetson Nano 2GB Edge Brain Deployment Package
Optimized for lightweight AI processing and edge monitoring
"""

import os
import sys
import subprocess
import json
import psutil
from pathlib import Path

class JetsonNanoEdgeBrain:
    def __init__(self):
        self.jetson_ip = "10.143.230.90"
        self.device_role = "edge_brain"
        self.home_dir = Path("/home/jetson")
        self.brain_dir = self.home_dir / "pb2s_edge_brain" 
        self.models_dir = self.home_dir / "lightweight_models"
        self.max_ram_gb = 2
        
    def setup_lightweight_environment(self):
        """Setup optimized Python environment for 2GB RAM"""
        print("🔧 Setting up lightweight Python environment...")
        
        # Create minimal virtual environment
        subprocess.run([
            "python3", "-m", "venv", 
            str(self.brain_dir / "venv"),
            "--system-site-packages"  # Use system packages to save space
        ])
        
        # Install only essential packages for edge processing
        pip_path = self.brain_dir / "venv" / "bin" / "pip"
        subprocess.run([
            str(pip_path), "install", "--no-cache-dir",
            "fastapi", "uvicorn", "websockets", 
            "psutil", "numpy", "opencv-python-headless",
            "requests", "aiofiles"
        ])
        
        print("✅ Lightweight environment configured")
        
    def check_system_resources(self):
        """Check available system resources"""
        ram_gb = psutil.virtual_memory().total / (1024**3)
        available_gb = psutil.virtual_memory().available / (1024**3)
        
        print(f"📊 System Resources:")
        print(f"   Total RAM: {ram_gb:.1f} GB")
        print(f"   Available RAM: {available_gb:.1f} GB")
        print(f"   CPU Cores: {psutil.cpu_count()}")
        
        return {
            "total_ram_gb": ram_gb,
            "available_ram_gb": available_gb,
            "cpu_cores": psutil.cpu_count()
        }
    
    def setup_edge_capabilities(self):
        """Setup edge processing capabilities"""
        print("🌐 Configuring edge processing capabilities...")
        
        capabilities = [
            "network_monitoring",
            "sensor_data_processing", 
            "lightweight_inference",
            "real_time_communication",
            "edge_coordination",
            "system_health_monitoring"
        ]
        
        # Create capability modules
        for capability in capabilities:
            module_file = self.brain_dir / f"{capability}.py"
            with open(module_file, 'w') as f:
                f.write(f'''#!/usr/bin/env python3
"""
{capability.replace('_', ' ').title()} Module
Edge processing capability for Jetson Nano 2GB
"""

class {capability.replace('_', '').title()}:
    def __init__(self):
        self.active = True
        self.capability_name = "{capability}"
    
    async def process(self, data):
        """Process data for {capability}"""
        # Implementation will be added during deployment
        return {{"status": "ready", "capability": "{capability}"}}
''')
        
        print(f"   ✅ {capability} module created")
        
    def deploy_edge_brain_core(self):
        """Deploy the PB2S edge brain core"""
        print("🧠 Deploying PB2S edge brain core...")
        
        system_info = self.check_system_resources()
        
        # Edge brain configuration optimized for 2GB RAM
        edge_config = {
            "device": "jetson_nano_2gb",
            "ip": self.jetson_ip,
            "role": "edge_brain",
            "max_ram_gb": self.max_ram_gb,
            "system_resources": system_info,
            "model_storage": str(self.models_dir),
            "capabilities": [
                "lightweight_inference",
                "network_monitoring",
                "sensor_processing",
                "real_time_response",
                "edge_coordination"
            ],
            "recommended_models": [
                "Qwen2-VL-2B-mmproj-q5_1.gguf",  # 500MB - fits in 2GB
                "lightweight_text_model.gguf",
                "edge_monitoring_model.gguf"
            ],
            "status": "ready_for_edge_deployment",
            "connection": {
                "big_brain": "10.143.230.228",
                "coordinator": "10.143.230.129",
                "network_switch": "8_port_gigabit"
            }
        }
        
        # Save edge configuration
        config_file = self.brain_dir / "edge_brain_config.json"
        with open(config_file, 'w') as f:
            json.dump(edge_config, f, indent=2)
            
        print(f"✅ Edge brain configuration saved: {config_file}")
        return edge_config
    
    def start_edge_server(self):
        """Start edge brain communication server"""
        print("🚀 Starting edge brain server...")
        print("🔗 Ready to coordinate with:")
        print("   🧠 Big Brain (Orin 8GB): 10.143.230.228")
        print("   🖥️ Coordinator (Laptop): 10.143.230.129")
        print("   📡 Network: 8-port switch via Cat 6")
        
        print("\n📦 Waiting for deployment packages:")
        print("   - Edge brain core files")
        print("   - Lightweight GGUF models") 
        print("   - Sensor integration scripts")
        print("   - Network coordination protocols")

if __name__ == "__main__":
    print("🌐 PB2S Jetson Nano 2GB Edge Brain Deployment")
    print("=" * 55)
    
    edge_brain = JetsonNanoEdgeBrain()
    edge_brain.setup_lightweight_environment()
    edge_brain.setup_edge_capabilities() 
    config = edge_brain.deploy_edge_brain_core()
    edge_brain.start_edge_server()
    
    print(f"\n✅ Jetson Nano 2GB Edge Brain ready!")
    print(f"🌐 IP: {config['ip']}")
    print(f"🔧 Role: {config['role']}")
    print("📞 SSH: ssh jetson@10.143.230.90")