#!/usr/bin/env python3
"""
PB2S Brain Network Monitor
Real-time monitoring of distributed brain network
"""

import time
import socket
import subprocess
import json
from datetime import datetime

class BrainNetworkMonitor:
    def __init__(self):
        self.brain_nodes = {
            "big_brain": {
                "ip": "10.143.230.228",
                "type": "jetson_orin_8gb", 
                "role": "primary_reasoning",
                "ports": [22, 5000, 8000, 8765]
            },
            "edge_brain": {
                "ip": "10.143.230.90",
                "type": "jetson_nano_2gb",
                "role": "edge_processing", 
                "ports": [22, 5000, 8001, 8766]
            }
        }
        
    def ping_test(self, ip):
        """Test if device responds to ping"""
        try:
            result = subprocess.run(
                ["ping", "-n", "1", "-w", "1000", ip],
                capture_output=True, text=True
            )
            return result.returncode == 0
        except:
            return False
    
    def port_test(self, ip, port):
        """Test if specific port is open"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((ip, port))
            sock.close()
            return result == 0
        except:
            return False
    
    def scan_node(self, node_name, node_config):
        """Comprehensive scan of brain node"""
        ip = node_config["ip"]
        status = {
            "name": node_name,
            "ip": ip,
            "type": node_config["type"],
            "role": node_config["role"],
            "ping": self.ping_test(ip),
            "ports": {},
            "brain_status": "unknown",
            "timestamp": datetime.now().isoformat()
        }
        
        if status["ping"]:
            # Test each port
            for port in node_config["ports"]:
                status["ports"][port] = self.port_test(ip, port)
            
            # Determine brain status
            if status["ports"].get(22, False):
                status["brain_status"] = "ssh_ready"
            elif status["ports"].get(5000, False) or status["ports"].get(8000, False):
                status["brain_status"] = "brain_active"
            else:
                status["brain_status"] = "booting"
        else:
            status["brain_status"] = "offline"
            
        return status
    
    def monitor_network(self, duration_minutes=5):
        """Monitor network for specified duration"""
        print("🧠 PB2S Brain Network Monitor Starting...")
        print("=" * 60)
        
        end_time = time.time() + (duration_minutes * 60)
        
        while time.time() < end_time:
            print(f"\n🕒 {datetime.now().strftime('%H:%M:%S')} - Network Scan")
            print("-" * 40)
            
            for node_name, node_config in self.brain_nodes.items():
                status = self.scan_node(node_name, node_config)
                
                # Status emoji
                if status["brain_status"] == "brain_active":
                    emoji = "🟢"
                elif status["brain_status"] == "ssh_ready":
                    emoji = "🟡" 
                elif status["brain_status"] == "booting":
                    emoji = "🔵"
                else:
                    emoji = "🔴"
                
                print(f"{emoji} {status['name']:12} ({status['ip']:15}) - {status['brain_status']}")
                
                # Show open ports
                open_ports = [str(port) for port, open_status in status['ports'].items() if open_status]
                if open_ports:
                    print(f"   📡 Open ports: {', '.join(open_ports)}")
            
            # Check if both brains are active
            statuses = [self.scan_node(name, config)["brain_status"] 
                       for name, config in self.brain_nodes.items()]
            
            if all(status in ["brain_active", "ssh_ready"] for status in statuses):
                print("\n🎉 DISTRIBUTED BRAIN NETWORK FULLY OPERATIONAL!")
                return True
                
            time.sleep(10)  # Wait 10 seconds between scans
        
        print(f"\n⏰ Monitoring completed after {duration_minutes} minutes")
        return False

if __name__ == "__main__":
    monitor = BrainNetworkMonitor()
    monitor.monitor_network(duration_minutes=5)