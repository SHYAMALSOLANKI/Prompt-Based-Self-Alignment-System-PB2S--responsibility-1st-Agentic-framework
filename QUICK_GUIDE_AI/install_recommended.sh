#!/bin/bash
# install_recommended.sh: One-click install of recommended software for Jetson

set -e

# Update system
sudo apt update && sudo apt upgrade -y

# Python & AI libraries
sudo apt install -y python3-pip python3-venv
pip3 install --upgrade pip
pip3 install numpy scipy pandas matplotlib scikit-learn opencv-python torch torchvision

# Jupyter Notebook
pip3 install notebook

# Docker
sudo apt install -y docker.io
sudo usermod -aG docker $USER

# NVIDIA JetPack SDK (if available)
sudo apt install -y nvidia-jetpack || echo "JetPack not available via apt on this system."

# Edge/IoT Tools
sudo apt install -y mosquitto node-red

# Web Browsers
sudo apt install -y firefox chromium-browser

# Text Editors
sudo apt install -y nano vim

# System Utilities
sudo apt install -y htop tmux git

# Finish
echo "All recommended software installed. Please reboot if Docker or JetPack was installed."
