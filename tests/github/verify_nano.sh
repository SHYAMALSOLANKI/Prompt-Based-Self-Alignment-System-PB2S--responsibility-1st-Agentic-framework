#!/bin/bash
# Jetson Nano 2GB Complete Verification
# Optimized for 2GB memory constraints

echo "========================================="
echo "🔍 Jetson Nano 2GB System Verification"
echo "========================================="
date
echo

# System information
echo "📋 Nano System Info:"
echo "Hostname: $(hostname)"
echo "Architecture: $(uname -m)"
echo "Kernel: $(uname -r)"
echo "IP: $(hostname -I)"
echo

# Memory and CPU (critical for Nano)
echo "🧠 Resource Status:"
echo "Memory:"
free -h
echo
echo "CPU Info:"
nproc
cat /proc/cpuinfo | grep "model name" | head -1
echo
echo "Temperature:"
cat /sys/devices/virtual/thermal/thermal_zone*/temp 2>/dev/null | head -1 | awk '{print $1/1000"°C"}' || echo "Temperature monitoring not available"
echo

# Storage
echo "💾 Storage:"
df -h | grep -E "(mmcblk|sda|root)"
echo

# Find brain location
echo "🧠 Brain System Check:"
BRAIN_FOUND=false
for base_path in /media/jetson/* /mnt/* /; do
    if [ -f "$base_path/pb2s_brain/nano_brain.py" ]; then
        echo "✅ Nano brain found at: $base_path"
        echo "   Brain files: $(ls -1 "$base_path/pb2s_brain/" | wc -l)"
        echo "   Models: $(ls -1 "$base_path/models/"*.gguf 2>/dev/null | wc -l)"
        
        # Check model sizes
        echo "   Model details:"
        ls -lh "$base_path/models/"*.gguf 2>/dev/null | while read line; do
            size=$(echo "$line" | awk '{print $5}')
            name=$(basename "$(echo "$line" | awk '{print $NF}')")
            echo "     - $name: $size"
        done
        BRAIN_FOUND=true
        break
    fi
done

if [ "$BRAIN_FOUND" = false ]; then
    echo "❌ Nano brain not found"
    echo "Available directories:"
    ls -la /media/ 2>/dev/null || true
    ls -la /mnt/ 2>/dev/null || true
fi
echo

# SSH Status
echo "🔐 SSH Status:"
if systemctl is-active --quiet ssh; then
    echo "✅ SSH service is running"
    echo "SSH port status:"
    netstat -ln | grep :22 || echo "SSH port not found"
else
    echo "❌ SSH service not running"
    systemctl status ssh --no-pager
fi
echo

# Network connectivity
echo "🌐 Network Test:"
if ping -c 2 8.8.8.8 >/dev/null 2>&1; then
    echo "✅ Internet connectivity OK"
else
    echo "❌ No internet connection"
fi
echo

# Python environment
echo "🐍 Python Environment:"
python3 --version 2>/dev/null || echo "Python3 not found"
echo "Python packages:"
pip3 list 2>/dev/null | grep -E "(torch|numpy|transformers)" || echo "AI packages check failed"
echo

# Process check
echo "🏃 Running Processes:"
ps aux | grep -E "(python|brain)" | grep -v grep | head -5
echo

# Log files
echo "📋 Recent Logs:"
echo "--- Nano Init Log ---"
tail -5 /tmp/nano_init.log 2>/dev/null || echo "No init log"
echo
echo "--- SSH Nano Log ---"
tail -5 /tmp/ssh_nano.log 2>/dev/null || echo "No SSH log"
echo
echo "--- Nano Brain Log ---"
tail -5 /tmp/nano_brain.log 2>/dev/null || echo "No brain log"
echo

# Status files
echo "🎯 Status Markers:"
[ -f /tmp/nano_ready.txt ] && echo "✅ Nano initialization completed" || echo "❌ Nano init not completed"
[ -f /tmp/ssh_status.txt ] && echo "✅ SSH status: $(cat /tmp/ssh_status.txt)" || echo "❌ SSH status unknown"
[ -f /tmp/nano_brain.pid ] && echo "✅ Brain PID: $(cat /tmp/nano_brain.pid)" || echo "❌ Brain PID not found"
echo

echo "========================================="
echo "✅ Nano Verification Complete"
echo "Device Type: Jetson Nano 2GB"
echo "Configuration: Resource-Optimized"
echo "========================================="
date