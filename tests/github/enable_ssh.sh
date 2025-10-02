#!/bin/bash
# Auto-enable SSH on Jetson boot
sudo systemctl enable ssh
sudo systemctl start ssh
sudo systemctl enable ssh.socket
echo "SSH enabled successfully" >> /tmp/ssh_enable.log