#!/bin/bash
# Nano Initialization Script - Corruption Resistant
# This ensures proper file permissions and prevents corruption

echo "🔧 Jetson Nano 2GB Initialization" >> /tmp/nano_init.log
date >> /tmp/nano_init.log

# Wait for filesystem to be fully ready
echo "⏳ Waiting for filesystem ready..." >> /tmp/nano_init.log
sleep 20

# Find the SD card mount point
SD_MOUNT=""
for mount_point in /media/jetson/* /mnt/* /media/*; do
    if [ -d "$mount_point" ] && [ -f "$mount_point/enable_ssh_nano.sh" ]; then
        SD_MOUNT="$mount_point"
        echo "📁 Found SD card at: $SD_MOUNT" >> /tmp/nano_init.log
        break
    fi
done

if [ -z "$SD_MOUNT" ]; then
    echo "❌ SD card not found" >> /tmp/nano_init.log
    exit 1
fi

# Sync filesystem to prevent corruption
sync

# Set proper permissions (avoiding corruption)
echo "🔧 Setting permissions..." >> /tmp/nano_init.log
find "$SD_MOUNT" -name "*.sh" -exec chmod +x {} \; 2>/dev/null || true
find "$SD_MOUNT" -name "*.py" -exec chmod +x {} \; 2>/dev/null || true

# Sync again
sync

# Run SSH setup
if [ -f "$SD_MOUNT/enable_ssh_nano.sh" ]; then
    echo "🔐 Running SSH setup..." >> /tmp/nano_init.log
    bash "$SD_MOUNT/enable_ssh_nano.sh" >> /tmp/nano_init.log 2>&1
fi

# Setup systemd service if available
if [ -f "$SD_MOUNT/pb2s-nano-brain.service" ]; then
    echo "⚙️ Installing systemd service..." >> /tmp/nano_init.log
    sudo cp "$SD_MOUNT/pb2s-nano-brain.service" /etc/systemd/system/ 2>/dev/null || true
    sudo systemctl daemon-reload 2>/dev/null || true
    sudo systemctl enable pb2s-nano-brain.service 2>/dev/null || true
fi

# Final sync to ensure all writes complete
sync

echo "✅ Nano initialization completed" >> /tmp/nano_init.log
date >> /tmp/nano_init.log

# Create ready marker
echo "NANO_READY" > /tmp/nano_ready.txt
date >> /tmp/nano_ready.txt