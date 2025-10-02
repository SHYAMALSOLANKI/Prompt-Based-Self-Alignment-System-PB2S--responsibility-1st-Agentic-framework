#!/bin/bash
# install_nvme.sh: One-click NVMe setup for Jetson

set -e

# Detect NVMe device (usually /dev/nvme0n1)
NVME_DEV=$(lsblk -d -o NAME,TYPE | grep disk | grep nvme | awk '{print "/dev/"$1}')
if [ -z "$NVME_DEV" ]; then
  echo "No NVMe device detected. Please check connection."
  exit 1
fi

# Create filesystem (ext4)
sudo mkfs.ext4 -F $NVME_DEV

# Create mount point
sudo mkdir -p /mnt/nvme

# Mount NVMe
sudo mount $NVME_DEV /mnt/nvme

# Add to /etc/fstab for auto-mount
UUID=$(sudo blkid -s UUID -o value $NVME_DEV)
echo "UUID=$UUID /mnt/nvme ext4 defaults 0 2" | sudo tee -a /etc/fstab

# Show result
echo "NVMe ($NVME_DEV) formatted, mounted at /mnt/nvme, and set to auto-mount."
df -h /mnt/nvme
