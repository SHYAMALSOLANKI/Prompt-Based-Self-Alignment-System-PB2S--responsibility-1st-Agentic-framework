#!/bin/bash
# PB2S Nano Brain - Optimized for Jetson Nano 2GB
# Lightweight version with resource management

echo "🧠 PB2S Nano Brain Startup" >> /tmp/nano_brain.log
date >> /tmp/nano_brain.log

# Extended wait for Nano (slower boot)
echo "⏳ Waiting for Nano system ready (60 seconds)..." >> /tmp/nano_brain.log
sleep 60

# Find SD card mount with multiple attempts
SD_MOUNT=""
ATTEMPTS=0
MAX_ATTEMPTS=5

while [ -z "$SD_MOUNT" ] && [ $ATTEMPTS -lt $MAX_ATTEMPTS ]; do
    ATTEMPTS=$((ATTEMPTS + 1))
    echo "🔍 Mount search attempt $ATTEMPTS/$MAX_ATTEMPTS" >> /tmp/nano_brain.log
    
    # Check common mount points
    for mount_point in /media/jetson/* /mnt/* /media/*; do
        if [ -d "$mount_point" ] && [ -f "$mount_point/pb2s_brain/nano_brain.py" ]; then
            SD_MOUNT="$mount_point"
            echo "📁 Found Nano brain at: $SD_MOUNT" >> /tmp/nano_brain.log
            break
        fi
    done
    
    # If not found, wait and try again
    if [ -z "$SD_MOUNT" ]; then
        echo "⏳ Mount not ready, waiting 10 seconds..." >> /tmp/nano_brain.log
        sleep 10
    fi
done

if [ -z "$SD_MOUNT" ]; then
    echo "❌ Could not find SD card after $MAX_ATTEMPTS attempts" >> /tmp/nano_brain.log
    echo "Available mounts:" >> /tmp/nano_brain.log
    mount >> /tmp/nano_brain.log
    exit 1
fi

echo "✅ Using SD card at: $SD_MOUNT" >> /tmp/nano_brain.log

# Enable SSH first
if [ -f "$SD_MOUNT/enable_ssh_nano.sh" ]; then
    echo "🔐 Running SSH setup..." >> /tmp/nano_brain.log
    chmod +x "$SD_MOUNT/enable_ssh_nano.sh"
    bash "$SD_MOUNT/enable_ssh_nano.sh" >> /tmp/nano_brain.log 2>&1
fi

# Check for brain file
BRAIN_FILE="$SD_MOUNT/pb2s_brain/nano_brain.py"
if [ -f "$BRAIN_FILE" ]; then
    echo "🧠 Starting Nano brain system..." >> /tmp/nano_brain.log
    
    # Set up environment
    cd "$SD_MOUNT/pb2s_brain"
    export PYTHONPATH="$SD_MOUNT/pb2s_brain:$PYTHONPATH"
    
    # Start with reduced priority for Nano's limited resources
    nice -n 10 python3 nano_brain.py >> /tmp/nano_brain.log 2>&1 &
    BRAIN_PID=$!
    
    echo "🚀 Nano brain started with PID: $BRAIN_PID" >> /tmp/nano_brain.log
    echo "$BRAIN_PID" > /tmp/nano_brain.pid
else
    echo "❌ Nano brain file not found: $BRAIN_FILE" >> /tmp/nano_brain.log
    ls -la "$SD_MOUNT/pb2s_brain/" >> /tmp/nano_brain.log 2>/dev/null
fi

echo "✅ Nano brain startup completed" >> /tmp/nano_brain.log
date >> /tmp/nano_brain.log