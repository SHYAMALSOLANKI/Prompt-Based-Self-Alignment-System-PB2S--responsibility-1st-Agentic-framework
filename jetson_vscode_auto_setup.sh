#!/bin/bash

# JETSON CONNECTIVITY CHECKER AND VS CODE REMOTE SETUP
# ===================================================
# This script monitors Jetson connectivity and automatically sets up VS Code Remote

JETSON_IP="10.224.0.138"
JETSON_USER="shyamal"
MAX_RETRIES=60  # 5 minutes of checking
RETRY_INTERVAL=5  # seconds

echo "🔍 JETSON CONNECTIVITY MONITOR"
echo "=============================="
echo "Target: $JETSON_USER@$JETSON_IP"
echo "Checking every $RETRY_INTERVAL seconds..."
echo "Max attempts: $MAX_RETRIES"
echo ""

# Function to test connectivity
test_connectivity() {
    ping -c 1 -W 2 $JETSON_IP >/dev/null 2>&1
    return $?
}

# Function to test SSH
test_ssh() {
    ssh -o ConnectTimeout=5 -o BatchMode=yes $JETSON_USER@$JETSON_IP "echo 'SSH OK'" >/dev/null 2>&1
    return $?
}

# Function to setup VS Code Remote
setup_vscode_remote() {
    echo "🚀 Setting up VS Code Remote connection..."
    
    # Create SSH config if it doesn't exist
    SSH_CONFIG="$HOME/.ssh/config"
    mkdir -p ~/.ssh
    
    # Check if jetson-pb2s host already exists
    if ! grep -q "Host jetson-pb2s" "$SSH_CONFIG" 2>/dev/null; then
        echo "📝 Adding Jetson to SSH config..."
        cat >> "$SSH_CONFIG" << EOF

# Jetson PB2S Configuration
Host jetson-pb2s
    HostName $JETSON_IP
    User $JETSON_USER
    Port 22
    IdentitiesOnly yes
    ServerAliveInterval 60
    ServerAliveCountMax 3

EOF
        echo "✅ SSH config updated"
    else
        echo "✅ SSH config already contains jetson-pb2s"
    fi
    
    # Install VS Code Remote extensions if not present
    echo "📦 Installing VS Code Remote extensions..."
    
    if command -v code >/dev/null 2>&1; then
        # Check if extensions are installed
        if ! code --list-extensions | grep -q "ms-vscode-remote.remote-ssh"; then
            echo "Installing Remote-SSH extension..."
            code --install-extension ms-vscode-remote.remote-ssh
        fi
        
        if ! code --list-extensions | grep -q "ms-vscode-remote.vscode-remote-extensionpack"; then
            echo "Installing Remote Development pack..."
            code --install-extension ms-vscode-remote.vscode-remote-extensionpack
        fi
        
        echo "✅ VS Code extensions ready"
    else
        echo "⚠️  VS Code not found in PATH. Please install VS Code first."
        echo "   Download from: https://code.visualstudio.com/"
    fi
}

# Function to transfer PB2S system
transfer_pb2s_system() {
    echo "📦 Transferring complete PB2S system..."
    
    # Create remote directory
    ssh $JETSON_USER@$JETSON_IP "mkdir -p ~/PB2S_Complete_System" 2>/dev/null
    
    # Key files to transfer
    TRANSFER_FILES=(
        "launch_complete_pb2s_system.py"
        "complete_system_diagnostic.py"
        "deploy_complete_pb2s.sh"
        "pb2s_orchestrator.py"
        "brain_llm_connection.py"
        "newborn_brain_core.py"
        "enhanced_dashboard.py"
        "server/"
        "requirements.txt"
        "brain_llm_config.json"
        "VSCODE_REMOTE_JETSON_COMPLETE.md"
    )
    
    echo "Transferring files..."
    for item in "${TRANSFER_FILES[@]}"; do
        if [ -e "$item" ]; then
            echo "  📄 Transferring $item..."
            scp -r -o ConnectTimeout=10 "$item" $JETSON_USER@$JETSON_IP:~/PB2S_Complete_System/ 2>/dev/null || echo "    ⚠️ Failed to transfer $item"
        fi
    done
    
    echo "✅ Transfer attempt complete"
}

# Function to launch VS Code Remote
launch_vscode_remote() {
    echo "🎯 Launching VS Code Remote connection..."
    
    if command -v code >/dev/null 2>&1; then
        echo "Opening VS Code Remote to Jetson..."
        code --remote ssh-remote+jetson-pb2s ~/PB2S_Complete_System
        echo "✅ VS Code Remote launched!"
        echo ""
        echo "📋 Next steps in VS Code:"
        echo "1. Open terminal in VS Code (Ctrl+Shift+\`)"
        echo "2. Run: chmod +x deploy_complete_pb2s.sh"
        echo "3. Run: ./deploy_complete_pb2s.sh"
        echo "4. Run: python3 launch_complete_pb2s_system.py"
        echo ""
        echo "🌐 Access your system at:"
        echo "   API: http://$JETSON_IP:8000"
        echo "   Dashboard: http://$JETSON_IP:8501"
    else
        echo "❌ VS Code not found. Please install VS Code first."
    fi
}

# Main monitoring loop
attempt=1
while [ $attempt -le $MAX_RETRIES ]; do
    echo -n "[$attempt/$MAX_RETRIES] Checking connectivity... "
    
    if test_connectivity; then
        echo "✅ Ping successful!"
        
        echo -n "Testing SSH... "
        if test_ssh; then
            echo "✅ SSH connection successful!"
            echo ""
            echo "🎉 JETSON IS ONLINE AND ACCESSIBLE!"
            echo "=================================="
            
            # Setup VS Code Remote
            setup_vscode_remote
            
            # Transfer PB2S system
            transfer_pb2s_system
            
            # Launch VS Code Remote
            launch_vscode_remote
            
            echo ""
            echo "🚀 Setup complete! Your 4000+ hour PB2S system is ready to deploy on Jetson!"
            exit 0
        else
            echo "❌ SSH failed (checking SSH service...)"
            # Try to give helpful hints
            echo "💡 Troubleshooting tips:"
            echo "   - Ensure SSH is enabled on Jetson: sudo systemctl enable ssh"
            echo "   - Check SSH is running: sudo systemctl start ssh"
            echo "   - Verify firewall settings"
        fi
    else
        echo "❌ No response"
    fi
    
    echo "⏳ Waiting $RETRY_INTERVAL seconds before retry..."
    sleep $RETRY_INTERVAL
    attempt=$((attempt + 1))
done

echo ""
echo "❌ CONNECTIVITY TIMEOUT"
echo "======================"
echo "Jetson did not respond after $MAX_RETRIES attempts."
echo ""
echo "🔧 Manual troubleshooting:"
echo "1. Check Jetson power and network cables"
echo "2. Verify Jetson IP address: ip addr show"
echo "3. Check network connectivity from Jetson: ping 8.8.8.8"
echo "4. Ensure SSH service is running: sudo systemctl status ssh"
echo ""
echo "📞 When Jetson is ready, run this script again or manually:"
echo "   code --remote ssh-remote+$JETSON_USER@$JETSON_IP"