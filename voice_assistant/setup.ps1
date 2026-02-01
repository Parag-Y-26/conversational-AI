# Setup script for Windows Voice Assistant
# Run this in PowerShell as Administrator

Write-Host "================================" -ForegroundColor Cyan
Write-Host "  Voice Assistant Setup Script" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Check Python
Write-Host "[1/4] Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "  Found: $pythonVersion" -ForegroundColor Green
}
catch {
    Write-Host "  ERROR: Python not found. Please install Python 3.10+" -ForegroundColor Red
    exit 1
}

# Create virtual environment (optional)
Write-Host ""
Write-Host "[2/4] Setting up environment..." -ForegroundColor Yellow
$createVenv = Read-Host "Create virtual environment? (y/n)"
if ($createVenv -eq "y") {
    python -m venv venv
    .\venv\Scripts\Activate.ps1
    Write-Host "  Virtual environment created and activated" -ForegroundColor Green
}

# Install dependencies
Write-Host ""
Write-Host "[3/4] Installing dependencies..." -ForegroundColor Yellow
Write-Host "  This may take a few minutes..." -ForegroundColor Gray

pip install --upgrade pip

# Try regular install first
pip install -r requirements.txt 2>&1 | Out-Null

# Check if PyAudio failed
$pyaudioInstalled = pip show pyaudio 2>&1
if ($pyaudioInstalled -like "*not found*") {
    Write-Host "  PyAudio failed, trying pipwin..." -ForegroundColor Yellow
    pip install pipwin
    pipwin install pyaudio
}

Write-Host "  Dependencies installed!" -ForegroundColor Green

# Verify installation
Write-Host ""
Write-Host "[4/4] Verifying installation..." -ForegroundColor Yellow

$modules = @("pyttsx3", "speech_recognition", "mss", "PIL", "httpx", "pystray")
foreach ($mod in $modules) {
    $result = python -c "import $mod" 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✓ $mod" -ForegroundColor Green
    }
    else {
        Write-Host "  ✗ $mod" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "================================" -ForegroundColor Cyan
Write-Host "  Setup Complete!" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "To run the assistant:" -ForegroundColor White
Write-Host "  python main.py" -ForegroundColor Yellow
Write-Host ""
Write-Host "Say 'Hey Nebula' to activate!" -ForegroundColor Cyan
