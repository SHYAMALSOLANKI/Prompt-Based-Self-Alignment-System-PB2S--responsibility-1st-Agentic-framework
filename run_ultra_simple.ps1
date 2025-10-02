Param(
  [int]$Port = 8001
)

$ErrorActionPreference = 'Stop'
Write-Host "[PB2S] Launching ultra_simple_chat on port $Port" -ForegroundColor Cyan

# Ensure venv
if (-not (Test-Path ".\.venv")) {
  Write-Host "[PB2S] Creating venv..." -ForegroundColor Yellow
  python -m venv .venv
}

. .\.venv\Scripts\Activate.ps1

# Install minimal deps
if (-not (Test-Path ".\requirements-ultrasimple.txt")) {
  Write-Host "[PB2S] requirements-ultrasimple.txt missing" -ForegroundColor Red
  exit 1
}
pip install --disable-pip-version-check -r requirements-ultrasimple.txt | Out-Null

# Auto-pick free port if requested one is busy
$inUse = (netstat -ano | Select-String ":$Port\s").Length -gt 0
if ($inUse) {
  Write-Host "[PB2S] Port $Port busy; trying 8001 then 8000..." -ForegroundColor Yellow
  foreach ($p in 8001,8000,8002,8010) {
    $busy = (netstat -ano | Select-String ":$p\s").Length -gt 0
    if (-not $busy) { $Port = $p; break }
  }
}

Write-Host "[PB2S] Using port $Port" -ForegroundColor Green

# Run server
python -m uvicorn ultra_simple_chat:app --host 0.0.0.0 --port $Port
