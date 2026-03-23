$ErrorActionPreference = 'Stop'
$script = 'D:\ClawX-Data\tools\gh\scripts\multi_repo_daily_summary.ps1'
$logDir = 'D:\ClawX-Data\logs'
New-Item -ItemType Directory -Force -Path $logDir | Out-Null
$log = Join-Path $logDir 'github-daily-summary.log'

function Write-Log($msg){
  $ts = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'
  "$ts $msg" | Add-Content -Path $log -Encoding UTF8
}

try {
  if(-not (Test-Path $script)){
    throw "script_missing: $script"
  }
  $out = & powershell -NoProfile -ExecutionPolicy Bypass -File $script 2>&1
  if($LASTEXITCODE -ne 0){
    Write-Log "[ERR] script_exit=$LASTEXITCODE output=$($out -join ' | ')"
    exit 1
  }

  $reportPath = ($out | Select-Object -Last 1).ToString().Trim()
  if($reportPath -and (Test-Path $reportPath)){
    Write-Log "[OK] report=$reportPath"
  } else {
    Write-Log "[WARN] no_report_path output=$($out -join ' | ')"
  }
} catch {
  Write-Log "[ERR] $($_.Exception.Message)"
  exit 1
}
