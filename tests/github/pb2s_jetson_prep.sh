#!/bin/bash
# PB2S Jetson Orin 8GB Preparation Script
# This will prepare the Jetson for AI brain deployment

echo "=== PB2S Jetson Preparation Starting ===" >> /tmp/pb2s_setup.log
date >> /tmp/pb2s_setup.log

# Enable SSH
sudo systemctl enable ssh
sudo systemctl start ssh
sudo systemctl enable ssh.socket

# Update system
sudo apt update

# Install Python and required packages
sudo apt install -y python3-pip python3-venv git

# Create directories for brain deployment
mkdir -p /home/jetson/pb2s_brain
mkdir -p /home/jetson/models
mkdir -p /home/jetson/logs

# Set permissions
sudo chown -R jetson:jetson /home/jetson/pb2s_brain
sudo chown -R jetson:jetson /home/jetson/models
sudo chown -R jetson:jetson /home/jetson/logs

# Create ready marker
echo "Jetson Orin 8GB ready for PB2S brain deployment" > /home/jetson/READY_FOR_DEPLOYMENT.txt
date >> /home/jetson/READY_FOR_DEPLOYMENT.txt
echo "IP: 10.143.230.228" >> /home/jetson/READY_FOR_DEPLOYMENT.txt
echo "SSH: Enabled" >> /home/jetson/READY_FOR_DEPLOYMENT.txt

echo "=== PB2S Jetson Preparation Complete ===" >> /tmp/pb2s_setup.log
date >> /tmp/pb2s_setup.log