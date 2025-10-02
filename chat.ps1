Param(
  [Parameter(Mandatory=$true)][string]$Message,
  [int]$Port
)

$ErrorActionPreference = 'Stop'

if (-not $Port) {
  foreach ($p in 8001,8000) {
    try {
      $r = Invoke-RestMethod -Uri "http://127.0.0.1:$p/status" -TimeoutSec 2
      if ($r.ok) { $Port = $p; break }
    } catch {}
  }
}

if (-not $Port) {
  Write-Host "[PB2S] No server detected on 8001/8000. Start it with run_ultra_simple.ps1" -ForegroundColor Red
  exit 1
}

$body = @{ message = $Message; max_cycles = 1 } | ConvertTo-Json
$resp = Invoke-RestMethod -Method POST -Uri "http://127.0.0.1:$Port/chat" -ContentType 'application/json' -Body $body

# Print only the text section for readability
if ($resp -and $resp.text) {
  $resp.text
} else {
  $resp | ConvertTo-Json -Depth 6
}
