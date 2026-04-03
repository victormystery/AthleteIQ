# PowerShell script to set up Windows Task Scheduler for automated Google Sheets sync
# Run this script as Administrator to create scheduled task

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "Setting Up Automated Google Sheets Sync" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Configuration
$TaskName = "Google Sheets CSV Sync - Career Recommender"
$Description = "Automatically syncs Google Sheets data to CSV every 2 days"
$ScriptPath = Join-Path $PSScriptRoot "run_sync.bat"
$WorkingDirectory = Split-Path $PSScriptRoot -Parent | Split-Path -Parent

# Check if script exists
if (-not (Test-Path $ScriptPath)) {
    Write-Host "ERROR: Script not found at $ScriptPath" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "Script path: $ScriptPath" -ForegroundColor Yellow
Write-Host "Working directory: $WorkingDirectory" -ForegroundColor Yellow
Write-Host ""

# Prompt for schedule preference
Write-Host "Choose sync interval:" -ForegroundColor Green
Write-Host "1. Every 2 days (recommended)"
Write-Host "2. Daily"
Write-Host "3. Every 3 days"
Write-Host "4. Weekly"
$choice = Read-Host "Enter choice (1-4)"

switch ($choice) {
    "1" { 
        $IntervalDays = 2
        $Interval = "P2D"
    }
    "2" { 
        $IntervalDays = 1
        $Interval = "P1D"
    }
    "3" { 
        $IntervalDays = 3
        $Interval = "P3D"
    }
    "4" { 
        $IntervalDays = 7
        $Interval = "P7D"
    }
    default { 
        $IntervalDays = 2
        $Interval = "P2D"
    }
}

Write-Host ""
Write-Host "Schedule: Run every $IntervalDays days at 9:00 AM" -ForegroundColor Green
Write-Host ""

# Check if task already exists
$ExistingTask = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue

if ($ExistingTask) {
    Write-Host "⚠️  Task already exists!" -ForegroundColor Yellow
    $overwrite = Read-Host "Do you want to overwrite it? (y/n)"
    if ($overwrite -ne "y") {
        Write-Host "Cancelled." -ForegroundColor Yellow
        Read-Host "Press Enter to exit"
        exit 0
    }
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
    Write-Host "Removed existing task." -ForegroundColor Yellow
}

# Create scheduled task action
$Action = New-ScheduledTaskAction `
    -Execute "cmd.exe" `
    -Argument "/c `"$ScriptPath`"" `
    -WorkingDirectory $WorkingDirectory

# Create trigger - Run every N days at 9:00 AM
$Trigger = New-ScheduledTaskTrigger `
    -Daily `
    -At 9am `
    -DaysInterval $IntervalDays

# Create settings
$Settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -RunOnlyIfNetworkAvailable `
    -MultipleInstances IgnoreNew

# Create principal (run with user's permissions)
$Principal = New-ScheduledTaskPrincipal `
    -UserId $env:USERNAME `
    -LogonType Interactive `
    -RunLevel Limited

# Register the task
try {
    Register-ScheduledTask `
        -TaskName $TaskName `
        -Description $Description `
        -Action $Action `
        -Trigger $Trigger `
        -Settings $Settings `
        -Principal $Principal `
        -ErrorAction Stop
    
    Write-Host ""
    Write-Host "============================================" -ForegroundColor Green
    Write-Host "✅ SUCCESS: Scheduled task created!" -ForegroundColor Green
    Write-Host "============================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Task details:" -ForegroundColor Cyan
    Write-Host "  Name: $TaskName"
    Write-Host "  Schedule: Every $IntervalDays days at 9:00 AM"
    Write-Host "  Script: $ScriptPath"
    Write-Host ""
    Write-Host "To manage this task:" -ForegroundColor Yellow
    Write-Host "  1. Open Task Scheduler (taskschd.msc)"
    Write-Host "  2. Navigate to 'Task Scheduler Library'"
    Write-Host "  3. Find '$TaskName'"
    Write-Host ""
    
    # Test run option
    $testRun = Read-Host "Do you want to test run the sync now? (y/n)"
    if ($testRun -eq "y") {
        Write-Host ""
        Write-Host "Running sync script..." -ForegroundColor Cyan
        Start-Process -FilePath "cmd.exe" -ArgumentList "/c", "`"$ScriptPath`"" -Wait -NoNewWindow
    }
    
} catch {
    Write-Host ""
    Write-Host "❌ ERROR: Failed to create scheduled task" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    Write-Host ""
    Write-Host "Note: You may need to run this script as Administrator" -ForegroundColor Yellow
}

Write-Host ""
Read-Host "Press Enter to exit"
