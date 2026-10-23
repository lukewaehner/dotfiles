# refresh_and_extract.ps1
# Opens the Sector Indices workbook READ-ONLY in Excel so the Bloomberg add-in
# refreshes every BDP formula, waits for the async pulls to settle, then extracts
# the Sector Heatmap / SPAC Scorecard / Warrant Watch tables to tables.json.
# Read-only => never fights a copy the user already has open, and never saves.
param(
  [string]$Workbook = "G:\Shared drives\Interns\Sector Indices\Sector Indices - Testing.xlsx",
  [string]$OutDir = "",
  [int]$MaxWaitSec = 240
)
$ErrorActionPreference = "Stop"
if ([string]::IsNullOrWhiteSpace($OutDir)) { $OutDir = Join-Path (Split-Path $PSScriptRoot -Parent) "out" }
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null
$Log = Join-Path $OutDir "run.log"
$TablesJson = Join-Path $OutDir "tables.json"
$StatusJson = Join-Path $OutDir "status.json"
Set-Content -Path $Log -Value "" -Encoding utf8
function Log($m){ $ts=(Get-Date).ToString("HH:mm:ss"); Add-Content -Path $Log -Value "[$ts] $m" -Encoding utf8 }
Log "START refresh_and_extract"
Log ("Workbook: " + $Workbook)

# ---- helpers ----
function To-Jagged($v){
  if ($null -eq $v) { return @() }
  if (-not ($v -is [Array]) -or $v.Rank -ne 2) { return ,@(,@($v)) }
  $r0 = $v.GetLowerBound(0); $r1 = $v.GetUpperBound(0)
  $c0 = $v.GetLowerBound(1); $c1 = $v.GetUpperBound(1)
  $out = New-Object System.Collections.ArrayList
  for ($r=$r0; $r -le $r1; $r++){
    $row = New-Object System.Collections.ArrayList
    for ($c=$c0; $c -le $c1; $c++){ [void]$row.Add($v.GetValue($r,$c)) }
    [void]$out.Add($row)
  }
  return ,$out
}
function Count-Pending($wb){
  $n = 0
  foreach ($ws in $wb.Worksheets){
    $v = $ws.UsedRange.Value2
    if ($v -is [Array] -and $v.Rank -eq 2){
      foreach ($c in $v){ if ($c -is [string] -and $c -like '*Requesting Data*'){ $n++ } }
    } elseif ($v -is [string]) { if ($v -like '*Requesting Data*'){ $n++ } }
  }
  return $n
}

# ---- main ----
$xl = $null; $wb = $null; $ok = $false; $pending = -1; $settle = -1; $err = ""
try {
  $xl = New-Object -ComObject Excel.Application
  $xl.Visible = $false
  $xl.DisplayAlerts = $false
  $xl.AskToUpdateLinks = $false
  $xl.ScreenUpdating = $false
  Log "Excel COM created; opening workbook read-only"
  $wb = $xl.Workbooks.Open($Workbook, 0, $true)
  $xl.Calculation = -4105
  $xl.CalculateFullRebuild()
  Log "Full rebuild issued; polling for Bloomberg to settle"
  $sw = [System.Diagnostics.Stopwatch]::StartNew()
  while ($true) {
    Start-Sleep -Seconds 8
    $pending = Count-Pending $wb
    $el = [int]$sw.Elapsed.TotalSeconds
    Log ("t=" + $el + "s pending=" + $pending)
    if ($pending -eq 0) { $settle = $el; break }
    if ($el -gt $MaxWaitSec) { $settle = $el; Log "TIMEOUT (still pending)"; break }
    if (($el % 32) -lt 8) { $xl.CalculateFull() }
  }

  $xl.CalculateFull()
  Log "Extracting tables"
  $hm = $wb.Worksheets.Item("Sector Heatmap").UsedRange.Value2
  $sc = $wb.Worksheets.Item("SPAC Scorecard").UsedRange.Value2
  $ww = $wb.Worksheets.Item("Warrant Watch").UsedRange.Value2
  $result = [ordered]@{
    generated_local = (Get-Date).ToString("yyyy-MM-dd HH:mm")
    settle_seconds  = $settle
    pending_left    = $pending
    heatmap   = (To-Jagged $hm)
    scorecard = (To-Jagged $sc)
    warrant   = (To-Jagged $ww)
  }
  $result | ConvertTo-Json -Depth 12 | Out-File -FilePath $TablesJson -Encoding utf8
  $ok = ($pending -eq 0)
  Log ("Wrote " + $TablesJson)
}
catch { $err = $_.Exception.Message; Log ("ERROR: " + $err) }
finally {
  if ($wb) { try { $wb.Close($false) } catch {} }
  if ($xl) { try { $xl.Quit() } catch {} }
  if ($xl) { try { [void][System.Runtime.InteropServices.Marshal]::ReleaseComObject($xl) } catch {} }
  [System.GC]::Collect(); [System.GC]::WaitForPendingFinalizers()
  $status = [ordered]@{ ok=$ok; pending_left=$pending; settle_seconds=$settle; error=$err; generated_local=(Get-Date).ToString("yyyy-MM-dd HH:mm") }
  $status | ConvertTo-Json | Out-File -FilePath $StatusJson -Encoding utf8
  Log ("DONE ok=" + $ok + " pending=" + $pending + " settle=" + $settle + "s")
}
