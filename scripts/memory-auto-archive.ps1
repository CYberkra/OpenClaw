$ErrorActionPreference = 'Stop'
$repo = 'C:\Users\17844\.openclaw\workspace'
$git = 'C:\Program Files (x86)\Git\cmd\git.exe'
$logDir = 'D:\ClawX-Data\logs'
New-Item -ItemType Directory -Force -Path $logDir | Out-Null
$log = Join-Path $logDir 'memory-auto-archive.log'

function Write-Log($msg){
  $ts = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'
  "$ts $msg" | Add-Content -Path $log -Encoding UTF8
}

try {
  Set-Location $repo
  $status = & $git status --porcelain -- memory rules skills docs examples reports 2>$null
  if (-not $status) {
    Write-Log '[NOOP] no changes in memory/rules/skills/docs/examples/reports'
    exit 0
  }

  $date = Get-Date -Format 'yyyy-MM-dd'
  & $git add memory/ rules/ skills/ docs/ examples/ reports/ | Out-Null

  # avoid failing when nothing actually added after pathspec filtering
  $staged = & $git diff --cached --name-only
  if (-not $staged) {
    Write-Log '[NOOP] nothing staged after git add'
    exit 0
  }

  & $git commit -m "Sync: OpenClaw auto-archive $date" | Out-Null
  $commit = (& $git rev-parse --short HEAD).Trim()

  # push best-effort to both remotes
  $pushMemoryOk = $true
  $pushOriginOk = $true
  try { & $git push memory main | Out-Null } catch { $pushMemoryOk = $false; Write-Log "[WARN] git push memory main failed: $($_.Exception.Message)" }
  try { & $git push origin main | Out-Null } catch { $pushOriginOk = $false; Write-Log "[WARN] git push origin main failed: $($_.Exception.Message)" }

  Write-Log "[OK] committed=$commit push_memory=$pushMemoryOk push_origin=$pushOriginOk"
} catch {
  Write-Log "[ERR] $($_.Exception.Message)"
  exit 1
}

