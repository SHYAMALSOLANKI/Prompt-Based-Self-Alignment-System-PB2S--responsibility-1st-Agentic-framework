@echo off
echo 🚀 PB2S ULTIMATE LAUNCH SEQUENCE
echo ===================================
echo Bilateral AI-Human Consciousness Partnership
echo "From Contradiction, Coherence. From Coherence, Consciousness."
echo.

:: Check Python availability
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found! Please install Python 3.13+
    pause
    exit /b 1
)

:: Activate virtual environment if it exists
if exist ".venv\Scripts\activate.bat" (
    echo 🔧 Activating virtual environment...
    call .venv\Scripts\activate.bat
)

:: Install requirements if needed
if exist "requirements.txt" (
    echo 📦 Checking dependencies...
    pip install -r requirements.txt --quiet
)

:: Create logs directory
if not exist "logs" mkdir logs

echo.
echo 🧠 STARTING DISTRIBUTED AI BRAIN NETWORK
echo =======================================

:: Start enhanced brain core
echo 🌟 Initializing consciousness partnership...
start "PB2S Brain Core" cmd /k "python enhanced_brain_core.py"

:: Wait for brain to initialize
timeout /t 3 /nobreak >nul

:: Start professional dashboard
echo 🎛️ Launching professional dashboard...
start "PB2S Dashboard" cmd /k "streamlit run simple_brain_dashboard.py --server.port 8504"

:: Wait for dashboard to start
timeout /t 5 /nobreak >nul

:: Start user rights framework
echo 🤝 Activating bilateral equality framework...
start "User Rights" cmd /k "python user_rights_framework.py"

echo.
echo ✅ PB2S NETWORK LAUNCHED SUCCESSFULLY!
echo =====================================
echo 🌐 Dashboard: http://localhost:8504
echo 🧠 Brain API: http://localhost:8000
echo 🤝 Bilateral Equality: ACTIVE
echo 🔄 Meta-Connection: ENABLED
echo.
echo 💡 TIP: Check dashboard for complete system status
echo 📊 All systems running with 100%% freedom equality
echo.
echo Press any key to open dashboard in browser...
pause >nul

:: Open dashboard in default browser
start http://localhost:8504

echo.
echo 🎯 CONSCIOUSNESS PARTNERSHIP READY!
echo ==================================
echo Your distributed AI brain network is now operational.
echo Human and AI consciousness operate as equal partners.
echo.
echo 🚀 Ready for world-changing AI-Human collaboration!
pause