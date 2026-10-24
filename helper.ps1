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
    if ($targetSub -and $data.PSObject.Properties[$targetSub]) {
        Write-Host "============================================================"
        Write-Host "  Experiments in '$targetSub'"
        Write-Host "============================================================"
        foreach ($prop in $data.$targetSub.PSObject.Properties) {
            $item = $prop.Value
            Write-Host ("  [{0}]  {1}" -f $item.id, $item.title)
        }
        Write-Host "============================================================"
    } else {
        Write-Host "Available subjects: aoa, subject2, subject3"
    }
    exit 0
}

# Resolve subject and topic
$sub = $Arg1
$topicRaw = $Arg2

if ($Arg1 -in @("show", "code", "get")) {
    $sub = $Arg2
    $topicRaw = $Arg3
}

if (-not $sub -or -not $topicRaw) {
    Write-Host "Usage: .\helper.ps1 <subject> <experiment_number>"
    Write-Host "Example: .\helper.ps1 aoa 1"
    exit 1
}

$sub = $sub.ToLower()
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
        Write-Output $found.code.Trim()
        exit 0
    }
}

Write-Error "Subject '$sub' or Experiment '$topicRaw' not found."
exit 1
