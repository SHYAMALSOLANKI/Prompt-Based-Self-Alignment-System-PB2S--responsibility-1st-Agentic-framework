#!/bin/bash
# PB2S Jetson Nano 2GB Edge Brain Preparation Script
# Optimized for 2GB RAM and edge processing

echo "=== PB2S Jetson Nano 2GB Edge Brain Setup Starting ===" >> /tmp/pb2s_edge_setup.log
date >> /tmp/pb2s_edge_setup.log

# Enable SSH
sudo systemctl enable ssh
sudo systemctl start ssh
sudo systemctl enable ssh.socket

# Update system (minimal)
sudo apt update

# Install lightweight Python packages for edge processing
sudo apt install -y python3-pip python3-venv git nano htop

# Create directories for edge brain deployment  
mkdir -p /home/jetson/pb2s_edge_brain
mkdir -p /home/jetson/lightweight_models
mkdir -p /home/jetson/sensor_data
mkdir -p /home/jetson/logs

# Set permissions
sudo chown -R jetson:jetson /home/jetson/pb2s_edge_brain
sudo chown -R jetson:jetson /home/jetson/lightweight_models
sudo chown -R jetson:jetson /home/jetson/sensor_data
sudo chown -R jetson:jetson /home/jetson/logs

# Create edge brain ready marker
echo "Jetson Nano 2GB Edge Brain ready for PB2S deployment" > /home/jetson/EDGE_BRAIN_READY.txt
date >> /home/jetson/EDGE_BRAIN_READY.txt
echo "IP: 10.143.230.90" >> /home/jetson/EDGE_BRAIN_READY.txt
echo "Role: Edge processing, monitoring, lightweight AI" >> /home/jetson/EDGE_BRAIN_READY.txt
echo "SSH: Enabled" >> /home/jetson/EDGE_BRAIN_READY.txt
echo "RAM: 2GB (optimized for lightweight models)" >> /home/jetson/EDGE_BRAIN_READY.txt

# Set up swap for better memory management
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab

echo "=== PB2S Jetson Nano 2GB Edge Brain Setup Complete ===" >> /tmp/pb2s_edge_setup.log
date >> /tmp/pb2s_edge_setup.log