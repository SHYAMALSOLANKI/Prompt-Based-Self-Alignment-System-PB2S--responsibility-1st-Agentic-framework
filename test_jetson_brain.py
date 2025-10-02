#!/usr/bin/env python3
"""
PB2S Jetson Brain Communication Test
Test communication with deployed brain core
"""

import socket
import json
import time

def test_brain_communication(jetson_ip="10.143.230.228", brain_port=8765):
    """Test communication with Jetson brain core"""
    print(f"🧠 Testing brain communication with {jetson_ip}:{brain_port}")
    
    try:
        # Connect to brain server
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect((jetson_ip, brain_port))
        
        # Receive brain response
        response = sock.recv(1024).decode()
        brain_data = json.loads(response)
        
        print("✅ BRAIN COMMUNICATION SUCCESS!")
        print(f"Brain Status: {brain_data.get('brain_status')}")
        print(f"Message: {brain_data.get('message')}")
        print(f"Timestamp: {brain_data.get('timestamp')}")
        
        sock.close()
        return True
        
    except Exception as e:
        print(f"❌ Brain communication failed: {e}")
        return False

def ping_jetson(jetson_ip="10.143.230.228"):
    """Ping Jetson to verify connectivity"""
    import subprocess
    result = subprocess.run(['ping', '-n', '1', jetson_ip], 
                          capture_output=True, text=True)
    if result.returncode == 0:
        print(f"✅ Jetson {jetson_ip} is responding to ping")
        return True
    else:
        print(f"❌ Jetson {jetson_ip} not responding to ping")
        return False

def main():
    """Main test function"""
    print("🔍 PB2S Jetson Brain Communication Test")
    print("=" * 45)
    
    jetson_ip = "10.143.230.228"
    
    # Test basic connectivity
    if ping_jetson(jetson_ip):
        print("📡 Basic connectivity: OK")
        
        # Test brain communication
        print("\n🧠 Testing brain core communication...")
        for attempt in range(3):
            print(f"Attempt {attempt + 1}/3...")
            if test_brain_communication(jetson_ip):
                print("\n🎉 JETSON BRAIN CORE IS ONLINE!")
                print("Ready for distributed AI consciousness!")
                break
            else:
                print(f"Attempt {attempt + 1} failed, retrying in 2 seconds...")
                time.sleep(2)
        else:
            print("\n⚠️ Brain communication test failed after 3 attempts")
            print("Brain core may still be starting up...")
    else:
        print("❌ Cannot reach Jetson - check network connection")

if __name__ == "__main__":
    main()