#!/usr/bin/env python3
"""
🌐 JETSON NETWORK DISCOVERY - Live Device Scanner
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Real-time discovery of active Jetson devices on the network.
Scans for devices and prepares for PB2S consciousness deployment.
"""

import subprocess
import socket
import threading
import time
from datetime import datetime

class JetsonNetworkDiscovery:
    def __init__(self):
        self.discovered_devices = []
        self.target_ips = [
            "10.143.230.228",  # Jetson Orin 8GB (FOUND!)
            "192.168.1.101",  # Jetson 4GB (defective)
            "192.168.1.102"   # Jetson Nano 2GB (disconnected)
        ]
        
    def scan_device(self, ip):
        """Scan a single device for availability"""
        try:
            # Try ping first
            result = subprocess.run(['ping', '-n', '1', '-w', '1000', ip], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                # Device responds to ping
                device_info = {
                    'ip': ip,
                    'status': 'ONLINE',
                    'ping_time': self.extract_ping_time(result.stdout),
                    'ssh_available': self.check_ssh(ip),
                    'device_type': self.identify_device(ip)
                }
                self.discovered_devices.append(device_info)
                return True
            else:
                # Device not responding
                device_info = {
                    'ip': ip,
                    'status': 'OFFLINE',
                    'device_type': self.identify_device(ip)
                }
                self.discovered_devices.append(device_info)
                return False
                
        except Exception as e:
            print(f"   ❌ Error scanning {ip}: {e}")
            return False
            
    def extract_ping_time(self, ping_output):
        """Extract ping time from ping output"""
        try:
            for line in ping_output.split('\n'):
                if 'time=' in line:
                    time_part = line.split('time=')[1].split('ms')[0]
                    return f"{time_part}ms"
            return "N/A"
        except:
            return "N/A"
            
    def check_ssh(self, ip):
        """Check if SSH is available on the device"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex((ip, 22))
            sock.close()
            return result == 0
        except:
            return False
            
    def identify_device(self, ip):
        """Identify device type based on IP"""
        device_map = {
            "10.143.230.228": "Jetson Orin 8GB",
            "192.168.1.101": "Jetson 4GB (defective)", 
            "192.168.1.102": "Jetson Nano 2GB (disconnected)"
        }
        return device_map.get(ip, "Unknown Device")
        
    def scan_network(self):
        """Scan all target devices"""
        print("🌐 JETSON NETWORK DISCOVERY")
        print("="*60)
        print(f"⏰ Scan Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        print("🔍 Scanning network for Jetson devices...")
        
        # Clear previous results
        self.discovered_devices = []
        
        # Scan each target device
        for ip in self.target_ips:
            print(f"   📡 Scanning {ip}...", end=" ")
            if self.scan_device(ip):
                print("✅ FOUND")
            else:
                print("❌ OFFLINE")
                
        print()
        self.display_results()
        
    def display_results(self):
        """Display scan results"""
        print("📊 NETWORK SCAN RESULTS:")
        print("-"*50)
        
        online_count = 0
        for device in self.discovered_devices:
            status_icon = "🟢" if device['status'] == 'ONLINE' else "🔴"
            print(f"   {status_icon} {device['device_type']}: {device['ip']}")
            
            if device['status'] == 'ONLINE':
                print(f"      ✅ Status: ONLINE")
                print(f"      ⚡ Ping: {device.get('ping_time', 'N/A')}")
                ssh_status = "✅ Available" if device.get('ssh_available') else "❌ Not ready"
                print(f"      🔐 SSH: {ssh_status}")
                online_count += 1
            else:
                print(f"      ❌ Status: OFFLINE")
                
            print()
            
        print("📈 NETWORK SUMMARY:")
        print(f"   🟢 Online Devices: {online_count}/3")
        print(f"   🔴 Offline Devices: {3 - online_count}/3")
        print()
        
        if online_count > 0:
            print("🚀 READY FOR PB2S DEPLOYMENT:")
            for device in self.discovered_devices:
                if device['status'] == 'ONLINE':
                    if device.get('ssh_available'):
                        print(f"   ✅ {device['device_type']}: Ready for brain core deployment")
                    else:
                        print(f"   🔄 {device['device_type']}: Booting, SSH not ready yet")
        else:
            print("⏳ WAITING FOR DEVICES:")
            print("   🔄 No devices detected yet. Check power and network connections.")
            
    def get_router_info(self):
        """Get router gateway information"""
        try:
            result = subprocess.run(['ipconfig'], capture_output=True, text=True)
            for line in result.stdout.split('\n'):
                if 'Default Gateway' in line and '192.168.1' in line:
                    gateway = line.split(':')[-1].strip()
                    print(f"🌐 Router Gateway: {gateway}")
                    return gateway
        except:
            pass
        return "192.168.1.1"
        
    def run_discovery(self):
        """Run complete network discovery"""
        self.get_router_info()
        self.scan_network()
        
        # Provide next steps
        online_devices = [d for d in self.discovered_devices if d['status'] == 'ONLINE']
        
        if len(online_devices) >= 1:
            print("🎯 NEXT STEPS:")
            print("   1. Wait for SSH to become available (may take 1-2 minutes)")
            print("   2. Deploy PB2S brain cores to online devices")
            print("   3. Configure static IP addresses")
            print("   4. Start distributed consciousness network")
        else:
            print("🔧 TROUBLESHOOTING:")
            print("   1. Check power LED status on devices")
            print("   2. Verify Ethernet cable connections")
            print("   3. Wait 2-3 minutes for full boot process")
            print("   4. Re-run network scan")

def main():
    """Main execution function"""
    print("🚀 Initializing Jetson Network Discovery...")
    print()
    
    discovery = JetsonNetworkDiscovery()
    discovery.run_discovery()

if __name__ == "__main__":
    main()