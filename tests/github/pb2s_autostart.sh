#!/bin/bash
# PB2S Auto-Start Script for Self-Contained Brain
# Place in /etc/rc.local or create systemd service

echo "🧠 PB2S Self-Contained Brain Auto-Start" >> /tmp/pb2s_boot.log
date >> /tmp/pb2s_boot.log

# Wait for system to be ready
sleep 30

# Find SD card mount point
SD_MOUNT=$(mount | grep -E "(mmcblk|sda)" | grep -v "boot" | head -1 | awk '{print $3}')

if [ -z "$SD_MOUNT" ]; then
    echo "❌ SD card not found" >> /tmp/pb2s_boot.log
    exit 1
fi

echo "📁 SD card found at: $SD_MOUNT" >> /tmp/pb2s_boot.log

# Check if brain exists on SD card
if [ -f "$SD_MOUNT/pb2s_brain/self_contained_brain.py" ]; then
    echo "✅ Brain found on SD card, starting..." >> /tmp/pb2s_boot.log
    
    # Run as jetson user
    sudo -u jetson python3 "$SD_MOUNT/pb2s_brain/self_contained_brain.py" >> /tmp/pb2s_boot.log 2>&1 &
    
    echo "🚀 Brain started successfully" >> /tmp/pb2s_boot.log
else
    echo "❌ Brain not found on SD card" >> /tmp/pb2s_boot.log
fi

date >> /tmp/pb2s_boot.log