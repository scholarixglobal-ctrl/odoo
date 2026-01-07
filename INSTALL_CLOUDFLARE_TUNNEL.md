# Install Cloudflare Tunnel for SSH Access

## Problem
- Port 22 is blocked (connection timed out)
- Need to use Cloudflare tunnel to access SSH
- `cloudflared` CLI is not installed

## Solution
Install and configure Cloudflare tunnel CLI

---

## Step 1: Download & Install Cloudflare Tunnel

### Option A: Using Chocolatey (Recommended)

**1. Open PowerShell as Administrator**
- Right-click PowerShell → Run as Administrator

**2. Install Cloudflare tunnel:**
```powershell
choco install cloudflare-warp
```

### Option B: Manual Download

**1. Download installer:**
- Go to: https://github.com/cloudflare/cloudflared/releases
- Download: `cloudflared-windows-amd64.exe` (64-bit)
- Download: `cloudflared-windows-386.exe` (32-bit)

**2. Install by running the .exe file**

**3. Add to PATH:**
- Right-click This PC → Properties
- Advanced system settings → Environment Variables
- Add folder containing `cloudflared.exe` to PATH

### Option C: Windows Terminal/PowerShell

```powershell
# Download and install
Invoke-WebRequest -Uri "https://github.com/cloudflare/cloudflared/releases/download/2024.12.0/cloudflared-windows-amd64.msi" -OutFile "$env:TEMP\cloudflared.msi"
Start-Process msiexec.exe -ArgumentList "/i $env:TEMP\cloudflared.msi /quiet"
```

---

## Step 2: Verify Installation

```powershell
cloudflared --version
```

**Expected output:**
```
cloudflared version 2024.12.0 (built 2024-12-10)
```

---

## Step 3: Authenticate with Cloudflare

```powershell
cloudflared tunnel login
```

**What happens:**
1. Opens browser to Cloudflare login
2. Select your domain (scholarixglobal.com)
3. Authenticates your local `cloudflared`
4. Creates certificate at `C:\Users\USER\.cloudflared\cert.pem`

---

## Step 4: Create SSH Tunnel Configuration

### Find Your Tunnel ID

```powershell
cloudflared tunnel list
```

**Expected output:**
```
ID     | Name              | Created              | Connections
-------|-------------------|----------------------|----------
abc123 | my-tunnel         | 2024-01-07 12:00:00  | ACTIVE
```

Copy the ID (abc123)

### Create Configuration File

**Location:** `C:\Users\USER\.cloudflared\config.yml`

```yaml
tunnel: YOUR_TUNNEL_ID_HERE
credentials-file: C:\Users\USER\.cloudflared\YOUR_TUNNEL_ID_HERE.json

ingress:
  - hostname: ssh.odoo.scholarixglobal.com
    service: ssh://localhost:22
  - service: http_status:404
```

**Replace:**
- `YOUR_TUNNEL_ID_HERE` with your actual tunnel ID

---

## Step 5: Start the Tunnel

**One-time connection:**
```powershell
cloudflared tunnel run YOUR_TUNNEL_ID_HERE
```

**Or start the service:**
```powershell
cloudflared service install
cloudflared service start
```

---

## Step 6: Test SSH Connection

**In a NEW PowerShell window:**

```powershell
ssh -i C:\Users\USER\.ssh\id_rsa odoo@ssh.odoo.scholarixglobal.com
```

**Note:** Uses `ssh.odoo.scholarixglobal.com` (not direct domain)

---

## Troubleshooting

### "cloudflared command not found"
- Restart PowerShell
- Check PATH environment variable
- Reinstall cloudflared

### "Tunnel not authenticated"
```powershell
cloudflared tunnel login
```

### "Connection refused"
- Tunnel service not running
- Check: `cloudflared tunnel list`
- Restart: `cloudflared service restart`

### "Permission denied"
- Verify SSH key exists
- Check SSH key permissions

---

## Alternative: Use Web Control Panel

If CLI is too complex:

1. Go to Cloudflare dashboard
2. Select your domain
3. Tunnels & Connectors → Tunnels
4. Click on your tunnel
5. Configure Public Hostnames:
   - Subdomain: ssh
   - Domain: odoo.scholarixglobal.com
   - Service: SSH (localhost:22)
6. Save

Then use: `ssh -i KEY odoo@ssh.odoo.scholarixglobal.com`

---

## Quick Reference

**Check tunnel status:**
```powershell
cloudflared tunnel list
```

**View tunnel logs:**
```powershell
cloudflared tunnel logs YOUR_TUNNEL_ID
```

**Stop tunnel:**
```powershell
cloudflared service stop
```

**Restart tunnel:**
```powershell
cloudflared service restart
```

---

## Next Steps (Once Tunnel is Running)

```powershell
# Test SSH connection
ssh -i C:\Users\USER\.ssh\id_rsa odoo@ssh.odoo.scholarixglobal.com

# Or with ED25519
ssh -i C:\Users\USER\.ssh\id_ed25519 odoo@ssh.odoo.scholarixglobal.com
```

---

**Document created:** January 7, 2026  
**Status:** Installation guide for Cloudflare tunnel  
**Next:** Install cloudflared and authenticate
