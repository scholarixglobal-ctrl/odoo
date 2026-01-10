#!/usr/bin/env powershell
# Automated Cloudflare Tunnel Setup for Odoo19
# Run as Administrator
# Date: January 10, 2026

Write-Host "===============================================" -ForegroundColor Cyan
Write-Host "  Odoo19 - Cloudflare Tunnel Setup Wizard      " -ForegroundColor Cyan
Write-Host "===============================================" -ForegroundColor Cyan
Write-Host ""

# Check if running as Administrator
if (-not ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Write-Host "❌ ERROR: This script must be run as Administrator" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please:"
    Write-Host "1. Right-click PowerShell"
    Write-Host "2. Select 'Run as Administrator'"
    Write-Host "3. Run this script again"
    exit
}

Write-Host "✅ Running as Administrator" -ForegroundColor Green
Write-Host ""

# Step 1: Check if cloudflared is installed
Write-Host "Step 1: Checking cloudflared installation..." -ForegroundColor Yellow
$cloudflared = Get-Command cloudflared -ErrorAction SilentlyContinue

if ($cloudflared) {
    Write-Host "✅ cloudflared is already installed" -ForegroundColor Green
    $version = cloudflared --version
    Write-Host "   Version: $version" -ForegroundColor Green
} else {
    Write-Host "❌ cloudflared not found. Installing..." -ForegroundColor Red
    
    # Check if Chocolatey is installed
    $choco = Get-Command choco -ErrorAction SilentlyContinue
    
    if (-not $choco) {
        Write-Host "   Installing Chocolatey first..." -ForegroundColor Yellow
        Set-ExecutionPolicy Bypass -Scope Process -Force
        [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
        iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
    }
    
    Write-Host "   Installing Cloudflare Tunnel..." -ForegroundColor Yellow
    choco install cloudflare-warp -y
    
    # Reload PATH
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
    
    $version = cloudflared --version
    Write-Host "✅ Installed: $version" -ForegroundColor Green
}

Write-Host ""
Write-Host "Step 2: Authenticating with Cloudflare..." -ForegroundColor Yellow
Write-Host "   This will open your browser for authentication" -ForegroundColor Cyan
Write-Host ""

Read-Host "Press ENTER to continue"

cloudflared tunnel login

Write-Host ""
Write-Host "✅ Authentication complete!" -ForegroundColor Green
Write-Host ""

# Step 3: Create tunnel
Write-Host "Step 3: Creating Odoo19 tunnel..." -ForegroundColor Yellow
$tunnelName = "odoo19"

# Check if tunnel already exists
$existingTunnels = cloudflared tunnel list | Select-String $tunnelName

if ($existingTunnels) {
    Write-Host "⚠️  Tunnel '$tunnelName' already exists" -ForegroundColor Yellow
    $createNew = Read-Host "Create new tunnel anyway? (y/n)"
    if ($createNew -eq "n") {
        Write-Host "Using existing tunnel: $tunnelName" -ForegroundColor Green
    } else {
        cloudflared tunnel create $tunnelName
    }
} else {
    cloudflared tunnel create $tunnelName
}

Write-Host ""
Write-Host "✅ Tunnel created successfully!" -ForegroundColor Green
Write-Host ""

# Get tunnel ID
$tunnelInfo = cloudflared tunnel list | Select-String $tunnelName
$tunnelId = ($tunnelInfo -split '\s+')[0]

Write-Host "   Tunnel ID: $tunnelId" -ForegroundColor Green
Write-Host ""

# Step 4: Create config.yml
Write-Host "Step 4: Creating configuration file..." -ForegroundColor Yellow

$cloudflaredDir = "$env:UserProfile\.cloudflared"
$configPath = "$cloudflaredDir\config.yml"
$credentialsFile = "$cloudflaredDir\$tunnelId.json"

$configContent = @"
tunnel: $tunnelId
credentials-file: $credentialsFile

ingress:
  # Odoo Web Interface - Primary
  - hostname: odoo.scholarixglobal.com
    service: http://localhost:8069

  # Optional: Alternative hostname
  - hostname: odoo19.scholarixglobal.com
    service: http://localhost:8069

  # Optional: pgAdmin for database management
  - hostname: pgadmin.scholarixglobal.com
    service: http://localhost:5050

  # Catch-all
  - service: http_status:404
"@

Set-Content -Path $configPath -Value $configContent -Force

Write-Host "✅ Configuration file created:" -ForegroundColor Green
Write-Host "   $configPath" -ForegroundColor Green
Write-Host ""

# Step 5: Route domain
Write-Host "Step 5: Routing domain..." -ForegroundColor Yellow

cloudflared tunnel route dns $tunnelName odoo.scholarixglobal.com
cloudflared tunnel route dns $tunnelName odoo19.scholarixglobal.com

Write-Host "✅ DNS routes created!" -ForegroundColor Green
Write-Host ""

# Step 6: Install as service
Write-Host "Step 6: Installing as Windows Service..." -ForegroundColor Yellow
Write-Host "   This allows cloudflared to run automatically at startup" -ForegroundColor Cyan
Write-Host ""

cloudflared service install
$serviceStatus = Get-Service cloudflared -ErrorAction SilentlyContinue

if ($serviceStatus) {
    Write-Host "✅ Service installed!" -ForegroundColor Green
    
    Write-Host ""
    Write-Host "Starting service..." -ForegroundColor Yellow
    Start-Service cloudflared
    
    Start-Sleep -Seconds 2
    $serviceStatus = (Get-Service cloudflared).Status
    
    if ($serviceStatus -eq "Running") {
        Write-Host "✅ Service started and running!" -ForegroundColor Green
    } else {
        Write-Host "❌ Service failed to start" -ForegroundColor Red
    }
} else {
    Write-Host "❌ Service installation failed" -ForegroundColor Red
}

Write-Host ""
Write-Host "===============================================" -ForegroundColor Green
Write-Host "  Setup Complete! ✅                            " -ForegroundColor Green
Write-Host "===============================================" -ForegroundColor Green
Write-Host ""
Write-Host "Your Odoo19 is now accessible at:" -ForegroundColor Cyan
Write-Host "  🔗 https://odoo.scholarixglobal.com" -ForegroundColor Green
Write-Host ""
Write-Host "Alternative URL:" -ForegroundColor Cyan
Write-Host "  🔗 https://odoo19.scholarixglobal.com" -ForegroundColor Green
Write-Host ""
Write-Host "NEXT STEPS:" -ForegroundColor Yellow
Write-Host "  1. Update Odoo configuration (odoo.conf):"
Write-Host "     - Add: proxy_mode = True"
Write-Host "     - Add: web.base.url = https://odoo.scholarixglobal.com"
Write-Host ""
Write-Host "  2. Restart Odoo:"
Write-Host "     docker-compose restart odoo"
Write-Host ""
Write-Host "  3. Test access:"
Write-Host "     https://odoo.scholarixglobal.com"
Write-Host ""
Write-Host "USEFUL COMMANDS:" -ForegroundColor Yellow
Write-Host "  Check status:     cloudflared tunnel list" -ForegroundColor Cyan
Write-Host "  View logs:        cloudflared service logs" -ForegroundColor Cyan
Write-Host "  Restart service:  cloudflared service restart" -ForegroundColor Cyan
Write-Host "  Stop service:     cloudflared service stop" -ForegroundColor Cyan
Write-Host ""
Write-Host "SECURITY RECOMMENDATIONS:" -ForegroundColor Yellow
Write-Host "  1. Enable Cloudflare Zero Trust Access Control" -ForegroundColor Cyan
Write-Host "  2. Change default Odoo admin password" -ForegroundColor Cyan
Write-Host "  3. Use strong PostgreSQL password" -ForegroundColor Cyan
Write-Host "  4. Monitor access in Cloudflare dashboard" -ForegroundColor Cyan
Write-Host ""
Write-Host "For troubleshooting, see:" -ForegroundColor Yellow
Write-Host "  C:\odoo19\EXPOSE_ODOO_CLOUDFLARE_SETUP.md" -ForegroundColor Cyan
Write-Host ""

