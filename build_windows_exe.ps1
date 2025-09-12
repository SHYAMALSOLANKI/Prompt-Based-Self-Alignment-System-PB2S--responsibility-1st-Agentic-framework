# PowerShell script to build Windows .exe for PB2S Dashboard

Write-Host "Building Windows .exe for PB2S Dashboard..." -ForegroundColor Green

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "Python is not installed. Please install Python from https://www.python.org/downloads/" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Install PyInstaller if not already installed
Write-Host "Installing PyInstaller..." -ForegroundColor Yellow
pip install pyinstaller

# Install dependencies from requirements.txt
if (Test-Path "requirements.txt") {
    Write-Host "Installing dependencies from requirements.txt..." -ForegroundColor Yellow
    pip install -r requirements.txt
} else {
    Write-Host "requirements.txt not found. Please ensure dependencies are installed manually." -ForegroundColor Red
}

# Build the .exe
if (Test-Path "pb2s_dashboard.py") {
    Write-Host "Building .exe from pb2s_dashboard.py..." -ForegroundColor Yellow
    pyinstaller --onefile --windowed pb2s_dashboard.py
    Write-Host "Build complete! Check the dist/ folder for pb2s_dashboard.exe" -ForegroundColor Green
} elseif (Test-Path "launch_dashboard.py") {
    Write-Host "Building .exe from launch_dashboard.py..." -ForegroundColor Yellow
    pyinstaller --onefile --windowed launch_dashboard.py
    Write-Host "Build complete! Check the dist/ folder for launch_dashboard.exe" -ForegroundColor Green
} else {
    Write-Host "No dashboard script found. Please ensure pb2s_dashboard.py or launch_dashboard.py exists." -ForegroundColor Red
}

Read-Host "Press Enter to exit"