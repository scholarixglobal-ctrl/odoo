# Remote Server Connection Guide for Colleagues
## Accessing odoo.scholarixglobal.com via Cloudflare Tunnel

**Date:** January 7, 2026  
**Environment:** Odoo 19 on odoo.scholarixglobal.com  
**Access Method:** Cloudflare Tunnel (SSH)  
**Database:** SGCTECHAI (PostgreSQL 16.11)

---

## 🚀 QUICK START

### Prerequisites
- SSH key installed on your computer
- Cloudflare tunnel credentials
- Server SSH username
- Basic terminal/PowerShell knowledge

### In 30 Seconds
```powershell
# 1. Open PowerShell
# 2. Run this command (replace USERNAME with your server username)
ssh -i C:\Users\YOUR_USERNAME\.ssh\id_rsa odoo@odoo.scholarixglobal.com

# 3. You're connected! Verify with:
sudo -u postgres psql -l
```

---

## 📋 DETAILED SETUP INSTRUCTIONS

### Step 1: Locate Your SSH Key

**Option A: Using PowerShell (Recommended)**
```powershell
# List all SSH keys on your computer
Get-ChildItem -Path $HOME\.ssh -Force

# Should show:
# id_rsa (main key)
# id_ed25519 (alternative)
# scholarix_deploy (deployment key)
```

**Option B: Using File Explorer**
```
C:\Users\YOUR_USERNAME\.ssh\
```

### Step 2: Test SSH Connection

**First Attempt (Using RSA key):**
```powershell
ssh -i C:\Users\YOUR_USERNAME\.ssh\id_rsa odoo@odoo.scholarixglobal.com
```

**If that fails, try ED25519:**
```powershell
ssh -i C:\Users\YOUR_USERNAME\.ssh\id_ed25519 odoo@odoo.scholarixglobal.com
```

**If that fails, try deployment key:**
```powershell
ssh -i C:\Users\YOUR_USERNAME\.ssh\scholarix_deploy odoo@odoo.scholarixglobal.com
```

### Step 3: What to Expect

**Successful Connection:**
```
The authenticity of host can't be established...
Are you sure you want to continue? (yes/no/[fingerprint])
```
Type: `yes` and press Enter

**You'll see a prompt like:**
```
odoo@server:~$
```
or
```
root@server:~#
```

✅ **You're connected!**

### Step 4: Exit SSH When Done

```bash
exit
```

---

## 🔧 COMMON COMMANDS ONCE CONNECTED

### Database Inspection

**Check all databases:**
```bash
sudo -u postgres psql -l
```

**Count CRM leads:**
```bash
sudo -u postgres psql -d SGCTECHAI -c "SELECT COUNT(*) FROM crm_lead;"
```

**Count tags:**
```bash
sudo -u postgres psql -d SGCTECHAI -c "SELECT COUNT(*) FROM crm_tag;"
```

**List database tables:**
```bash
sudo -u postgres psql -d SGCTECHAI -c "\dt"
```

### Odoo Service Management

**Check Odoo status:**
```bash
sudo systemctl status odoo
```

**Restart Odoo:**
```bash
sudo systemctl restart odoo
```

**Stop Odoo:**
```bash
sudo systemctl stop odoo
```

**Start Odoo:**
```bash
sudo systemctl start odoo
```

### Logs & Debugging

**View Odoo logs (last 50 lines):**
```bash
sudo tail -50 /var/log/odoo/odoo-server.log
```

**View logs in real-time:**
```bash
sudo tail -f /var/log/odoo/odoo-server.log
```
*(Press Ctrl+C to exit)*

**Check system resources:**
```bash
top
```
*(Press 'q' to quit)*

### File Management

**List files in home directory:**
```bash
ls -la ~
```

**Check disk space:**
```bash
df -h
```

**Check current location:**
```bash
pwd
```

---

## 📤 UPLOADING FILES TO REMOTE SERVER

### Using SCP (Recommended)

**From your local computer (NOT in SSH session):**

```powershell
# Upload a file
scp -i C:\Users\YOUR_USERNAME\.ssh\id_rsa C:\local\path\file.dump odoo@odoo.scholarixglobal.com:~/

# Example with backup file:
scp -i C:\Users\YOUR_USERNAME\.ssh\id_rsa C:\odoo19\backups\sync_to_remote_20260106_145050.dump odoo@odoo.scholarixglobal.com:~/
```

### Using WinSCP (GUI - Easier)

1. Download: https://winscp.net
2. Create new connection:
   - Protocol: SFTP
   - Host: odoo.scholarixglobal.com
   - Username: odoo
   - Private key: C:\Users\YOUR_USERNAME\.ssh\id_rsa
3. Click Login
4. Drag and drop files

---

## 🗄️ DATABASE BACKUP & RESTORE

### Create a Backup (Safety First!)

```bash
# Create backup of SGCTECHAI database
sudo -u postgres pg_dump -d SGCTECHAI -F c -f ~/sgctechai_backup_$(date +%Y%m%d_%H%M%S).dump

# Example output: sgctechai_backup_20260107_143022.dump
```

### List Your Backups

```bash
ls -lh ~/*.dump
```

### Restore from Backup

```bash
# Drop existing database (⚠️ CAREFUL - This deletes data!)
sudo -u postgres psql -c "DROP DATABASE IF EXISTS SGCTECHAI;"

# Create new empty database
sudo -u postgres psql -c "CREATE DATABASE SGCTECHAI OWNER odoo;"

# Restore from backup
sudo -u postgres pg_restore -d SGCTECHAI -v ~/sgctechai_backup_20260107_143022.dump
```

---

## ⚠️ TROUBLESHOOTING

### "Permission denied (publickey)"

**Cause:** SSH key not recognized by server

**Solutions:**
1. Verify key exists: `Test-Path C:\Users\YOUR_USERNAME\.ssh\id_rsa`
2. Try different key: Use `id_ed25519` or `scholarix_deploy`
3. Contact provider to add your public key

### "Connection refused"

**Cause:** SSH service not running on server

**Solution:** Contact system administrator

### "No such file or directory"

**Cause:** SSH key path is wrong

**Solution:** Use full path with backslashes or forward slashes:
```powershell
ssh -i C:\Users\YOUR_USERNAME\.ssh\id_rsa odoo@odoo.scholarixglobal.com
```

### "Passphrase for key"

**Cause:** Your SSH key is password-protected

**Solution:** Enter the password you set when creating the key (characters won't display - that's normal)

### "Connection timed out"

**Cause:** Firewall/network issue

**Solutions:**
1. Check internet connection
2. Verify Cloudflare tunnel is active
3. Try `ping odoo.scholarixglobal.com` (should work)
4. Contact IT support

### "ssh: command not found"

**Cause:** SSH client not installed

**Solution (Windows):**
- Windows 10+ has built-in OpenSSH
- If not available, install Git for Windows: https://git-scm.com

---

## 🔐 SECURITY BEST PRACTICES

### 1. Protect Your SSH Key
```powershell
# Never share your private key!
# Never upload id_rsa to websites
# Keep passphrase secret
```

### 2. Use Key Passphrase
- Set a password when creating SSH keys
- This adds extra security layer

### 3. Log Out When Done
```bash
exit
```

### 4. Check Who's Connected
```bash
sudo who
sudo w
```

### 5. Review Logs
```bash
sudo tail -20 /var/log/auth.log
```

---

## 📊 USEFUL STATUS CHECKS

### Complete Health Check Script

Run all these commands to verify system status:

```bash
#!/bin/bash
echo "=== ODOO SERVICE STATUS ==="
sudo systemctl status odoo

echo -e "\n=== DATABASE STATUS ==="
sudo -u postgres psql -l

echo -e "\n=== CRM DATA COUNT ==="
sudo -u postgres psql -d SGCTECHAI -c "SELECT COUNT(*) FROM crm_lead; SELECT COUNT(*) FROM crm_tag;"

echo -e "\n=== DISK USAGE ==="
df -h

echo -e "\n=== MEMORY USAGE ==="
free -h

echo -e "\n=== RECENT ERRORS ==="
sudo tail -20 /var/log/odoo/odoo-server.log
```

---

## 🎯 TYPICAL WORKFLOW

### 1. Connect
```powershell
ssh -i C:\Users\YOUR_USERNAME\.ssh\id_rsa odoo@odoo.scholarixglobal.com
```

### 2. Backup (Always!)
```bash
sudo -u postgres pg_dump -d SGCTECHAI -F c -f ~/backup_$(date +%s).dump
```

### 3. Check Odoo Status
```bash
sudo systemctl status odoo
```

### 4. Make Changes
```bash
# Your commands here
```

### 5. Verify
```bash
sudo -u postgres psql -d SGCTECHAI -c "SELECT COUNT(*) FROM crm_lead;"
```

### 6. Check Logs
```bash
sudo tail -50 /var/log/odoo/odoo-server.log
```

### 7. Disconnect
```bash
exit
```

---

## 🚀 ADVANCED: AUTOMATED BACKUPS

### Create Daily Backup Script

```bash
#!/bin/bash
BACKUP_DIR="/home/odoo/backups"
mkdir -p $BACKUP_DIR
sudo -u postgres pg_dump -d SGCTECHAI -F c -f "$BACKUP_DIR/sgctechai_$(date +%Y%m%d).dump"
echo "Backup created: $BACKUP_DIR/sgctechai_$(date +%Y%m%d).dump"
```

### Schedule with Cron

```bash
# Edit crontab
sudo crontab -e

# Add this line (runs daily at 2 AM):
0 2 * * * /home/odoo/backup.sh
```

---

## 📞 NEED HELP?

### Common Issue Resolution

| Issue | Check | Fix |
|-------|-------|-----|
| Can't connect | Cloudflare tunnel status | Restart tunnel or check credentials |
| Odoo slow | `top` command | Restart Odoo service |
| Database error | `/var/log/odoo/odoo-server.log` | Check error, backup, restart |
| Disk full | `df -h` | Check `/var/log/odoo`, clean old logs |
| Permission denied | `id` command | Check user permissions, use `sudo` |

### Important Contacts

- **System Administrator:** [Contact Info]
- **Database Owner:** [Contact Info]
- **Cloudflare Support:** https://support.cloudflare.com

---

## 📚 REFERENCE: KEY DIRECTORIES

| Path | Purpose |
|------|---------|
| `/var/log/odoo/` | Odoo logs |
| `/home/odoo/` | Home directory for odoo user |
| `/etc/odoo/` | Odoo configuration |
| `/var/lib/postgresql/` | PostgreSQL data |
| `~/backups/` | Custom backup directory |

---

## ✅ CHECKLIST: BEFORE YOU START

- [ ] You have SSH key (id_rsa or id_ed25519)
- [ ] You know your server username (usually 'odoo')
- [ ] You have Cloudflare tunnel access
- [ ] You have PowerShell or terminal available
- [ ] You know the server domain (odoo.scholarixglobal.com)
- [ ] You tested SSH connection (even if it failed)
- [ ] You backed up local files

---

## 🎓 LEARNING RESOURCES

### SSH Basics
```bash
man ssh          # SSH manual
ssh-keygen -h    # Key generation help
```

### PostgreSQL Commands
```bash
man psql         # PostgreSQL CLI manual
```

### Linux Commands
```bash
man ls           # List files
man cd           # Change directory
man sudo         # Super user do
```

### Online Resources
- PostgreSQL Docs: https://www.postgresql.org/docs/
- SSH Guide: https://www.ssh.com/ssh/
- Linux Command Reference: https://man7.org/linux/man-pages/

---

## 📝 NOTES FOR YOUR TEAM

### Current Server Status
- **Status:** Active and running Odoo 19.0
- **Database:** SGCTECHAI (PostgreSQL 16.11)
- **CRM Leads:** 8,912 active leads
- **Last Updated:** January 7, 2026

### Known Issues
- Database manager disabled (security)
- SSH requires Cloudflare tunnel
- Port 22 blocked by firewall

### Recent Changes
- Restored missing CRM stages (5, 6, 7)
- Created verified database backup
- Implemented Cloudflare tunnel access

---

## 🔄 SUPPORT WORKFLOW

**If colleague gets stuck:**

1. **Ask them for:**
   - Exact error message (screenshot if possible)
   - What command they ran
   - What they were trying to do

2. **Try these fixes:**
   ```powershell
   # Test connectivity first
   ping odoo.scholarixglobal.com
   
   # Verify SSH key exists
   Test-Path C:\Users\$env:USERNAME\.ssh\id_rsa
   
   # Try verbose SSH (shows what's happening)
   ssh -vvv -i C:\Users\$env:USERNAME\.ssh\id_rsa odoo@odoo.scholarixglobal.com
   ```

3. **Escalate if needed:**
   - Contact system administrator
   - Check Cloudflare tunnel status
   - Review server logs

---

## 🎉 YOU'RE ALL SET!

Your colleague is now ready to:
- ✅ Connect to the remote server via SSH
- ✅ Access the database
- ✅ View logs and troubleshoot
- ✅ Perform backups
- ✅ Manage the Odoo service

**Next Steps:**
1. Share this document
2. Have them test connection
3. Walk through first backup together
4. Create team reference guide

---

**Document Version:** 1.0  
**Last Updated:** January 7, 2026  
**Maintained By:** Development Team  
**Next Review Date:** January 21, 2026

---

*Questions? Issues? Update this document and share improvements with the team!*
