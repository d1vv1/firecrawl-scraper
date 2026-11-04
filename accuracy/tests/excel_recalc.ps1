# Opens each output workbook in Excel, recalculates fully, and fails if any cell holds an error value
# (#REF!, #VALUE!, #DIV/0!, #NAME?, #N/A, #NUM!, #NULL!). Also checks the scoring Summary formulas
# agree with the engine counts and the Module Check weights equal 1.
#   powershell -ExecutionPolicy Bypass -File accuracy/tests/excel_recalc.ps1
$ErrorActionPreference = "Stop"
$out = Join-Path (Split-Path $PSScriptRoot -Parent) "out"
$files = @("allshares_first50_scoring.xlsx", "allshares_field_checks.xlsx", "allshares_reference_ranges.xlsx")
$xl = New-Object -ComObject Excel.Application
$xl.Visible = $false; $xl.DisplayAlerts = $false
$bad = 0
try {
  foreach ($f in $files) {
    $wb = $xl.Workbooks.Open((Join-Path $out $f), 0, $true)
    $xl.CalculateFull()
    $errs = 0; $formulas = 0
    foreach ($ws in $wb.Worksheets) {
      $ur = $ws.UsedRange
      $vals = $ur.Value2
      $hasF = $ur.HasFormula
      if ($hasF -ne $false) {
        try { $fc = $ur.SpecialCells(-4123); $formulas += $fc.Count } catch {}
      }
      try { $ec = $ur.SpecialCells(-4123, 16); $errs += $ec.Count; Write-Host "  $f / $($ws.Name): $($ec.Count) formula errors at $($ec.Address(0,0))" } catch {}
      try { $ec2 = $ur.SpecialCells(2, 16); $errs += $ec2.Count; Write-Host "  $f / $($ws.Name): $($ec2.Count) error constants" } catch {}
    }
    if ($f -eq "allshares_first50_scoring.xlsx") {
      $s = $wb.Worksheets.Item("Summary")
      for ($r = 8; $r -le 18; $r++) {
        $a = $s.Cells.Item($r, 2).Value2; $b = $s.Cells.Item($r, 3).Value2
        if ([double]$a -ne [double]$b) { Write-Host "  Summary row $r ($($s.Cells.Item($r,1).Value2)): formula $a vs engine $b"; $errs++ }
      }
    }
    if ($f -eq "allshares_field_checks.xlsx") {
      $m = $wb.Worksheets.Item("Module Check")
      for ($r = 2; $r -le 4; $r++) {
        $w = [double]$m.Cells.Item($r, 2).Value2
        if ([math]::Abs($w - 1) -gt 1e-9) { Write-Host "  Module Check $($m.Cells.Item($r,1).Value2): $w"; $errs++ }
      }
    }
    Write-Host ("{0}: {1} formulas recalculated, {2} problems" -f $f, $formulas, $errs)
    $bad += $errs
    $wb.Close($false)
  }
} finally {
  $xl.Quit()
  [System.Runtime.InteropServices.Marshal]::ReleaseComObject($xl) | Out-Null
}
if ($bad) { Write-Host "FAIL"; exit 1 } else { Write-Host "OK: zero errors" }
