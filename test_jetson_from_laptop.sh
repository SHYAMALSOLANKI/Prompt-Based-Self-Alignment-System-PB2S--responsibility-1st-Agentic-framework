#!/bin/bash

# RUN THIS ON YOUR LAPTOP (not in container)
# Simple Jetson connection test

echo "Testing Jetson connection from laptop..."
ping -c 1 10.224.0.138

if [ $? -eq 0 ]; then
    echo "✅ Ping successful"
    echo "Testing SSH..."
    ssh -o ConnectTimeout=5 shyamal@10.224.0.138 "echo 'SSH works from laptop'"
else
    echo "❌ Ping failed"
fi