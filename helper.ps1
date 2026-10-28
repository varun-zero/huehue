param (
    [string]$Arg1,
    [string]$Arg2,
    [string]$Arg3
)

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$dataPath = Join-Path $scriptDir "data.json"

if (-not (Test-Path $dataPath)) {
    Write-Error "data.json not found in $scriptDir"
    exit 1
}

$data = Get-Content $dataPath -Raw | ConvertFrom-Json

# If Arg1 is 'list'
if ($Arg1 -eq "list") {
    $targetSub = if ($Arg2) { $Arg2.ToLower() } else { $null }
    if ($targetSub -in @("subject1", "sub1", "s1")) { $targetSub = "aoa" }
    if ($targetSub -in @("subject2", "sub2", "s2")) { $targetSub = "coa" }
    if ($targetSub -in @("subject3", "sub3", "s3")) { $targetSub = "fsjp" }
    if ($targetSub -and $data.PSObject.Properties[$targetSub]) {
        $label = if ($targetSub -in @("aoa", "coa", "fsjp")) { "Experiments" } else { "Topics" }
        Write-Host "============================================================"
        Write-Host "  $label in '$targetSub'"
        Write-Host "============================================================"
        foreach ($prop in $data.$targetSub.PSObject.Properties) {
            $item = $prop.Value
            $suffix = if ($item.code_type -eq "asm") { " [ASM]" } else { "" }
            if ($item.files -and $item.files.Count -gt 1) {
                $suffix += " ($($item.files.Count) files)"
            }
            Write-Host ("  [Exp {0:D2}]  {1}{2}" -f [int]$prop.Name, $item.title, $suffix)
        }
        Write-Host "============================================================"
    } else {
        $subjects = ($data.PSObject.Properties.Name | Sort-Object) -join ", "
        Write-Host "Available subjects: $subjects"
    }
    exit 0
}

# Resolve subject and topic
$sub = $Arg1
$topicRaw = $Arg2
$isAsm = $false

if ($Arg1 -eq "asm") {
    $sub = $Arg2
    $topicRaw = $Arg3
    $isAsm = $true
} elseif ($Arg1 -in @("show", "code", "get")) {
    $sub = $Arg2
    $topicRaw = $Arg3
} elseif ($Arg3 -eq "asm") {
    $isAsm = $true
}

if (-not $sub -or -not $topicRaw) {
    Write-Host "Usage: .\helper.ps1 <subject> <experiment_number>"
    Write-Host "       .\helper.ps1 asm <subject> <experiment_number>"
    Write-Host "COA 3, 4, 8, 9 are assembly-only."
    Write-Host "Example: .\helper.ps1 coa 1"
    Write-Host "         .\helper.ps1 fsjp 1"
    exit 1
}

$sub = $sub.ToLower()
if ($sub -in @("subject1", "sub1", "s1")) {
    $sub = "aoa"
}
if ($sub -in @("subject2", "sub2", "s2")) {
    $sub = "coa"
}
if ($sub -in @("subject3", "sub3", "s3")) {
    $sub = "fsjp"
}
$expNum = $topicRaw -replace '[^0-9]', ''
if (-not $expNum) { $expNum = $topicRaw }

if ($data.PSObject.Properties[$sub]) {
    $subData = $data.$sub
    $found = $null
    foreach ($prop in $subData.PSObject.Properties) {
        $pName = $prop.Name -replace '[^0-9]', ''
        if ($prop.Name -eq $topicRaw -or $pName -eq $expNum) {
            $found = $prop.Value
            break
        }
    }
    if ($found) {
        if ($found.files -and $found.files.Count -gt 1) {
            Write-Error "This experiment has multiple files. Use helper.py: python helper.py show $sub $expNum"
            exit 1
        }
        if ($isAsm) {
            if ($found.asm) {
                Write-Output $found.asm.Trim()
                exit 0
            }
            if ($found.code_type -eq "asm") {
                Write-Output $found.code.Trim()
                exit 0
            }
            Write-Error "No assembly program for this experiment."
            exit 1
        }
        Write-Output $found.code.Trim()
        exit 0
    }
}

Write-Error "Subject '$sub' or Experiment '$topicRaw' not found."
exit 1
