# JETSON RESCUE GUIDE - GET RUNNING TODAY

## STEP-BY-STEP JETSON SETUP (NO CODING KNOWLEDGE NEEDED)

### STEP 1: Check Your Current Location
Open terminal on Jetson and type:
```bash
pwd
```
This shows where you are right now.

### STEP 2: Go to Your PB2S_1 Folder
Based on your screenshots, type exactly this:
```bash
cd /home/pb2s_brain/GitHub/PB2S_1
```

### STEP 3: Check Files Are There
Type:
```bash
ls
```
You should see files like: requirements.txt, README.md, server folder, etc.

### STEP 4: Install Python Packages (THE RIGHT WAY)
Type exactly this (note the "s" in requirements):
```bash
pip3 install -r requirements.txt
```

### STEP 5: If Step 4 Fails, Install Individual Packages
Type these one by one:
```bash
pip3 install fastapi
pip3 install uvicorn
pip3 install aiohttp
pip3 install asyncio-mqtt
pip3 install websockets
pip3 install openai
pip3 install scikit-learn
pip3 install opencv-python
pip3 install matplotlib
pip3 install numpy
pip3 install pandas
```

### STEP 6: Start the PB2S Server
Type:
```bash
python3 -c "import uvicorn; uvicorn.run('server.main:app', host='0.0.0.0', port=8000)"
```

### STEP 7: Test From Your Laptop
Open Command Prompt on your laptop and type:
```bash
curl -X POST http://10.224.0.138:8000/chat -H "Content-Type: application/json" -d "{\"message\": \"Hello PB2S brain!\"}"
```

## IF ANYTHING FAILS:

### Problem: "No such file or directory"
- Make sure you're in the right folder: `/home/pb2s_brain/GitHub/PB2S_1`
- Check the folder exists: `ls /home/pb2s_brain/GitHub/`

### Problem: "Permission denied"
- Add `sudo` before the command: `sudo pip3 install -r requirements.txt`

### Problem: "Module not found"
- Install packages individually (see Step 5 above)

### Problem: "Port already in use"
- Kill existing processes: `sudo pkill -f uvicorn`
- Try again

## EMERGENCY BACKUP PLAN

If nothing works, create a simple test:

1. Create a test file:
```bash
echo 'print("Jetson is working!")' > test.py
```

2. Run it:
```bash
python3 test.py
```

If this works, Python is fine and we can debug the PB2S installation.

## CONTACT POINTS
- IP Address: 10.224.0.138
- Username: shyamal
- Main Folder: /home/pb2s_brain/GitHub/PB2S_1

You WILL get this working today. Follow these steps exactly and let me know where you get stuck.
