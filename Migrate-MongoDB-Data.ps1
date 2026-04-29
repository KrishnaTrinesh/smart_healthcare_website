# MongoDB Data Migration Script
# Run this script as Administrator to move MongoDB data to the project folder

param(
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"

# Define paths
$SourcePath = "C:\Program Files\MongoDB\Server\8.2\data"
$TargetPath = "$PSScriptRoot\db\data"
$MongoConfigPath = "C:\Program Files\MongoDB\Server\8.2\bin\mongod.cfg"

Write-Host "========================================" -ForegroundColor Green
Write-Host "  MongoDB Data Migration Script" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

# Check if running as Administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")
if (-not $isAdmin -and -not $DryRun) {
    Write-Host "ERROR: This script must be run as Administrator!" -ForegroundColor Red
    Write-Host "Right-click PowerShell and select 'Run as Administrator'" -ForegroundColor Yellow
    exit 1
}

# Check if source exists
if (-not (Test-Path $SourcePath)) {
    Write-Host "ERROR: Source path not found: $SourcePath" -ForegroundColor Red
    exit 1
}

Write-Host "Source: $SourcePath" -ForegroundColor Cyan
Write-Host "Target: $TargetPath" -ForegroundColor Cyan
Write-Host ""

if ($DryRun) {
    Write-Host "DRY RUN MODE - No changes will be made" -ForegroundColor Yellow
    Write-Host ""
}

# Get MongoDB service status
try {
    $service = Get-Service -Name MongoDB -ErrorAction SilentlyContinue
    if ($service -and $service.Status -eq 'Running') {
        Write-Host "INFO: MongoDB service is running" -ForegroundColor Yellow
        if (-not $DryRun) {
            Write-Host "Stopping MongoDB service..." -ForegroundColor Yellow
            Stop-Service MongoDB -Force
            Start-Sleep -Seconds 2
        }
    }
} catch {
    Write-Host "INFO: MongoDB service not found or already stopped" -ForegroundColor Gray
}

# Create target directory
Write-Host "Creating target directory..." -ForegroundColor Yellow
if (-not $DryRun) {
    New-Item -ItemType Directory -Path $TargetPath -Force | Out-Null
}

# Copy files
Write-Host "Copying data files..." -ForegroundColor Yellow
if ($DryRun) {
    $files = Get-ChildItem -Path $SourcePath -Recurse | Measure-Object
    Write-Host "Would copy $($files.Count) files" -ForegroundColor Gray
} else {
    robocopy $SourcePath $TargetPath /E /R:3 /W:5 /NP /NDL /NFL | Out-Null
    if ($LASTEXITCODE -le 1) {
        Write-Host "[OK] Data copied successfully" -ForegroundColor Green
    } else {
        Write-Host "ERROR: Failed to copy data (Exit code: $LASTEXITCODE)" -ForegroundColor Red
        exit 1
    }
}

# Update MongoDB configuration
if (-not $DryRun) {
    Write-Host "Updating MongoDB configuration..." -ForegroundColor Yellow
    if (Test-Path $MongoConfigPath) {
        $configContent = Get-Content $MongoConfigPath -Raw
        $newConfigContent = $configContent -replace '(storage:\s+dbPath:\s+)[^\r\n]+', "`$1$TargetPath"
        Set-Content -Path $MongoConfigPath -Value $newConfigContent
        Write-Host "[OK] Configuration updated" -ForegroundColor Green
    } else {
        Write-Host "WARNING: Config file not found at: $MongoConfigPath" -ForegroundColor Yellow
    }
    
    # Start MongoDB service
    Write-Host "Starting MongoDB service..." -ForegroundColor Yellow
    try {
        Start-Service MongoDB -ErrorAction SilentlyContinue
        Write-Host "[OK] MongoDB service started" -ForegroundColor Green
    } catch {
        Write-Host "WARNING: Could not start MongoDB service automatically" -ForegroundColor Yellow
        Write-Host "You may need to start it manually: net start MongoDB" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
if ($DryRun) {
    Write-Host "  Migration Preview Complete" -ForegroundColor Green
    Write-Host "  Run without -DryRun to perform migration" -ForegroundColor Yellow
} else {
    Write-Host "  Migration Complete!" -ForegroundColor Green
}
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Verify data: mongosh smarthealthcare --eval 'db.getCollectionNames()'" -ForegroundColor White
Write-Host "2. Test your application" -ForegroundColor White
Write-Host "3. Backup the new data location" -ForegroundColor White

