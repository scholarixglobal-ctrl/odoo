# ✅ Zoho Mail Server Configuration - Setup Complete!

**Status:** Configured and ready (Password update required)  
**Date:** January 14, 2026

---

## 📧 Current Configuration

### Mail Server Setup
- **Server ID:** 2
- **Provider:** Zoho Mail
- **SMTP Host:** smtppro.zoho.com
- **SMTP Port:** 587
- **Email:** noreply@scholarixglobal.com
- **Encryption:** STARTTLS
- **Authentication:** Login
- **Status:** ✅ Active

### Admin Configuration
- **Admin Email:** admin@scholarixglobal.com (configured)
- **Admin User:** admin (ID: 2)

---

## 🚀 Quick Setup (2 Steps)

### Step 1: Get Your Zoho Password

1. Go to https://accounts.zoho.com
2. Login with your Zoho account
3. Navigate to **Settings → Security**
4. Find **App Passwords** section
5. If you have 2FA enabled:
   - Create a new App Password for "SMTP"
   - Copy the password shown
6. If you don't have 2FA:
   - Use your Zoho account password directly

### Step 2: Update Odoo

Run this command with your Zoho password:

```bash
cd /c/odoo19
./setup_zoho_mail.sh 'YOUR_ZOHO_PASSWORD'
```

**Example:**
```bash
./setup_zoho_mail.sh 'ZohoPassword123'
```

The script will:
- ✅ Update the password
- ✅ Restart Odoo
- ✅ Verify the system is running
- ✅ Show instructions for testing

---

## 🧪 Verify It's Working

### Method 1: Via Odoo Web Interface

1. Login to: https://scholarixglobal.com
2. Go to: **Settings → Technical → Email → Outgoing Mail Servers**
3. Click: **Scholarix Global Mail Server**
4. Click: **Test Connection** button
5. You should see: ✅ "Connection Test Succeeded!"

### Method 2: Send Test Email

After updating the password, send a test email:

```bash
docker exec odoo19-odoo-1 odoo shell -d SGCTECHAI --no-http << 'EOF'
# Send test email
env['mail.mail'].create({
    'email_from': 'noreply@scholarixglobal.com',
    'email_to': 'your-email@example.com',
    'subject': 'Test Email from Odoo',
    'body_html': '<p>Zoho mail server is working perfectly!</p><p>This confirms your SMTP configuration is correct.</p>',
}).send()
env.cr.commit()
print('✅ Test email sent!')
EOF
```

Check your email inbox for the test message.

---

## 🔧 Troubleshooting

### "Authentication Failed"

**Cause:** Wrong password or Zoho 2FA enabled without app password

**Solution:**
1. Make sure you're using an **App Password** (not account password) if 2FA is enabled
2. Go to https://accounts.zoho.com → Settings → Security → App Passwords
3. Create a new app password for "SMTP"
4. Copy the exact password and try again:
   ```bash
   ./setup_zoho_mail.sh 'YOUR_NEW_APP_PASSWORD'
   ```

### "Connection Refused"

**Cause:** Firewall blocking port 587 or wrong host

**Solution:**
```bash
# Test Zoho SMTP connection from your system
telnet smtppro.zoho.com 587

# Or use nc
nc -zv smtppro.zoho.com 587
```

If it doesn't work, your firewall may be blocking outbound SMTP. Contact your ISP or IT team.

### "Please configure an email on the current user"

**Cause:** Admin user doesn't have email address

**Solution:** Already fixed! Admin email is now set to: `admin@scholarixglobal.com`

Verify:
```bash
docker exec odoo19-db-1 psql -U odoo -d SGCTECHAI -c \
  "SELECT id, login, partner_id FROM res_users WHERE id=2;"
```

### "TLS/SSL Error"

**Cause:** Certificate validation issues

**Solution:**
```bash
# Restart Odoo to refresh SSL certificates
docker restart odoo19-odoo-1
```

---

## 📋 Manual Configuration (if needed)

### Update Password Only
```bash
docker exec odoo19-db-1 psql -U odoo -d SGCTECHAI -c \
  "UPDATE ir_mail_server SET smtp_pass='YOUR_PASSWORD' WHERE id=2;"

docker restart odoo19-odoo-1
```

### Change Email Address
```bash
docker exec odoo19-db-1 psql -U odoo -d SGCTECHAI -c \
  "UPDATE ir_mail_server SET smtp_user='YOUR_EMAIL@scholarixglobal.com' WHERE id=2;"
```

### View Current Configuration
```bash
docker exec odoo19-db-1 psql -U odoo -d SGCTECHAI -c \
  "SELECT id, name, smtp_host, smtp_port, smtp_user, smtp_encryption, active FROM ir_mail_server WHERE id=2;"
```

---

## 🔐 Security Notes

1. **Never share your password** - Keep it confidential
2. **Use App Passwords** - If Zoho has 2FA, always create app-specific passwords
3. **Rotate regularly** - Change passwords every 90 days
4. **Monitor email logs** - Check for suspicious activity

### View Email Logs
```bash
# See all sent emails
docker exec odoo19-db-1 psql -U odoo -d SGCTECHAI -c \
  "SELECT id, email_from, email_to, subject, state, create_date 
   FROM mail_mail 
   ORDER BY create_date DESC LIMIT 20;"

# See failed emails only
docker exec odoo19-db-1 psql -U odoo -d SGCTECHAI -c \
  "SELECT id, email_to, subject, failure_reason 
   FROM mail_mail 
   WHERE state='exception' 
   ORDER BY create_date DESC;"
```

---

## 📞 Commands Reference

### Setup Zoho Password
```bash
./setup_zoho_mail.sh 'YOUR_ZOHO_PASSWORD'
```

### View Mail Server Details
```bash
docker exec odoo19-db-1 psql -U odoo -d SGCTECHAI -c \
  "SELECT * FROM ir_mail_server WHERE id=2;"
```

### Restart Odoo After Changes
```bash
docker restart odoo19-odoo-1
```

### Test Connection from Command Line
```bash
docker exec odoo19-odoo-1 bash -c "python3 -c '
import smtplib
smtp = smtplib.SMTP(\"smtppro.zoho.com\", 587)
smtp.starttls()
smtp.login(\"noreply@scholarixglobal.com\", \"YOUR_PASSWORD\")
print(\"✅ Connection successful!\")
smtp.quit()
'"
```

---

## ✅ Next Steps

1. **Run the setup script** with your Zoho password:
   ```bash
   ./setup_zoho_mail.sh 'YOUR_PASSWORD'
   ```

2. **Test the connection** in Odoo UI:
   - Settings → Technical → Email → Outgoing Mail Servers
   - Click "Scholarix Global Mail Server"
   - Click "Test Connection"

3. **Send a test email** to verify it works

4. **Configure email templates** (if needed):
   - Settings → Technical → Email Templates
   - Customize message templates

5. **Monitor email delivery**:
   - Check mail queue in Settings → Technical
   - Verify sent emails in mail.mail table

---

## 🎯 What's Configured

✅ Mail server created with Zoho SMTP  
✅ Email address set to: noreply@scholarixglobal.com  
✅ Admin user email configured: admin@scholarixglobal.com  
✅ STARTTLS encryption enabled  
✅ Port 587 configured  
✅ Duplicate mail servers removed  
✅ Odoo restarted and running  

---

## ⏭️ Once Password is Updated

After running `./setup_zoho_mail.sh`, you'll be able to:

✅ Send automated email notifications  
✅ Send CRM lead follow-up emails  
✅ Send customer communications  
✅ Send password reset emails  
✅ Send order confirmations  
✅ Send all system notifications  

---

**Status:** Ready for password configuration  
**Your Action:** Run `./setup_zoho_mail.sh` with your Zoho credentials  
**Support:** Check logs with `docker logs odoo19-odoo-1 | grep -i mail`

---

*Last Updated: January 14, 2026*  
*For more help: https://www.zoho.com/mail/help/smtp.html*
