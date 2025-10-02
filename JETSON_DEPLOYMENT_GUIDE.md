# PB2S Jetson Orin Deployment Guide

## System Overview
- **Small Brain**: Jetson Orin 8GB + tinyllama-1.1b LLM
- **Big Brain**: Main server with full reasoning
- **Learning Storage**: Google Drive 200GB sync
- **Core Vocabulary**: 300 essential words + learning expansion

## Hardware Requirements
- Jetson Orin Super Kit (8GB)
- 4GB dedicated attention memory
- SD card/storage for models
- Internet connection for Google Drive sync

## Installation Steps

### 1. Prepare Jetson Orin
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python dependencies
pip install fastapi uvicorn transformers torch streamlit requests paho-mqtt

# Install Google Drive sync tools (optional)
pip install pydrive2
```

### 2. Copy PB2S System
```bash
# Copy all PB2S files to Jetson
scp -r models/ jetson@jetson-orin:~/pb2s/
scp -r gdrive_sync/ jetson@jetson-orin:~/pb2s/
scp pb2s_enhanced_server.py jetson@jetson-orin:~/pb2s/
scp pb2s_model_manager.py jetson@jetson-orin:~/pb2s/
scp pb2s_gdrive_sync.py jetson@jetson-orin:~/pb2s/
```

### 3. Configure for Jetson
Model: tinyllama-1.1b
Configuration: {
  "device": "jetson_orin",
  "memory_limit": "8GB",
  "attention_memory": "4GB",
  "compute_cores": "2048 CUDA cores",
  "model": "tinyllama-1.1b",
  "pb2s_mode": true,
  "optimization": {
    "precision": "FP16",
    "batch_size": 1,
    "max_tokens": 512,
    "attention_optimization": true,
    "memory_efficient": true
  },
  "pb2s_config": {
    "irq_queue_size": 1000,
    "learned_rules_limit": 5000,
    "sal_tag_processing": true,
    "contradiction_detection": true,
    "google_drive_sync": true
  }
}

### 4. Start Services
```bash
# Start PB2S Small Brain
cd ~/pb2s
python pb2s_enhanced_server.py

# The server will run on port 8000
# Dashboard can connect to this endpoint
```

## Testing the System

### Basic Test
```bash
curl -X POST http://localhost:8000/chat \
     -H "Content-Type: application/json" \
     -d '{"message": "What is quantum entanglement?"}'
```

### Expected Response Format
```json
{
  "text": "DRAFT\nQuantum entanglement explanation...\n\nREFLECT\n- Analysis points...\n\nREVISE\nImproved explanation...\n\nLEARNED\nRule for future use",
  "pb2s_proof": {
    "decision": "APPROVE",
    "cycles": 1,
    "audit_ref": "run-20250912-xxxxx",
    "method": "llm_enhanced",
    "model": "tinyllama-1.1b"
  }
}
```

## PB2S Structure Integration

### IRQ Queue Format
```
[YYYY-MM-DD HH:MM] SRC: <source> RULE: <learned rule>
```

### SAL Tags
- Definition: Clear boundaries and constraints
- Claim: Evidence-backed assertions  
- Evidence: Verifiable supporting data
- Contradiction: Logical conflicts identified
- Ambiguity: Unclear elements clarified
- Task: Executable actions with verification

### Learning Flow
1. **Input** → Small Brain (Jetson) processes with tinyllama-1.1b
2. **PB2S Structure** → DRAFT → REFLECT → REVISE → LEARNED
3. **Storage** → Google Drive sync stores patterns and rules
4. **Feedback** → Big Brain receives enhanced patterns
5. **Evolution** → System improves through accumulated learning

## Google Drive Sync Structure
```
gdrive_sync/
├── pb2s_learning/
│   ├── irq_queue/          # Real-time learning entries
│   ├── learned_rules/      # Accumulated wisdom
│   ├── sal_patterns/       # SAL tag patterns
│   ├── training_data/      # Model fine-tuning data
│   ├── contradiction_logs/ # Resolved contradictions
│   ├── model_checkpoints/  # Model updates
│   ├── attention_patterns/ # 4GB attention optimization
│   ├── jetson_logs/       # System performance logs
│   └── big_brain_sync/    # Coordination with main server
```

## Monitoring & Maintenance

### Check System Status
```bash
curl http://localhost:8000/status
```

### Monitor Storage Usage
The system automatically manages the 200GB Google Drive storage limit.

### Update Model
To switch models or update:
```bash
curl -X POST http://localhost:8000/setup_model?model_name=phi-2
```

## Integration with Main Dashboard
Update your dashboard to connect to Jetson Small Brain:
```python
nodes = [
    {"name": "Small Brain (Jetson)", "url": "http://jetson-orin:8000", "role": "🧠 Lightweight LLM reasoning"},
    {"name": "Big Brain", "url": "http://127.0.0.1:8000", "role": "🎯 Full reasoning and coordination"}
]
```

## Troubleshooting

### Common Issues
1. **Memory Error**: Reduce batch_size in Jetson config
2. **Model Loading Fails**: Check model files in models/ directory
3. **Google Drive Sync Issues**: Verify internet connection and credentials
4. **Performance Issues**: Monitor with `nvidia-smi` and adjust attention_memory

### Performance Optimization
- Use FP16 precision for memory efficiency
- Limit max_tokens to 512 for faster responses
- Enable attention optimization in config
- Monitor temperature with `tegrastats`

## Expected Performance
- **Response Time**: 2-5 seconds for typical queries
- **Memory Usage**: ~6GB total (2GB model + 4GB attention)
- **Power Consumption**: ~20W typical, 40W peak
- **Learning Rate**: Continuous with Google Drive sync
