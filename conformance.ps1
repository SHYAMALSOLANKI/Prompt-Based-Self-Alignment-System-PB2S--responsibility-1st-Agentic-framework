Param(
  [int]$Port
)

$ErrorActionPreference = 'Stop'
. .\.venv\Scripts\Activate.ps1

if (-not $Port) {
  # Detect one of our typical ports
  foreach ($p in 8001,8000) {
    $ok = $false
    try {
      $resp = Invoke-RestMethod -Uri "http://127.0.0.1:$p/status" -TimeoutSec 2
      if ($resp.ok) { $Port = $p; $ok = $true }
    } catch {}
    if ($ok) { break }
  }
}

if (-not $Port) {
  Write-Host "[PB2S] Could not find running server on 8001/8000. Start it first." -ForegroundColor Red
  exit 1
}

Write-Host "[PB2S] Running conformance on port $Port" -ForegroundColor Cyan
python scripts/conformance.py --endpoint "http://127.0.0.1:$Port/chat"
