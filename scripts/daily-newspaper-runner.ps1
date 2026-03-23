$ErrorActionPreference = 'Stop'
$logDir = 'D:\ClawX-Data\logs'
New-Item -ItemType Directory -Force -Path $logDir | Out-Null
$log = Join-Path $logDir 'daily-newspaper.log'
$script = 'C:\Users\17844\.openclaw\workspace\skills\daily-newspaper\scripts\fetch_news.py'

function Write-Log($msg){
  $ts = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'
  "$ts $msg" | Add-Content -Path $log -Encoding UTF8
}

try {
  $env:PYTHONIOENCODING='utf-8'
  Set-Location 'C:\Users\17844\.openclaw\workspace\skills\daily-newspaper'
  $out = & uv run python $script 2>&1
  if($LASTEXITCODE -ne 0){
    Write-Log "[ERR] exit=$LASTEXITCODE output=$($out -join ' | ')"
    exit 1
  }
  $jsonLine = ($out | Where-Object { $_ -match '^\{.*\}$' } | Select-Object -Last 1)
  if($jsonLine){
    Write-Log "[OK] $jsonLine"
  } else {
    Write-Log "[OK] generated (no json line)"
  }
} catch {
  Write-Log "[ERR] $($_.Exception.Message)"
  exit 1
}
