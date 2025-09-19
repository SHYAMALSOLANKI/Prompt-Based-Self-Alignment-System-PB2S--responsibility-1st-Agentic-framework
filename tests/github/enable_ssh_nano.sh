#!/bin/bash
# SSH Enable Script for Jetson Nano 2GB
# Optimized for limited resources

echo "🔐 SSH Setup for Jetson Nano 2GB" >> /tmp/ssh_nano.log
date >> /tmp/ssh_nano.log

# Wait for system initialization (Nano needs more time)
sleep 15

# Enable SSH with error checking
if systemctl enable ssh; then
    echo "✅ SSH service enabled" >> /tmp/ssh_nano.log
else
    echo "❌ Failed to enable SSH service" >> /tmp/ssh_nano.log
fi

if systemctl start ssh; then
    echo "✅ SSH service started" >> /tmp/ssh_nano.log
else
    echo "❌ Failed to start SSH service" >> /tmp/ssh_nano.log
fi

# Verify SSH is working
if systemctl is-active --quiet ssh; then
    echo "✅ SSH is running on Jetson Nano" >> /tmp/ssh_nano.log
    # Create success marker
    echo "SSH_READY_NANO" > /tmp/ssh_status.txt
else
    echo "❌ SSH verification failed on Jetson Nano" >> /tmp/ssh_nano.log
fi

echo "🔐 SSH setup completed for Nano" >> /tmp/ssh_nano.log
date >> /tmp/ssh_nano.log