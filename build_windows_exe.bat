@echo off
echo Building Windows .exe for PB2S Dashboard...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed. Please install Python from https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Install PyInstaller if not already installed
pip install pyinstaller

REM Install dependencies from requirements.txt
if exist requirements.txt (
    pip install -r requirements.txt
) else (
    echo requirements.txt not found. Please ensure dependencies are installed manually.
)

REM Build the .exe
if exist pb2s_dashboard.py (
    pyinstaller --onefile --windowed pb2s_dashboard.py
    echo Build complete! Check the dist/ folder for pb2s_dashboard.exe
) else if exist launch_dashboard.py (
    pyinstaller --onefile --windowed launch_dashboard.py
    echo Build complete! Check the dist/ folder for launch_dashboard.exe
) else (
    echo No dashboard script found. Please ensure pb2s_dashboard.py or launch_dashboard.py exists.
)

pause