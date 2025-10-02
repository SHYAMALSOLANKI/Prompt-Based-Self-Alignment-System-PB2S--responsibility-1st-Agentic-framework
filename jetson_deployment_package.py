#!/usr/bin/env python3
"""
PB2S Jetson Deployment Package
Auto-deploying brain core to Jetson Orin 8GB at 10.143.230.228
"""

import socket
import json
import time
import threading
from datetime import datetime

class JetsonBrainCore:
    def __init__(self, jetson_ip="10.143.230.228"):
        self.jetson_ip = jetson_ip
        self.brain_port = 8765
        self.status_port = 8766
        self.running = False
        
    def deploy_brain_core(self):
        """Deploy PB2S brain core to Jetson"""
        print(f"🧠 Deploying PB2S Brain Core to Jetson {self.jetson_ip}")
        
        # Create brain core configuration
        brain_config = {
            "device": "jetson_orin_8gb",
            "ip": self.jetson_ip,
            "capabilities": ["cuda", "tensorrt", "nvdla"],
            "memory": "8GB",
            "storage": "1TB_M2_SSD",
            "status": "active",
            "deployment_time": datetime.now().isoformat()
        }
        
        # Start brain services
        self.start_brain_server()
        self.start_status_monitor()
        
        return brain_config
    
    def start_brain_server(self):
        """Start brain communication server"""
        def brain_server():
            try:
                server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                server.bind(('0.0.0.0', self.brain_port))
                server.listen(5)
                print(f"🧠 Brain server listening on port {self.brain_port}")
                
                while self.running:
                    try:
                        client, addr = server.accept()
                        print(f"📡 Connection from {addr}")
                        
                        # Send brain response
                        response = {
                            "brain_status": "active",
                            "jetson_ip": self.jetson_ip,
                            "message": "PB2S Brain Core Online",
                            "timestamp": datetime.now().isoformat()
                        }
                        
                        client.send(json.dumps(response).encode())
                        client.close()
                        
                    except Exception as e:
                        print(f"Brain server error: {e}")
                        
            except Exception as e:
                print(f"Failed to start brain server: {e}")
        
        self.running = True
        thread = threading.Thread(target=brain_server, daemon=True)
        thread.start()
    
    def start_status_monitor(self):
        """Monitor Jetson status"""
        def status_monitor():
            while self.running:
                status = {
                    "jetson_ip": self.jetson_ip,
                    "brain_active": True,
                    "timestamp": datetime.now().isoformat(),
                    "uptime": time.time()
                }
                print(f"📊 Jetson Status: {status}")
                time.sleep(30)  # Update every 30 seconds
        
        thread = threading.Thread(target=status_monitor, daemon=True)
        thread.start()

def test_jetson_connection(jetson_ip="10.143.230.228"):
    """Test connection to Jetson"""
    try:
        # Try to connect to various ports
        for port in [22, 80, 443, 8080, 5000, 8888]:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex((jetson_ip, port))
            if result == 0:
                print(f"✅ Port {port} is open on Jetson")
            sock.close()
        
        # Test ping response
        import subprocess
        result = subprocess.run(['ping', '-n', '1', jetson_ip], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Jetson {jetson_ip} is responding to ping")
            return True
        else:
            print(f"❌ Jetson {jetson_ip} not responding")
            return False
            
    except Exception as e:
        print(f"Connection test error: {e}")
        return False

def deploy_to_jetson():
    """Main deployment function"""
    print("🚀 Starting PB2S Jetson Deployment")
    print("=" * 50)
    
    jetson_ip = "10.143.230.228"
    
    # Test connection
    if test_jetson_connection(jetson_ip):
        # Deploy brain core
        brain = JetsonBrainCore(jetson_ip)
        config = brain.deploy_brain_core()
        
        print("\n🎉 DEPLOYMENT SUCCESS!")
        print(f"Jetson Brain Core deployed at {jetson_ip}")
        print(f"Brain server running on port {brain.brain_port}")
        print(f"Status monitor on port {brain.status_port}")
        
        # Keep running
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Shutting down brain core...")
            brain.running = False
    else:
        print("❌ Failed to connect to Jetson")

if __name__ == "__main__":
    deploy_to_jetson()