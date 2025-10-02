# VS Code Remote Setup for Jetson - Complete Guide

## Step 1: Test Connectivity (Run This First)

```bash
# From laptop - test if Jetson is reachable
ping -c 3 10.224.0.138

# Test SSH connectivity  
ssh -o ConnectTimeout=10 shyamal@10.224.0.138 "echo 'Jetson is ready'"
```

## Step 2: Install VS Code Remote Extensions (On Laptop)

### Option A: Install from VS Code
1. Open VS Code
2. Go to Extensions (Ctrl+Shift+X)
3. Search and install:
   - **Remote - SSH** (ms-vscode-remote.remote-ssh)
   - **Remote Development** (ms-vscode-remote.vscode-remote-extensionpack)

### Option B: Install via Command Line
```bash
# Install Remote SSH extension
code --install-extension ms-vscode-remote.remote-ssh

# Install full Remote Development pack
code --install-extension ms-vscode-remote.vscode-remote-extensionpack
```

## Step 3: Configure SSH Connection

### Add Jetson to SSH Config
```bash
# Edit SSH config file
code ~/.ssh/config
```

Add this configuration:
```
Host jetson-pb2s
    HostName 10.224.0.138
    User shyamal
    Port 22
    IdentitiesOnly yes
    # Optional: Add your SSH key path
    # IdentityFile ~/.ssh/id_rsa
```

## Step 4: Connect VS Code to Jetson

### Method 1: Via Command Palette
1. Press `Ctrl+Shift+P`
2. Type "Remote-SSH: Connect to Host"
3. Select "jetson-pb2s" (or enter `shyamal@10.224.0.138`)
4. Enter password when prompted
5. VS Code will install VS Code Server on Jetson automatically

### Method 2: Via Command Line
```bash
# Connect directly from terminal
code --remote ssh-remote+jetson-pb2s
```

## Step 5: Setup Jetson for Development

Once connected via VS Code Remote, run these commands in VS Code terminal:

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python development tools
sudo apt install -y python3-pip python3-venv python3-dev

# Install essential development packages
sudo apt install -y git curl wget htop tree

# Install VS Code server dependencies
sudo apt install -y build-essential

# Create workspace directory
mkdir -p ~/PB2S_Workspace
cd ~/PB2S_Workspace
```

## Step 6: Transfer Your Complete PB2S System

### Option A: Via VS Code (Recommended)
1. In VS Code connected to Jetson
2. Open terminal (`Ctrl+Shift+` `)
3. Clone or transfer your repository:

```bash
# If you have git access
git clone https://github.com/SHYAMALSOLANKI/Prompt-Based-Self-Alignment-System-PB2S--responsibility-1st-Agentic-framework.git

# Or create the directory and transfer files via VS Code file explorer
mkdir -p PB2S_Complete_System
cd PB2S_Complete_System
```

### Option B: Direct Transfer (if SSH works)
```bash
# From laptop - transfer complete system
scp -r /workspaces/Prompt-Based-Self-Alignment-System-PB2S--responsibility-1st-Agentic-framework/* shyamal@10.224.0.138:~/PB2S_Workspace/
```

## Step 7: Install Your Complete PB2S System on Jetson

In VS Code terminal connected to Jetson:

```bash
cd ~/PB2S_Workspace
# If you transferred our deployment script
chmod +x deploy_complete_pb2s.sh
./deploy_complete_pb2s.sh

# Or install manually
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install fastapi uvicorn aiohttp streamlit requests numpy pandas scikit-learn
```

## Step 8: Launch Your 4000+ Hour System on Jetson

```bash
# Start the complete system
python3 launch_complete_pb2s_system.py

# Or individual components
python3 -c "import uvicorn; uvicorn.run('server.main:app', host='0.0.0.0', port=8000)" &
streamlit run enhanced_dashboard.py --server.port 8501 --server.address 0.0.0.0 &
```

## Step 9: Access Your System

From your laptop browser:
- **API Server**: http://10.224.0.138:8000
- **Dashboard**: http://10.224.0.138:8501
- **Chat API**: http://10.224.0.138:8000/chat

Test with:
```bash
curl -X POST http://10.224.0.138:8000/chat \
  -H 'Content-Type: application/json' \
  -d '{"message": "Test complete PB2S system with contradiction detection"}'
```

## Troubleshooting

### If VS Code Remote fails to connect:
1. Check SSH service: `sudo systemctl status ssh`
2. Start SSH if needed: `sudo systemctl start ssh`
3. Check firewall: `sudo ufw status`
4. Verify user permissions

### If VS Code Server installation fails:
```bash
# On Jetson - install dependencies
sudo apt update
sudo apt install -y libc6 libstdc++6 python3

# Clear VS Code server cache
rm -rf ~/.vscode-server
```

### Network Issues:
```bash
# Check network interface
ip addr show

# Check routing
ip route show

# Test internal connectivity
ping 8.8.8.8
```

## Complete Success Indicators

✅ **VS Code Remote Connected**: VS Code shows "SSH: jetson-pb2s" in bottom left
✅ **File System Access**: You can browse Jetson files in VS Code
✅ **Terminal Access**: VS Code terminal runs commands on Jetson
✅ **PB2S System Running**: API responds at http://10.224.0.138:8000
✅ **Dashboard Active**: Streamlit accessible at http://10.224.0.138:8501

Your 4000+ hours of sophisticated PB2S work will then be running on Jetson with full remote development capabilities! 🚀