#!/usr/bin/env python3
"""
🌐 JETSON NETWORK DISCOVERY - FIXED VERSION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Real-time discovery of active Jetson devices on the network.
Now with dynamic subnet detection and proper network scanning.
"""

import subprocess
import socket
import threading
import time
import ipaddress
from datetime import datetime

class JetsonNetworkDiscoveryFixed:
    def __init__(self):
        self.discovered_devices = []
        self.network_interfaces = []
        self.target_subnets = []
        
    def get_network_interfaces(self):
        """Get all active network interfaces and their subnets"""
        # Use fallback method for Windows compatibility
        return self.get_network_interfaces_fallback()
    
    def get_network_interfaces_fallback(self):
        """Fallback method to get network info using ipconfig"""
        interfaces = []
        try:
            result = subprocess.run(['ipconfig'], capture_output=True, text=True)
            lines = result.stdout.split('\n')
            
            current_adapter = None
            current_ip = None
            current_mask = None
            
            for line in lines:
                line = line.strip()
                if 'adapter' in line.lower() and ':' in line:
                    current_adapter = line
                elif 'IPv4 Address' in line and ':' in line:
                    current_ip = line.split(':')[-1].strip()
                elif 'Subnet Mask' in line and ':' in line:
                    current_mask = line.split(':')[-1].strip()
                    
                    if current_ip and current_mask and not current_ip.startswith('127.'):
                        try:
                            network = ipaddress.IPv4Network(f"{current_ip}/{current_mask}", strict=False)
                            interfaces.append({
                                'interface': current_adapter or 'Unknown',
                                'ip': current_ip,
                                'network': str(network),
                                'subnet': network
                            })
                        except:
                            pass
                        current_ip = None
                        current_mask = None
                        
        except Exception as e:
            print(f"Error getting network interfaces: {e}")
            
        return interfaces
    
    def scan_device(self, ip):
        """Scan a single device for availability and identify if it's a Jetson"""
        try:
            # Try ping first
            result = subprocess.run(['ping', '-n', '1', '-w', '1000', str(ip)], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                device_info = {
                    'ip': str(ip),
                    'status': 'ONLINE',
                    'ping_time': self.extract_ping_time(result.stdout),
                    'ssh_available': self.check_ssh(str(ip)),
                    'device_type': self.identify_device_type(str(ip)),
                    'hostname': self.get_hostname(str(ip)),
                    'open_ports': self.scan_common_ports(str(ip))
                }
                return device_info
            else:
                return None
                
        except Exception as e:
            print(f"   ❌ Error scanning {ip}: {e}")
            return None
            
    def extract_ping_time(self, ping_output):
        """Extract ping time from ping output"""
        try:
            for line in ping_output.split('\n'):
                if 'time=' in line or 'time<' in line:
                    if 'time=' in line:
                        time_part = line.split('time=')[1].split('ms')[0]
                    else:
                        time_part = line.split('time<')[1].split('ms')[0]
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
    
    def scan_common_ports(self, ip):
        """Scan common ports to help identify device type"""
        common_ports = [22, 80, 443, 5000, 8000, 8080, 8888, 8765, 8766]
        open_ports = []
        
        for port in common_ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((ip, port))
                if result == 0:
                    open_ports.append(port)
                sock.close()
            except:
                pass
                
        return open_ports
    
    def get_hostname(self, ip):
        """Try to get hostname of the device"""
        try:
            hostname = socket.gethostbyaddr(ip)[0]
            return hostname
        except:
            return "Unknown"
            
    def identify_device_type(self, ip):
        """Identify device type based on hostname, ports, and behavior"""
        hostname = self.get_hostname(ip).lower()
        open_ports = self.scan_common_ports(ip)
        
        # Check for Jetson-specific indicators
        if any(jetson_indicator in hostname for jetson_indicator in ['jetson', 'nano', 'orin', 'xavier']):
            if 'orin' in hostname:
                return "Jetson Orin (8GB)"
            elif 'nano' in hostname:
                return "Jetson Nano (2GB)"
            else:
                return "Jetson Device"
        
        # Check for common Jetson ports and services
        if 22 in open_ports:  # SSH commonly enabled on Jetson
            if any(port in open_ports for port in [8000, 8080, 5000]):
                return "Potential Jetson Device"
        
        # Check if it matches known IP patterns
        if ip.endswith('.100'):
            return "Possible Jetson Orin 8GB"
        elif ip.endswith('.102'):
            return "Possible Jetson Nano 2GB"
            
        return "Unknown Device"
        
    def scan_subnet(self, subnet):
        """Scan entire subnet for devices"""
        print(f"   🔍 Scanning subnet {subnet}...")
        devices_found = []
        
        # Scan key IPs first (faster for common setups)
        priority_ips = []
        try:
            network = ipaddress.IPv4Network(subnet, strict=False)
            # Check gateway + common device IPs
            for last_octet in [1, 100, 101, 102, 200, 201, 202]:
                try:
                    ip = network.network_address + last_octet
                    if ip in network:
                        priority_ips.append(ip)
                except:
                    pass
        except:
            pass
            
        # Scan priority IPs first
        for ip in priority_ips:
            device = self.scan_device(ip)
            if device:
                devices_found.append(device)
                print(f"      ✅ Found device at {ip}")
        
        # If we found devices, return early (for speed)
        if devices_found:
            return devices_found
            
        # Full subnet scan if no devices found in priority range
        print(f"   🔍 Full subnet scan of {subnet}...")
        try:
            network = ipaddress.IPv4Network(subnet, strict=False)
            for ip in network.hosts():
                if ip not in priority_ips:  # Skip already scanned IPs
                    device = self.scan_device(ip)
                    if device:
                        devices_found.append(device)
                        print(f"      ✅ Found device at {ip}")
        except Exception as e:
            print(f"   ❌ Error scanning subnet {subnet}: {e}")
            
        return devices_found
        
    def scan_network(self):
        """Scan all network interfaces for Jetson devices"""
        print("🌐 JETSON NETWORK DISCOVERY - FIXED VERSION")
        print("="*60)
        print(f"⏰ Scan Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Get network interfaces
        print("🔍 Detecting network interfaces...")
        self.network_interfaces = self.get_network_interfaces()
        
        if not self.network_interfaces:
            print("❌ No network interfaces found!")
            return
            
        print("📡 Available Network Interfaces:")
        for iface in self.network_interfaces:
            print(f"   • {iface['interface']}: {iface['ip']} ({iface['network']})")
        print()
        
        # Clear previous results
        self.discovered_devices = []
        
        # Scan each network
        print("🔍 Scanning networks for Jetson devices...")
        for iface in self.network_interfaces:
            subnet = iface['network']
            print(f"\n📡 Scanning {iface['interface']} network: {subnet}")
            
            devices = self.scan_subnet(subnet)
            self.discovered_devices.extend(devices)
                
        print()
        self.display_results()
        
    def display_results(self):
        """Display scan results"""
        print("📊 NETWORK SCAN RESULTS:")
        print("-"*50)
        
        if not self.discovered_devices:
            print("   ❌ No devices found on any network")
            print()
            print("🔧 TROUBLESHOOTING STEPS:")
            print("   1. Ensure Jetson devices are powered on")
            print("   2. Check all Ethernet cables are connected")
            print("   3. Wait 2-3 minutes for devices to fully boot")
            print("   4. Verify devices are on the same network as laptop")
            print("   5. Check if devices have WiFi enabled instead of Ethernet")
            return
        
        jetson_count = 0
        for device in self.discovered_devices:
            status_icon = "🟢"
            device_type = device['device_type']
            
            # Check if it's likely a Jetson
            is_jetson = any(keyword in device_type.lower() for keyword in ['jetson', 'orin', 'nano'])
            if is_jetson:
                jetson_count += 1
                status_icon = "🔥"
            
            print(f"   {status_icon} {device_type}: {device['ip']}")
            print(f"      🌐 Hostname: {device['hostname']}")
            print(f"      ⚡ Ping: {device['ping_time']}")
            
            ssh_status = "✅ Available" if device['ssh_available'] else "❌ Not ready"
            print(f"      🔐 SSH: {ssh_status}")
            
            if device['open_ports']:
                print(f"      📡 Open ports: {', '.join(map(str, device['open_ports']))}")
            
            print()
            
        print("📈 DISCOVERY SUMMARY:")
        print(f"   🔥 Potential Jetson Devices: {jetson_count}")
        print(f"   🌐 Total Devices Found: {len(self.discovered_devices)}")
        print()
        
        if jetson_count > 0:
            print("🚀 NEXT STEPS:")
            print("   1. Verify device identification")
            print("   2. Update IP addresses in configuration files")
            print("   3. Test SSH connections to confirmed Jetson devices")
            print("   4. Deploy PB2S brain cores")
        else:
            print("⚠️  NO JETSON DEVICES DETECTED:")
            print("   • Review device identification above")
            print("   • Check if devices are using different hostnames")
            print("   • Verify Jetson devices are properly networked")

def main():
    """Main execution function"""
    print("🚀 Initializing Fixed Jetson Network Discovery...")
    print()
    
    discovery = JetsonNetworkDiscoveryFixed()
    discovery.scan_network()

if __name__ == "__main__":
    main()