@echo off
title Home AI Brain Network - Ultimate Launcher
color 0A

echo.
echo ╔═════════════════════════════════════════════echo 📊 Step 4: Starting Complete PB2S Dashboard...
start "Complete Dashboard" cmd /c "streamlit run complete_pb2s_dashboard.py --server.port 8502"
timeout /t 3 >nul

echo 🌐 Opening dashboard in browser...
start http://localhost:8502════════════════╗
echo ║                                                                ║
echo ║        🧠 HOME AI BRAIN NETWORK - ULTIMATE LAUNCHER 🧠        ║
echo ║                                                                ║
echo ║    Your Complete Autonomous AI System with Dashboard          ║
echo ║                                                                ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

:MAIN_MENU
echo 🎯 CHOOSE YOUR OPTION:
echo.
echo [1] 🧠 Launch Brain Only (Test Mode)
echo [2] 🚀 Launch Brain Only (Full Autonomous)
echo [3] 📊 Launch Dashboard Only
echo [4] 🌟 Launch BOTH Brain + Dashboard (Recommended!)
echo [5] 🤖 Launch KoboldCpp + Brain + Dashboard (Complete System)
echo [6] 🔧 System Status Check
echo [7] 📖 View Documentation
echo [8] 🚪 Exit
echo.
set /p choice="Enter your choice (1-8): "

if "%choice%"=="1" goto BRAIN_TEST
if "%choice%"=="2" goto BRAIN_FULL
if "%choice%"=="3" goto DASHBOARD_ONLY
if "%choice%"=="4" goto BRAIN_AND_DASHBOARD
if "%choice%"=="5" goto COMPLETE_SYSTEM
if "%choice%"=="6" goto STATUS_CHECK
if "%choice%"=="7" goto DOCUMENTATION
if "%choice%"=="8" goto EXIT
goto MAIN_MENU

:BRAIN_TEST
echo.
echo 🧪 LAUNCHING BRAIN IN TEST MODE...
echo ═══════════════════════════════════════
echo This will run a 1-minute test of your autonomous brain
echo.
python launch_brain_fixed.py --test
echo.
echo ✅ Brain test completed!
pause
goto MAIN_MENU

:BRAIN_FULL
echo.
echo 🧠 LAUNCHING FULL AUTONOMOUS BRAIN...
echo ═══════════════════════════════════════
echo Your brain will run in full autonomous mode
echo Press Ctrl+C to stop when needed
echo.
python launch_brain_fixed.py
echo.
echo 👋 Brain session ended
pause
goto MAIN_MENU

:DASHBOARD_ONLY
echo.
echo 📊 LAUNCHING COMPLETE PB2S DASHBOARD...
echo ═══════════════════════════════════════
echo Features: Chat + Image Generation + Brain Monitoring
echo URL: http://localhost:8502
echo.
start "" cmd /c "streamlit run complete_pb2s_dashboard.py --server.port 8502"
echo ✅ Complete dashboard started in background
echo 🌐 Opening in browser...
timeout /t 3 >nul
start http://localhost:8502
pause
goto MAIN_MENU

:BRAIN_AND_DASHBOARD
echo.
echo 🌟 LAUNCHING BRAIN + DASHBOARD (INTEGRATED SYSTEM)
echo ═══════════════════════════════════════════════════
echo This will start both components with full integration
echo.

echo 🌉 Step 1: Starting Brain-Dashboard Bridge...
start "Brain Bridge" cmd /c "python brain_dashboard_bridge.py"
echo ✅ Bridge starting...

echo 🔄 Waiting for bridge to initialize...
timeout /t 3 >nul

echo 📊 Step 2: Starting Complete PB2S Dashboard...
start "Complete Dashboard" cmd /c "streamlit run complete_pb2s_dashboard.py --server.port 8502"
echo ✅ Dashboard starting...

echo 🔄 Waiting for dashboard to initialize...
timeout /t 5 >nul

echo 🌐 Opening dashboard in browser...
start http://localhost:8502

echo 🧠 Step 3: Starting Autonomous Brain...
echo ⚡ Brain will connect to dashboard for monitoring
echo.
python launch_brain_fixed.py

echo.
echo 👋 Integrated session ended
pause
goto MAIN_MENU

:COMPLETE_SYSTEM
echo.
echo 🤖 LAUNCHING COMPLETE AI SYSTEM
echo ═══════════════════════════════════
echo This includes: KoboldCpp + Brain + Dashboard + Network Coordinator + Bridge
echo.

echo 🤖 Step 1: Checking KoboldCpp...
python -c "import requests; print('✅ KoboldCpp:', 'ONLINE' if requests.get('http://localhost:5001/v1/models', timeout=3).status_code == 200 else '❌ OFFLINE')" 2>nul || echo ❌ KoboldCpp: OFFLINE - Please start KoboldCpp first

echo 🌉 Step 2: Starting Brain-Dashboard Bridge...
start "Brain Bridge" cmd /c "python brain_dashboard_bridge.py"
timeout /t 2 >nul

echo 🌐 Step 3: Starting Network Coordinator...
start "Network Coordinator" cmd /c "python network_coordinator.py"
timeout /t 2 >nul

echo 📊 Step 4: Starting Simple Dashboard...
start "Brain Dashboard" cmd /c "streamlit run simple_brain_dashboard.py --server.port 8501"
timeout /t 3 >nul

echo 🌐 Opening dashboard in browser...
start http://localhost:8501

echo 🧠 Step 5: Starting Enhanced Brain...
echo ⚡ Full system with LLM enhancement and real-time monitoring
echo.
python launch_brain_fixed.py

echo.
echo 🛑 Complete system session ended
pause
goto MAIN_MENU

:STATUS_CHECK
echo.
echo 🔍 SYSTEM STATUS CHECK
echo ═══════════════════════
echo.

echo 🧠 Brain System:
if exist "launch_brain_fixed.py" (echo ✅ Brain launcher ready) else (echo ❌ Brain launcher missing)
if exist "newborn_brain_core.py" (echo ✅ Brain core ready) else (echo ❌ Brain core missing)

echo.
echo 📊 Dashboard System:
if exist "enhanced_dashboard.py" (echo ✅ Enhanced dashboard ready) else (echo ❌ Dashboard missing)

echo.
echo 🌐 Network System:
if exist "network_coordinator.py" (echo ✅ Network coordinator ready) else (echo ❌ Network coordinator missing)

echo.
echo 🤖 LLM Integration:
python -c "import requests; print('✅ KoboldCpp: ONLINE - Port 5001') if requests.get('http://localhost:5001/v1/models', timeout=3).status_code == 200 else print('❌ KoboldCpp: OFFLINE')" 2>nul || echo ❌ KoboldCpp: OFFLINE
python -c "import requests; print('✅ LM Studio: ONLINE - Port 1234') if requests.get('http://localhost:1234/v1/models', timeout=2).status_code == 200 else print('❌ LM Studio: OFFLINE')" 2>nul || echo ❌ LM Studio: OFFLINE

echo.
echo 📁 Model Files:
if exist "gemma-3-4b-it-Q4_K_M.gguf" (echo ✅ Gemma 3 4B model ready) else (echo ❌ Gemma 3 model missing)
if exist "*.gguf" (echo ✅ GGUF models found) else (echo ❌ No GGUF models)

echo.
echo 🐍 Python Environment:
python --version 2>nul && echo ✅ Python ready || echo ❌ Python not found
pip show streamlit >nul 2>&1 && echo ✅ Streamlit installed || echo ❌ Streamlit missing
pip show torch >nul 2>&1 && echo ✅ PyTorch installed || echo ❌ PyTorch missing

pause
goto MAIN_MENU

:DOCUMENTATION
echo.
echo 📖 DOCUMENTATION
echo ════════════════
echo.
echo Available Documentation:
echo.
if exist "HOME_AI_BRAIN_NETWORK_GUIDE.md" (
    echo ✅ HOME_AI_BRAIN_NETWORK_GUIDE.md - Complete setup guide
) else (
    echo ❌ Main guide missing
)

if exist "MISSION_COMPLETE.md" (
    echo ✅ MISSION_COMPLETE.md - Achievement summary
) else (
    echo ❌ Mission summary missing
)

if exist "ULTIMATE_SUCCESS.md" (
    echo ✅ ULTIMATE_SUCCESS.md - Success celebration
) else (
    echo ❌ Success guide missing
)

echo.
echo 🌐 GitHub Repository:
echo https://github.com/SHYAMALSOLANKI/Prompt-Based-Self-Alignment-System-PB2S--responsibility-1st-Agentic-framework
echo.

set /p doc_choice="Open documentation? (y/n): "
if /i "%doc_choice%"=="y" (
    if exist "HOME_AI_BRAIN_NETWORK_GUIDE.md" start "" "HOME_AI_BRAIN_NETWORK_GUIDE.md"
    if exist "ULTIMATE_SUCCESS.md" start "" "ULTIMATE_SUCCESS.md"
)

pause
goto MAIN_MENU

:EXIT
echo.
echo 👋 Thank you for using the Home AI Brain Network!
echo    Your autonomous brain is ready when you are.
echo.
echo 🎯 Quick Commands for next time:
echo    • Brain Test: python launch_brain_fixed.py --test
echo    • Full Brain: python launch_brain_fixed.py  
echo    • Dashboard:  streamlit run enhanced_dashboard.py
echo.
pause
exit

REM Error handling
:ERROR
echo.
echo ❌ An error occurred. Please check:
echo 1. You're in the correct directory
echo 2. Python virtual environment is activated
echo 3. All required files are present
echo.
pause
goto MAIN_MENU