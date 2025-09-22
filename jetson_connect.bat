@echo off
set JETSON_IP=10.224.0.138
set JETSON_USER=your_jetson_username

echo Checking connectivity to Jetson Orin at %JETSON_IP% ...
ping -n 4 %JETSON_IP%
if errorlevel 1 (
    echo [ERROR] Jetson Orin is not reachable. Check WiFi, IP, and firewall settings.
    pause
    exit /b 1
) else (
    echo [OK] Jetson Orin is reachable.
)

echo Attempting SSH connection...
ssh %JETSON_USER%@%JETSON_IP%
if errorlevel 1 (
    echo [ERROR] SSH connection failed. Check credentials and SSH service on Jetson.
    pause
    exit /b 1
) else (
    echo [OK] SSH connection established.
)

pause
