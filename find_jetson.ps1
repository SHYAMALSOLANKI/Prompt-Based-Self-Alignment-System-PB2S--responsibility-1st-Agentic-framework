Param(
  [string]$HostName = 'jetson.local',
  [switch]$Quick
)

$ErrorActionPreference = 'SilentlyContinue'

Write-Host "[PB2S] Trying mDNS: $HostName" -ForegroundColor Cyan
try {
  $resolved = Resolve-DnsName -Name $HostName -Type A -ErrorAction SilentlyContinue
  if (-not $resolved) { $resolved = Resolve-DnsName -Name $HostName -Type AAAA -ErrorAction SilentlyContinue }
  if ($resolved) {
    $ipStr = ($resolved | Where-Object { $_.Type -eq 'A' } | Select-Object -First 1 -ExpandProperty IPAddress)
    if ($ipStr) {
      Write-Host "[PB2S] Resolved $HostName -> $ipStr" -ForegroundColor Green
      $ip = [System.Net.IPAddress]::Parse($ipStr)
    }
  } else {
    Write-Host "[PB2S] mDNS resolution failed." -ForegroundColor Yellow
  }
} catch {}

function Test-SSH($addr) {
  try {
    $t = New-Object System.Net.Sockets.TcpClient
    $iar = $t.BeginConnect($addr,22,$null,$null)
    $ok = $iar.AsyncWaitHandle.WaitOne(800)
    $t.Close()
    return $ok
  } catch { return $false }
}

if ($ip) {
  $addr = $ip.IPAddressToString
  $ssh = Test-SSH $addr
  $color = if ($ssh) { 'Green' } else { 'Yellow' }
  Write-Host "[PB2S] SSH on ${addr}: ${ssh}" -ForegroundColor $color
  return
}

Write-Host "[PB2S] Checking ARP table for likely new devices..." -ForegroundColor Cyan
$neighbors = Get-NetNeighbor -AddressFamily IPv4 |
  Where-Object {
    ($_.State -in @('Reachable','Stale')) -and (
      ($_.IPAddress -match '^(10\.|192\.168\.|172\.(1[6-9]|2[0-9]|3[0-1])\.)') -or
      ($_.IPAddress -match '^169\.254\.')
    ) -and ($_.IPAddress -notmatch '\.0$') -and ($_.IPAddress -notmatch '\.255$')
  } |
  Sort-Object IPAddress

$found = $false
foreach ($n in $neighbors) {
  if ($Quick) { break }
  $addr = $n.IPAddress.ToString()
  $ssh = Test-SSH $addr
  if ($ssh) {
    $found = $true
    Write-Host "[PB2S] Candidate Jetson IP: ${addr} (SSH open)" -ForegroundColor Green
  }
}

if (-not $found) {
  Write-Host "[PB2S] No SSH-open private IPs found via ARP. Check your router's DHCP client list for NVIDIA/Jetson and try: ssh ubuntu@<IP>" -ForegroundColor Yellow
}

Write-Host "[PB2S] If nothing found: open your router's DHCP client list and look for NVIDIA/Jetson vendor entries. Then: ssh ubuntu@<IP>" -ForegroundColor Yellow
