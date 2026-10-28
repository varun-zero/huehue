# helper.ps1 -- PowerShell helper for Full Stack Java Programming (FSJP)

param (
    [string]$Arg1,
    [string]$Arg2,
    [string]$Arg3,
    [string]$Arg4
)

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$candidates = @(
    (Join-Path $scriptDir "data.json"),
    (Join-Path $scriptDir "helper\data.json"),
    (Join-Path $PWD "data.json"),
    (Join-Path $PWD "helper\data.json"),
    (Join-Path $env:USERPROFILE "helper\data.json"),
    (Join-Path $env:USERPROFILE "data.json")
)

$dataPath = $null
foreach ($c in $candidates) {
    if (Test-Path $c) {
        $dataPath = $c
        break
    }
}

if (-not $dataPath) {
    Write-Error "data.json not found in $scriptDir or candidate paths"
    exit 1
}

$data = Get-Content $dataPath -Raw | ConvertFrom-Json
$defaultSubject = "fsjp"

# Handle 'list' command
if ($Arg1 -eq "list") {
    $targetSub = if ($Arg2) { $Arg2.ToLower() } else { $defaultSubject }
    if ($targetSub -in @("subject3", "sub3", "s3", "java")) { $targetSub = "fsjp" }
    
    if ($data.PSObject.Properties[$targetSub]) {
        Write-Host "============================================================"
        Write-Host "  Experiments in '$targetSub' (Full Stack Java Programming)"
        Write-Host "============================================================"
        foreach ($prop in $data.$targetSub.PSObject.Properties) {
            $item = $prop.Value
            $suffix = ""
            if ($item.files -and $item.files.Count -gt 1) {
                $suffix = " ($($item.files.Count) files)"
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

# Resolve command vs direct arguments
# Examples:
# .\helper.ps1 6
# .\helper.ps1 fsjp 6
# .\helper.ps1 fsjp 8 1
# .\helper.ps1 show fsjp 6
$cmd = $null
$sub = $null
$expArg = $null
$fileArg = $null

if ($Arg1 -in @("show", "code", "get")) {
    $cmd = "show"
    if ($Arg2 -match '^\d+$' -or $Arg2 -match '^(exp|q)\d+$') {
        $sub = $defaultSubject
        $expArg = $Arg2
        $fileArg = $Arg3
    } else {
        $sub = $Arg2
        $expArg = $Arg3
        $fileArg = $Arg4
    }
} elseif ($Arg1 -eq "write" -or $Arg1 -eq "copy") {
    $cmd = $Arg1
    if ($Arg2 -match '^\d+$' -or $Arg2 -match '^(exp|q)\d+$') {
        $sub = $defaultSubject
        $expArg = $Arg2
        $fileArg = $Arg3
    } else {
        $sub = $Arg2
        $expArg = $Arg3
        $fileArg = $Arg4
    }
} else {
    $cmd = "show"
    if ($Arg1 -match '^\d+$' -or $Arg1 -match '^(exp|q)\d+$') {
        $sub = $defaultSubject
        $expArg = $Arg1
        $fileArg = $Arg2
    } else {
        $sub = $Arg1
        $expArg = $Arg2
        $fileArg = $Arg3
    }
}

if (-not $expArg) {
    Write-Host "Usage: .\helper.ps1 fsjp <exp_number> [file_number|all]"
    Write-Host "       .\helper.ps1 <exp_number> [file_number|all]"
    Write-Host "       .\helper.ps1 list"
    Write-Host "Example: .\helper.ps1 6"
    Write-Host "         .\helper.ps1 fsjp 8 1"
    exit 1
}

$sub = if ($sub) { $sub.ToLower() } else { $defaultSubject }
if ($sub -in @("subject3", "sub3", "s3", "java")) {
    $sub = "fsjp"
}

$expNum = $expArg -replace '[^0-9]', ''
if (-not $expNum) { $expNum = $expArg }

if (-not $data.PSObject.Properties[$sub]) {
    Write-Error "Subject '$sub' not found in data.json."
    exit 1
}

$subData = $data.$sub
$found = $null
foreach ($prop in $subData.PSObject.Properties) {
    $pName = $prop.Name -replace '[^0-9]', ''
    if ($prop.Name -eq $expArg -or $pName -eq $expNum) {
        $found = $prop.Value
        break
    }
}

if (-not $found) {
    Write-Error "Experiment '$expArg' not found in subject '$sub'."
    exit 1
}

# Resolve files
$files = @()
if ($found.files -and $found.files.Count -gt 0) {
    $files = $found.files
} else {
    $single = [PSCustomObject]@{
        name = if ($found.filename) { $found.filename } else { "$($sub)_exp_$($expNum).java" }
        language = if ($found.language) { $found.language } else { "java" }
        code = $found.code
    }
    $files = @($single)
}

if ($files.Count -gt 1) {
    if (-not $fileArg) {
        # Check if stdin is interactive
        Write-Host "Exp $([int]$expNum): $($found.title)"
        Write-Host "$($files.Count) files available:`n"
        $fNum = 1
        foreach ($f in $files) {
            $lineCount = ($f.code.Trim().Split("`n").Count)
            Write-Host ("  {0}. {1,-28} {2,-12} {3,3} lines" -f $fNum, $f.name, $f.language.ToUpper(), $lineCount)
            $fNum++
        }
        Write-Host ""
        $fileArg = Read-Host "Select file (1-$($files.Count), all) [1]"
        if (-not $fileArg) { $fileArg = "1" }
    }

    if ($fileArg -eq "all") {
        $idx = 1
        foreach ($f in $files) {
            if ($idx -gt 1) { Write-Host "" }
            Write-Host "===== $idx. $($f.name) ====="
            Write-Output $f.code.Trim()
            $idx++
        }
        exit 0
    }

    $selectedFile = $null
    if ($fileArg -match '^\d+$') {
        $selIdx = [int]$fileArg - 1
        if ($selIdx -ge 0 -and $selIdx -lt $files.Count) {
            $selectedFile = $files[$selIdx]
        }
    } else {
        foreach ($f in $files) {
            if ($f.name.ToLower() -eq $fileArg.ToLower()) {
                $selectedFile = $f
                break
            }
        }
    }

    if ($selectedFile) {
        Write-Output $selectedFile.code.Trim()
        exit 0
    }

    Write-Error "Unknown file '$fileArg'. Available: 1 to $($files.Count)"
    exit 1
}

# Single file
Write-Output $files[0].code.Trim()
exit 0
