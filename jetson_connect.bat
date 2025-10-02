@echo off
set JETSON_IP=10.224.0.138
<<<<<<< HEAD
set JETSON_USER=your_jetson_username
=======
set JETSON_USER=shyamal
>>>>>>> 17c52f8d56fa6c10a0acbe313aa21aff4d1a67f1

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
