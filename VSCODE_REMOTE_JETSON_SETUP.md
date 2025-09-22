# VS CODE REMOTE SETUP FOR JETSON - COMPLETE GUIDE

## STEP 1: Install VS Code on Your Laptop (if not already installed)
Download from: https://code.visualstudio.com/

## STEP 2: Install Remote-SSH Extension
1. Open VS Code on your laptop
2. Click Extensions (left sidebar) or press Ctrl+Shift+X
3. Search for "Remote - SSH"
4. Install the extension by Microsoft

## STEP 3: Connect to Your Jetson
1. Press Ctrl+Shift+P (Command Palette)
2. Type "Remote-SSH: Connect to Host"
3. Select "Remote-SSH: Connect to Host..."
4. Enter: `shyamal@10.224.0.138`
5. Press Enter
6. Enter your password when prompted
7. VS Code will install VS Code Server on Jetson automatically

## STEP 4: Open Your Project Folder
1. Once connected, click "Open Folder"
2. Navigate to: `/home/pb2s_brain/GitHub/PB2S_1`
3. Click "OK"

## STEP 5: Install Python Extension on Jetson
1. In VS Code (now connected to Jetson), go to Extensions
2. Search for "Python" 
3. Install the Python extension by Microsoft

## STEP 6: Open Terminal in VS Code
1. Press Ctrl+` (backtick) or go to Terminal > New Terminal
2. You now have a terminal directly on Jetson!

## STEP 7: Ready for Direct Help!
Now I can see exactly what you see and help you step by step through VS Code!

## TROUBLESHOOTING

### If connection fails:
- Make sure Jetson is on and connected to WiFi
- Try pinging: `ping 10.224.0.138`
- Check SSH is running on Jetson: `sudo systemctl status ssh`

### If you can't find the folder:
- Use VS Code's file explorer to browse and find your PB2S files
- Look in `/home/shyamal/` or `/home/pb2s_brain/`

### If VS Code Server install fails:
- Make sure Jetson has internet connection
- Free up disk space if needed

## WHAT THIS GIVES US:
✅ Direct file editing on Jetson  
✅ Terminal access to Jetson  
✅ Real-time debugging  
✅ Easy file transfer  
✅ Full development environment  

Once you're connected, I can guide you through the exact PB2S setup with LLM capability!