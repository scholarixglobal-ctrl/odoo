# Why CRM Data Doesn't Appear on odoo.scholarixglobal.com

**Date:** January 6, 2026  
**Issue:** Local database has 8,912 CRM leads but odoo.scholarixglobal.com shows none

---

## **TL;DR - Quick Answer**

Your local database (`SGCTECHAI` on `DESKTOP-0862M4T`) and the production website (`odoo.scholarixglobal.com`) are **TWO SEPARATE, INDEPENDENT SYSTEMS**. They do not automatically sync.

**Local System:**
- Location: Your Windows machine (DESKTOP-0862M4T)
- Database: PostgreSQL running in Docker container `odoo19-db-1`
- Access: http://localhost:8069 or http://172.31.240.1:8069
- Data: 8,912 CRM leads ✅

**Remote System:**
- Location: Cloud server (likely DigitalOcean, AWS, or other hosting)
- Website: https://odoo.scholarixglobal.com
- Database: Separate PostgreSQL database on cloud server
- Data: 0 CRM leads (or different data) ❌

---

## **Why They Are Separate**

### **1. Different Database Servers**

```
┌─────────────────────────────────────┐      ┌──────────────────────────────────┐
│   LOCAL MACHINE (DESKTOP-0862M4T)   │      │  CLOUD SERVER (Remote Host)      │
├─────────────────────────────────────┤      ├──────────────────────────────────┤
│  Docker Container: odoo19-db-1      │      │  PostgreSQL Server               │
│  Database: SGCTECHAI                │      │  Database: SGCTECHAI (different) │
│  IP: 172.31.240.1:5433              │      │  IP: [Remote Server IP]          │
│  Data: 8,912 leads ✅               │      │  Data: Unknown/Empty ❌          │
│                                     │      │                                  │
│  Access: http://localhost:8069      │      │  Access: odoo.scholarixglobal.com│
└─────────────────────────────────────┘      └──────────────────────────────────┘
         ↑                                              ↑
    Development/Local                            Production/Live
```

### **2. Different Odoo Instances**

- **Local Odoo:** Runs in Docker container `odoo19-odoo-1`
- **Remote Odoo:** Runs on cloud server (completely separate installation)
- They do NOT share data automatically

### **3. No Automatic Synchronization**

- Odoo does not have built-in database replication between instances
- Any changes made locally stay local
- Any changes made remotely stay remote
- Manual sync/migration required

---

## **Evidence from Your System**

### **Email Addresses in Data**
Your backup files contain emails like `m.guido@scholarixglobal.com` and `catchall@scholarixglobal.com`, suggesting:
- This data was originally created on the remote system
- It was backed up and restored to your local machine
- But changes made locally have NOT been synced back

### **Container Names**
```bash
Local containers:
- odoo19-odoo-1  (Odoo application)
- odoo19-db-1    (PostgreSQL database)

These are LOCAL only and cannot be accessed from the internet.
```

---

## **How to Sync Data to odoo.scholarixglobal.com**

You have **4 main options**:

### **Option 1: Database Dump & Restore (RECOMMENDED for full sync)**

**Steps:**
```bash
# 1. Create backup of local database
docker exec odoo19-db-1 pg_dump -U odoo -d SGCTECHAI -F c -f /tmp/local_sync.dump

# 2. Copy dump from container to host
docker cp odoo19-db-1:/tmp/local_sync.dump C:/odoo19/backups/

# 3. Upload to remote server (via SCP, SFTP, or cloud storage)
scp C:/odoo19/backups/local_sync.dump user@remote-server:/tmp/

# 4. SSH into remote server
ssh user@remote-server

# 5. Stop Odoo on remote server
sudo systemctl stop odoo

# 6. Drop and recreate remote database
sudo -u postgres psql -c "DROP DATABASE SGCTECHAI;"
sudo -u postgres psql -c "CREATE DATABASE SGCTECHAI OWNER odoo;"

# 7. Restore the dump
sudo -u postgres pg_restore -d SGCTECHAI /tmp/local_sync.dump

# 8. Restart Odoo
sudo systemctl start odoo
```

**⚠️ WARNING:** This will REPLACE all data on the remote server!

---

### **Option 2: Odoo's Built-in Database Manager (Easier but risky)**

**Steps:**
1. Go to http://localhost:8069/web/database/manager
2. Click "Backup" on SGCTECHAI database
3. Download the ZIP file
4. Go to https://odoo.scholarixglobal.com/web/database/manager
5. Click "Restore" and upload the ZIP file
6. This will overwrite the remote database

**⚠️ WARNING:** This will DELETE all existing data on remote server!

---

### **Option 3: Export/Import CRM Data Only (Safer for selective sync)**

**Steps:**
```bash
# Export CRM data from local
docker exec odoo19-db-1 pg_dump -U odoo -d SGCTECHAI \
  -t crm_lead \
  -t crm_tag \
  -t crm_stage \
  -t crm_team \
  --data-only \
  --column-inserts \
  -f /tmp/crm_data.sql

# Copy to host
docker cp odoo19-db-1:/tmp/crm_data.sql C:/odoo19/backups/

# Upload to remote server
scp C:/odoo19/backups/crm_data.sql user@remote-server:/tmp/

# SSH to remote and import
ssh user@remote-server
sudo -u postgres psql -d SGCTECHAI -f /tmp/crm_data.sql
```

**Advantages:**
- Only syncs CRM data (safer)
- Preserves other remote data (users, settings, etc.)
- Less risky than full database replacement

**Disadvantages:**
- May cause conflicts if IDs already exist
- Requires manual conflict resolution

---

### **Option 4: API-Based Sync (Most Flexible)**

Use Odoo's XML-RPC or REST API to sync specific records:

```python
import xmlrpc.client

# Local Odoo
local_url = "http://localhost:8069"
local_db = "SGCTECHAI"
local_username = "admin"
local_password = "admin"

# Remote Odoo
remote_url = "https://odoo.scholarixglobal.com"
remote_db = "SGCTECHAI"
remote_username = "admin"
remote_password = "admin"

# Authenticate and sync leads
# (Full script available on request)
```

**Advantages:**
- Granular control over what syncs
- Can handle incremental updates
- No downtime required

**Disadvantages:**
- Requires programming
- Slower for large datasets
- Complex for relationships

---

## **What You Need to Know About Remote Server**

To sync data, you'll need:

### **Remote Server Access:**
- [ ] SSH access (username/password or SSH key)
- [ ] Server hostname or IP address
- [ ] PostgreSQL database credentials
- [ ] Odoo admin credentials

### **Remote Database Information:**
- [ ] Database name (likely `SGCTECHAI` or similar)
- [ ] Database host (localhost if Odoo and DB on same server)
- [ ] Database port (default 5432)
- [ ] Database user/password

### **Network Access:**
- [ ] Can you access the server via SSH?
- [ ] Is PostgreSQL accessible remotely? (Usually NO for security)
- [ ] Do you have sudo/root access?

---

## **Current Status Summary**

| System | Database | Leads | Status | Access |
|--------|----------|-------|--------|--------|
| **Local** | SGCTECHAI | 8,912 | ✅ Working | localhost:8069 |
| **Remote** | Unknown | 0 (?) | ❓ Unknown | scholarixglobal.com |

---

## **Recommended Next Steps**

### **Immediate Actions:**

1. **Verify Remote Access**
   ```bash
   ssh your-username@scholarixglobal.com
   # OR
   ssh your-username@[server-ip]
   ```

2. **Check Remote Database Status**
   ```bash
   sudo -u postgres psql -l
   # Look for database name
   
   sudo -u postgres psql -d SGCTECHAI -c "SELECT COUNT(*) FROM crm_lead;"
   # Check lead count
   ```

3. **Document Remote Configuration**
   - Server IP/hostname
   - Database name
   - Database credentials
   - Odoo installation path
   - Odoo version

4. **Create Backup of Remote Database FIRST**
   ```bash
   sudo -u postgres pg_dump -d SGCTECHAI -F c -f /tmp/remote_backup_$(date +%Y%m%d).dump
   ```

5. **Choose Sync Method** (from options above)

6. **Test in Staging First** (if available)

7. **Execute Sync During Off-Hours**

---

## **Why This Happened**

### **Common Scenarios:**

1. **Development vs Production Separation**
   - Local instance for testing/development
   - Remote instance for live/production
   - Intentional separation for safety

2. **Database Migration**
   - Data was backed up from remote
   - Restored locally for testing
   - Changes made locally
   - Never synced back to remote

3. **Data Recovery Scenario**
   - Remote database had issues
   - Restored from old backup locally
   - Working locally while remote is down/empty

---

## **Prevention for Future**

### **Set Up Automated Sync** (if needed)

Create a cron job for nightly sync:

```bash
#!/bin/bash
# /c/odoo19/scripts/sync-to-remote.sh

# Dump local database
docker exec odoo19-db-1 pg_dump -U odoo -d SGCTECHAI -F c \
  -f /tmp/nightly_sync.dump

# Upload to remote
docker cp odoo19-db-1:/tmp/nightly_sync.dump /c/odoo19/backups/
scp /c/odoo19/backups/nightly_sync.dump user@remote:/backups/

# Notify on completion
echo "Sync completed at $(date)" | mail -s "Database Sync" admin@scholarixglobal.com
```

### **Use Database Replication** (Advanced)

PostgreSQL supports master-slave replication:
- Local = Master (development)
- Remote = Slave (production, read-only)
- Changes propagate automatically

**Note:** Requires PostgreSQL expertise to set up.

---

## **Security Considerations**

### **Before Syncing:**

1. **Verify backup exists on remote**
   - Never sync without a backup
   - Test backup restoration first

2. **Check user accounts**
   - Local admin credentials ≠ Remote admin credentials
   - May need to reset passwords after sync

3. **Verify domain/URL settings**
   - `web.base.url` parameter in Odoo
   - Should be `https://odoo.scholarixglobal.com`

4. **Email configuration**
   - Local email settings ≠ Remote email settings
   - Update outgoing mail server after sync

5. **SSL/HTTPS**
   - Local runs on HTTP (no SSL)
   - Remote should use HTTPS
   - Verify certificates are valid

---

## **Contact Information for Remote Server**

**You'll need to gather this information:**

```yaml
Remote Server Details:
  Provider: [DigitalOcean / AWS / Azure / Other]
  IP Address: [XXX.XXX.XXX.XXX]
  Hostname: scholarixglobal.com
  SSH User: [username]
  SSH Key Path: [/path/to/key or password]

Database Details:
  Host: localhost (or IP if separate server)
  Port: 5432 (default PostgreSQL)
  Database Name: SGCTECHAI (or different?)
  User: odoo (or different?)
  Password: [get from Odoo config file]

Odoo Details:
  Install Path: /opt/odoo or /usr/lib/python3/dist-packages/odoo
  Config File: /etc/odoo/odoo.conf or similar
  Version: 19.0 (same as local?)
  Admin Password: [database manager password]
```

---

## **Troubleshooting**

### **"Cannot connect to remote server"**
- Check if you have SSH access
- Verify server is running
- Check firewall rules

### **"Database already exists"**
- Use `DROP DATABASE` first (with backup!)
- Or use `--clean` flag with pg_restore

### **"Permission denied"**
- Need sudo access
- Or run as postgres user: `sudo -u postgres pg_restore ...`

### **"Constraint violations during import"**
- Foreign key conflicts
- Use `--disable-triggers` flag (risky)
- Or import in correct order

---

## **Summary**

**Why data doesn't appear on odoo.scholarixglobal.com:**
- It's a SEPARATE system with a SEPARATE database
- No automatic synchronization exists
- Local changes stay local, remote changes stay remote

**To fix:**
1. Get remote server access credentials
2. Backup remote database FIRST
3. Choose sync method (full dump, selective export, or API)
4. Execute sync during off-hours
5. Test thoroughly after sync

**Need Help?**
- Check remote server access first
- Document all credentials (securely)
- Test sync on staging environment if possible
- Contact hosting provider if needed

---

*Document created: January 6, 2026*  
*For questions: Check your hosting provider dashboard or contact system administrator*
