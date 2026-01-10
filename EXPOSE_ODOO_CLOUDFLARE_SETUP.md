# 🚀 Expose Your Odoo19 Database & Web Interface via Cloudflare Tunnel

**Date:** January 10, 2026  
**Status:** Implementation Guide  
**Objective:** Make your local Odoo19 database accessible from anywhere securely

---

## 📊 CURRENT SETUP ANALYSIS

### ✅ What You Have
- **Odoo Version:** 19.0 (Custom Docker Build)
- **Database:** PostgreSQL 16 in Docker (Port: 5433)
- **Web Interface:** Running on localhost:8069
- **Database Name:** SGCTECHAI
- **Records:** 8,912 CRM leads, active database
- **Status:** Both Odoo and Database containers running ✓

### 🔧 Current Infrastructure
```
┌─ Windows Machine (DESKTOP-0862M4T) ─┐
│ IP: 172.31.240.1                    │
│                                      │
│ ┌─ Docker Network ─────────────┐   │
│ │                               │   │
│ │ odoo19-odoo-1 (8069)          │   │
│ │ odoo19-db-1 (postgres:16)     │   │
│ │ Network IP: 172.20.0.2        │   │
│ │                               │   │
│ └───────────────────────────────┘   │
│                                      │
│ Local Access: localhost:8069         │
│ Local DB: 172.31.240.1:5433          │
└──────────────────────────────────────┘
```

---

## 🎯 EXPOSURE OPTIONS COMPARISON

| Option | Setup | Security | Cost | Best For |
|--------|-------|----------|------|----------|
| **Cloudflare Tunnel** | Medium | ⭐⭐⭐⭐⭐ | FREE | Production-ready, recommended |
| **ngrok** | Easy | ⭐⭐⭐ | Paid | Quick testing |
| **Port Forwarding** | Easy | ⭐⭐ | FREE | Local network only |
| **VPN** | Hard | ⭐⭐⭐⭐ | Paid | Enterprise grade |

---

## ✨ RECOMMENDED: Cloudflare Tunnel (Complete Setup)

### What You Get
✅ Completely FREE  
✅ No bandwidth limits  
✅ End-to-end encryption  
✅ DDoS protection  
✅ Persistent URLs  
✅ Production-ready  
✅ Works through any firewall  

### Architecture After Setup
```
Internet
  ↓
[Cloudflare Global Network]
  ↓
[Cloudflare Tunnel - cloudflared]
  ↓
localhost:8069 (Odoo Web)
localhost:5433 (Database) - Optional
```

---

## 🔐 STEP-BY-STEP INSTALLATION (Windows)

### STEP 1: Install Cloudflare Tunnel (cloudflared)

**Option A: Using Chocolatey (Recommended)**
```powershell
# Open PowerShell as Administrator
# Run:
choco install cloudflare-warp
```

**Option B: Manual MSI Installation**
```powershell
# Download and install
$url = "https://github.com/cloudflare/cloudflared/releases/download/2024.12.0/cloudflared-windows-amd64.msi"
$output = "$env:TEMP\cloudflared.msi"
Invoke-WebRequest -Uri $url -OutFile $output
Start-Process msiexec.exe -ArgumentList "/i $output /quiet" -Wait
```

**Option C: Direct Download**
- Go to: https://github.com/cloudflare/cloudflared/releases
- Download: `cloudflared-windows-amd64.msi`
- Run the installer

**Verify Installation:**
```powershell
cloudflared --version
# Should output: cloudflared version X.X.X
```

---

### STEP 2: Authenticate with Cloudflare

```powershell
cloudflared tunnel login
```

**What happens:**
1. Opens your default browser
2. Shows Cloudflare login page
3. Select your domain: `scholarixglobal.com`
4. Authorizes the local cloudflared
5. Creates certificate: `C:\Users\USER\.cloudflared\cert.pem`

**Expected output:**
```
You have successfully authenticated cloudflared!
Your certificate is saved at C:\Users\USER\.cloudflared\cert.pem
```

---

### STEP 3: Create the Tunnel

```powershell
cloudflared tunnel create odoo19
```

**Expected output:**
```
Tunnel credentials written to C:\Users\USER\.cloudflared\<tunnel-id>.json
Tunnel named odoo19 created with id: abc123...xyz789
```

**Save your Tunnel ID** (you'll need it)

---

### STEP 4: Create Configuration File

**Location:** `C:\Users\USER\.cloudflared\config.yml`

**Create new file with this content:**

```yaml
tunnel: <YOUR_TUNNEL_ID>
credentials-file: C:\Users\USER\.cloudflared\<YOUR_TUNNEL_ID>.json

ingress:
  # Web Interface - Primary Access
  - hostname: odoo.scholarixglobal.com
    service: http://localhost:8069

  # Optional: Direct Odoo URL alias
  - hostname: odoo19.scholarixglobal.com
    service: http://localhost:8069

  # Catch-all for invalid routes
  - service: http_status:404
```

**Replace `<YOUR_TUNNEL_ID>` with your actual tunnel ID** from Step 3

---

### STEP 5: Route Domain to Tunnel

```powershell
# Primary domain
cloudflared tunnel route dns odoo19 odoo.scholarixglobal.com

# Optional: Create alias
cloudflared tunnel route dns odoo19 odoo19.scholarixglobal.com
```

**Expected output:**
```
Successfully created route for odoo.scholarixglobal.com
DNS record created:
  Name: odoo
  Type: CNAME
  Target: <tunnel-id>.cfargotunnel.com
```

---

### STEP 6: Start the Tunnel (2 Options)

**Option A: Run Now (Foreground)**
```powershell
cloudflared tunnel run odoo19
```

**Expected output:**
```
2026-01-10T12:34:56Z INF Starting tunnel manager
2026-01-10T12:34:57Z INF Registering tunnel connection
2026-01-10T12:34:58Z INF Tunnel registered successfully
2026-01-10T12:34:59Z INF Connected to Cloudflare!
```

**Option B: Install as Service (Persistent)**
```powershell
# Install service (runs on Windows startup)
cloudflared service install

# Start the service
cloudflared service start

# Check status
cloudflared service status

# View logs
cloudflared service logs
```

---

### STEP 7: Test Your Access

#### Test 1: Local Access
```
http://localhost:8069
# Should show Odoo login page
```

#### Test 2: Remote Access (Globally)
```
https://odoo.scholarixglobal.com
# Should show Odoo login page from anywhere!
```

#### Test 3: Check Tunnel Status
```powershell
cloudflared tunnel list

# Expected output:
# ID      | Name        | Created       | Connections
# --------|-------------|---------------|-----------
# abc123  | odoo19      | 2026-01-10    | ACTIVE
```

---

## 🛡️ SECURITY CONFIGURATION (Recommended)

### Option 1: Cloudflare Zero Trust Access Control

**In Cloudflare Dashboard:**
1. Go to: `Zero Trust` → `Access` → `Applications`
2. Click: `Create Application`
3. Configure:
   - **Application name:** Odoo19
   - **Session duration:** 24 hours
   - **Domain:** odoo.scholarixglobal.com
4. Add Access Policies:
   - **Require:** Email ends with `@scholarixglobal.com`
   - OR require **Authentication** before access
5. Save and Deploy

**Benefits:**
✅ Only authorized users can access  
✅ MFA support  
✅ Audit logs  
✅ Device posture checks  

### Option 2: Change Odoo Admin Password

```powershell
# Connect to Odoo container
docker exec -it odoo19-odoo-1 /bin/bash

# Change master password (be secure!)
python3 -c "
from odoo import tools
import os
import sys

# Set super admin password
db_password = tools.hash_passwordpython('YOUR_STRONG_PASSWORD')
"
```

**Or simpler - via Odoo web interface:**
1. Login as admin
2. Settings → Users & Companies → Administrator
3. Change password
4. Save

### Option 3: Enable HTTPS Only

**In Cloudflare:**
1. Go to domain settings
2. SSL/TLS → Edge Certificates
3. Minimum TLS Version: TLS 1.2
4. Always Use HTTPS: **ON**

---

## 📱 ACCESSING DATABASE REMOTELY (PostgreSQL)

### Option 1: Via Cloudflare Tunnel + SSH

**Configure SSH tunnel:**
```yaml
# Add to C:\Users\USER\.cloudflared\config.yml
ingress:
  # ... existing Odoo configs ...
  
  # SSH for direct database access
  - hostname: ssh.odoo.scholarixglobal.com
    service: ssh://localhost:22
```

**Then run:**
```powershell
cloudflared tunnel route dns odoo19 ssh.odoo.scholarixglobal.com
```

### Option 2: Via pgAdmin (Recommended)

**Add pgAdmin to your Docker Compose:**

Add to `C:\odoo19\docker-compose.yml`:

```yaml
  pgadmin:
    image: dpage/pgadmin4:latest
    environment:
      PGADMIN_DEFAULT_EMAIL: admin@example.com
      PGADMIN_DEFAULT_PASSWORD: admin123
    ports:
      - "5050:80"
    depends_on:
      - db
    networks:
      - odoo19_default
```

**Add to Cloudflare config:**
```yaml
  - hostname: pgadmin.scholarixglobal.com
    service: http://localhost:5050
```

**Start it:**
```powershell
cd C:\odoo19
docker-compose up -d pgadmin
```

**Access:**
```
https://pgadmin.scholarixglobal.com
```

---

## 🔧 DOCKER COMPOSE UPDATE (Recommended)

**Update `C:\odoo19\docker-compose.yml` for better Cloudflare support:**

```yaml
version: '3.8'

services:
  # Odoo Service
  odoo:
    build:
      context: ./docker
      dockerfile: Dockerfile
    image: odoo-custom:19.0
    restart: unless-stopped
    ports:
      - "8069:8069"
    environment:
      HOST: host.docker.internal
      USER: odoo
      PASSWORD: odoo
    volumes:
      - ./docker/odoo.conf:/etc/odoo/odoo.conf:ro
      - ./data/filestore/SGCTECHAI:/var/lib/odoo/.local/share/Odoo/filestore/SGCTECHAI
      - ./data/sessions:/var/lib/odoo/sessions
      - ./data/backups:/var/lib/odoo/backups
      - ./addons:/mnt/extra-addons
      - ./custom_addons:/mnt/custom-addons
    command: [
      "--config=/etc/odoo/odoo.conf",
      "--addons-path=/usr/lib/python3/dist-packages/odoo/addons,/mnt/extra-addons/CybroAddons,/mnt/custom-addons",
      "-d", "SGCTECHAI",
      "--logfile=/dev/stdout",
      "--proxy-mode"
    ]
    networks:
      - bridge
      - odoo19_default
    depends_on:
      - db

  # PostgreSQL Database
  db:
    image: postgres:16
    restart: unless-stopped
    environment:
      POSTGRES_USER: odoo
      POSTGRES_PASSWORD: odoo
      POSTGRES_DB: SGCTECHAI
    volumes:
      - ./data/postgres:/var/lib/postgresql/data
    ports:
      - "5433:5432"
    networks:
      - odoo19_default

  # Optional: pgAdmin for database management
  pgadmin:
    image: dpage/pgadmin4:latest
    environment:
      PGADMIN_DEFAULT_EMAIL: admin@scholarixglobal.com
      PGADMIN_DEFAULT_PASSWORD: secure_password_here
    ports:
      - "5050:80"
    depends_on:
      - db
    networks:
      - odoo19_default

networks:
  bridge:
    driver: bridge
  odoo19_default:
    external: true

volumes:
  db-data:
```

---

## ⚠️ IMPORTANT: odoo.conf Updates

**Edit `C:\odoo19/docker/odoo.conf` to include:**

```ini
[options]
db_host = db
db_port = 5432
db_user = odoo
db_password = odoo
http_port = 8069
addons_path = /usr/lib/python3/dist-packages/odoo/addons,/mnt/extra-addons/CybroAddons,/mnt/custom-addons
logfile = /dev/stdout
log_level = info

# IMPORTANT for Cloudflare Tunnel
proxy_mode = True
web.base.url = https://odoo.scholarixglobal.com
```

Then restart:
```powershell
docker-compose restart odoo
```

---

## ✅ QUICK REFERENCE CHECKLIST

- [ ] Install cloudflared (verify with `cloudflared --version`)
- [ ] Authenticate: `cloudflared tunnel login`
- [ ] Create tunnel: `cloudflared tunnel create odoo19`
- [ ] Create config.yml file
- [ ] Route domain: `cloudflared tunnel route dns odoo19 odoo.scholarixglobal.com`
- [ ] Start tunnel: `cloudflared service install && cloudflared service start`
- [ ] Test local: http://localhost:8069
- [ ] Test remote: https://odoo.scholarixglobal.com
- [ ] Update odoo.conf with proxy_mode = True
- [ ] Restart Odoo: `docker-compose restart odoo`
- [ ] Verify tunnel: `cloudflared tunnel list`
- [ ] Check logs: `cloudflared service logs`

---

## 🚨 TROUBLESHOOTING

### Issue: "cloudflared command not found"
```powershell
# Solution 1: Restart PowerShell
# Solution 2: Verify PATH
echo $env:Path | Select-String cloudflare

# Solution 3: Reinstall
choco uninstall cloudflare-warp
choco install cloudflare-warp
```

### Issue: "Tunnel authentication failed"
```powershell
# Re-authenticate
cloudflared tunnel login
```

### Issue: "Cannot connect to https://odoo.scholarixglobal.com"
```powershell
# Check tunnel is running
cloudflared tunnel list

# Check tunnel logs
cloudflared service logs

# Restart tunnel
cloudflared service restart
```

### Issue: "Odoo shows white screen / assets not loading"
```powershell
# Update odoo.conf and add:
proxy_mode = True
web.base.url = https://odoo.scholarixglobal.com

# Restart Odoo
docker-compose restart odoo

# Clear browser cache (Ctrl+Shift+Delete)
```

### Issue: "Database connection refused"
```powershell
# Check database is running
docker ps | grep odoo19-db

# Check logs
docker logs odoo19-db-1

# Verify connection
docker exec odoo19-db-1 psql -U odoo -d SGCTECHAI -c "SELECT version();"
```

---

## 📊 MONITORING & LOGS

### View Tunnel Status
```powershell
# List all tunnels
cloudflared tunnel list

# View tunnel logs
cloudflared tunnel logs odoo19

# Watch logs in real-time
cloudflared tunnel logs odoo19 --follow
```

### View Service Logs
```powershell
# Service logs (if running as Windows service)
cloudflared service logs

# Or in Event Viewer
# Windows Logs → Application → Cloudflared
```

### Monitor Performance
**In Cloudflare Dashboard:**
1. Go to: Analytics → Tunnels
2. Select: odoo19
3. View: Requests, Bandwidth, Uptime

---

## 🔄 UPDATING CONFIGURATION LATER

### To Add New Routes
```powershell
# Edit config.yml, then:
cloudflared tunnel route dns odoo19 new-subdomain.scholarixglobal.com
cloudflared service restart
```

### To Change Credentials
```powershell
cloudflared tunnel delete odoo19
cloudflared tunnel create odoo19
# Then update config.yml with new credentials file
```

### To Uninstall Service
```powershell
cloudflared service uninstall
```

---

## 🎯 NEXT STEPS

1. **Install Cloudflare Tunnel** using steps 1-2 above
2. **Create tunnel** and configure it
3. **Test access** from another device
4. **Set up security** (Zero Trust access control)
5. **Monitor performance** via Cloudflare dashboard
6. **Share link** with team: `https://odoo.scholarixglobal.com`

---

## 📞 SUPPORT & RESOURCES

- **Cloudflare Docs:** https://developers.cloudflare.com/cloudflare-one/connections/connect-applications/
- **Tunnel Configuration:** https://developers.cloudflare.com/cloudflare-one/connections/connect-applications/install-and-setup/tunnel-guide/
- **Zero Trust Setup:** https://developers.cloudflare.com/cloudflare-one/setup/

---

**Document Version:** 2.0  
**Last Updated:** January 10, 2026  
**Status:** Ready for Implementation  
**Estimated Setup Time:** 15-20 minutes  

