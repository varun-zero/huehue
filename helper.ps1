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

function Print-TomcatGuide([string]$expId) {
    $e = [int]($expId -replace '\D','')
    if ($e -notin @(7, 8, 9, 10)) { return }

    $tcPath = $env:CATALINA_HOME
    if (-not $tcPath -and (Test-Path "C:\apache-tomcat-9.0.86")) {
        $tcPath = "C:\apache-tomcat-9.0.86"
    }

    Write-Host ""
    Write-Host "============================================================"
    Write-Host ("  APACHE TOMCAT EXECUTION GUIDE -- Exp {0:D2}" -f $e)
    Write-Host "============================================================"
    if ($tcPath) {
        Write-Host "Tomcat Location : $tcPath"
    } else {
        Write-Host "Tomcat Location : Set `$env:CATALINA_HOME"
    }
    Write-Host "------------------------------------------------------------"

    if ($e -eq 7) {
        Write-Host "Webapp Target   : webapps/myapp/WEB-INF/classes/WelcomeServlet.class"
        Write-Host "Browser URL     : http://localhost:8080/myapp/welcome"
        Write-Host ""
        Write-Host "[1] Universal PowerShell Commands:"
        Write-Host '    New-Item -ItemType Directory -Force -Path "$env:CATALINA_HOME\webapps\myapp\WEB-INF\classes"'
        Write-Host '    javac -cp "$env:CATALINA_HOME\lib\servlet-api.jar" -d "$env:CATALINA_HOME\webapps\myapp\WEB-INF\classes" WelcomeServlet.java'
        Write-Host '    & "$env:CATALINA_HOME\bin\startup.bat"'
        Write-Host "    http://localhost:8080/myapp/welcome"
    } elseif ($e -eq 8) {
        Write-Host "Webapp Target   : webapps/myapp/index.html & WEB-INF/classes/HelloServlet.class"
        Write-Host "Browser URL     : http://localhost:8080/myapp/index.html"
        Write-Host ""
        Write-Host "[1] Universal PowerShell Commands:"
        Write-Host '    New-Item -ItemType Directory -Force -Path "$env:CATALINA_HOME\webapps\myapp\WEB-INF\classes"'
        Write-Host '    Copy-Item index.html "$env:CATALINA_HOME\webapps\myapp\"'
        Write-Host '    javac -cp "$env:CATALINA_HOME\lib\servlet-api.jar" -d "$env:CATALINA_HOME\webapps\myapp\WEB-INF\classes" HelloServlet.java'
        Write-Host '    & "$env:CATALINA_HOME\bin\startup.bat"'
        Write-Host "    http://localhost:8080/myapp/index.html"
    } elseif ($e -eq 9) {
        Write-Host "Webapp Target   : webapps/myapp/welcome.jsp (No javac needed)"
        Write-Host "Browser URL     : http://localhost:8080/myapp/welcome.jsp"
        Write-Host ""
        Write-Host "[1] Universal PowerShell Commands:"
        Write-Host '    New-Item -ItemType Directory -Force -Path "$env:CATALINA_HOME\webapps\myapp"'
        Write-Host '    Copy-Item welcome.jsp "$env:CATALINA_HOME\webapps\myapp\"'
        Write-Host '    & "$env:CATALINA_HOME\bin\startup.bat"'
        Write-Host "    http://localhost:8080/myapp/welcome.jsp"
    } elseif ($e -eq 10) {
        Write-Host "Webapp Target   : webapps/myapp/details.jsp (No javac needed)"
        Write-Host "Browser URL     : http://localhost:8080/myapp/details.jsp"
        Write-Host ""
        Write-Host "[1] Universal PowerShell Commands:"
        Write-Host '    New-Item -ItemType Directory -Force -Path "$env:CATALINA_HOME\webapps\myapp"'
        Write-Host '    Copy-Item details.jsp "$env:CATALINA_HOME\webapps\myapp\"'
        Write-Host '    & "$env:CATALINA_HOME\bin\startup.bat"'
        Write-Host "    http://localhost:8080/myapp/details.jsp"
    }
    if ($tcPath) {
        Write-Host ""
        Write-Host "[2] Ready-to-Run for THIS PC ($tcPath):"
        if ($e -eq 7) {
            Write-Host "    javac -cp `"$tcPath\lib\servlet-api.jar`" -d `"$tcPath\webapps\myapp\WEB-INF\classes`" WelcomeServlet.java"
            Write-Host "    & `"$tcPath\bin\startup.bat`""
            Write-Host "    http://localhost:8080/myapp/welcome"
        } elseif ($e -eq 8) {
            Write-Host "    Copy-Item index.html `"$tcPath\webapps\myapp\`""
            Write-Host "    javac -cp `"$tcPath\lib\servlet-api.jar`" -d `"$tcPath\webapps\myapp\WEB-INF\classes`" HelloServlet.java"
            Write-Host "    & `"$tcPath\bin\startup.bat`""
            Write-Host "    http://localhost:8080/myapp/index.html"
        } elseif ($e -eq 9) {
            Write-Host "    Copy-Item welcome.jsp `"$tcPath\webapps\myapp\`""
            Write-Host "    & `"$tcPath\bin\startup.bat`""
            Write-Host "    http://localhost:8080/myapp/welcome.jsp"
        } elseif ($e -eq 10) {
            Write-Host "    Copy-Item details.jsp `"$tcPath\webapps\myapp\`""
            Write-Host "    & `"$tcPath\bin\startup.bat`""
            Write-Host "    http://localhost:8080/myapp/details.jsp"
        }
    }
    Write-Host "============================================================"
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
        Print-TomcatGuide $expNum
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
        Print-TomcatGuide $expNum
        exit 0
    }

    Write-Error "Unknown file '$fileArg'. Available: 1 to $($files.Count)"
    exit 1
}

# Single file
Write-Output $files[0].code.Trim()
Print-TomcatGuide $expNum
exit 0
