# 📧 Odoo Mail Server Setup - Scholarix Global

**Status:** ✅ Mail server configured (Password update required)  
**Date:** January 14, 2026

---

## 🎯 Current Configuration

### Mail Server Details
- **Server ID:** 2
- **Name:** Scholarix Global Mail Server
- **SMTP Host:** smtp.gmail.com
- **SMTP Port:** 587
- **Email:** noreply@scholarixglobal.com
- **Encryption:** STARTTLS
- **Authentication:** Login
- **Status:** Active

### System Parameters
- **Catchall Domain:** scholarixglobal.com
- **Catchall Alias:** catchall
- **Bounce Alias:** bounce

---

## ⚠️ IMPORTANT: Update Email Password

The mail server is configured with a temporary placeholder password. You **MUST** update it with your actual credentials.

### Option 1: Using Gmail (Recommended)

If `noreply@scholarixglobal.com` is managed by Google Workspace or Gmail:

#### Step 1: Generate Gmail App Password

1. Go to your Google Account: https://myaccount.google.com
2. Navigate to **Security** → **2-Step Verification** (enable if not already)
3. Scroll down to **App passwords**
4. Create new app password:
   - App: **Mail**
   - Device: **Odoo Production Server**
5. Copy the 16-character password (format: `xxxx xxxx xxxx xxxx`)

#### Step 2: Update Odoo Database

Run this command with your actual app password:

```bash
docker exec odoo19-db-1 psql -U odoo -d SGCTECHAI -c \
  "UPDATE ir_mail_server SET smtp_pass='YOUR_16_CHAR_APP_PASSWORD' WHERE id=2;"
```

**Example:**
```bash
docker exec odoo19-db-1 psql -U odoo -d SGCTECHAI -c \
  "UPDATE ir_mail_server SET smtp_pass='abcd efgh ijkl mnop' WHERE id=2;"
```

#### Step 3: Restart Odoo
```bash
docker restart odoo19-odoo-1
```

---

### Option 2: Using Microsoft 365 / Outlook

If using Microsoft 365 for scholarixglobal.com:

#### Update SMTP Settings

```sql
UPDATE ir_mail_server SET 
  smtp_host = 'smtp.office365.com',
  smtp_port = 587,
  smtp_user = 'noreply@scholarixglobal.com',
  smtp_pass = 'YOUR_PASSWORD',
  smtp_encryption = 'starttls',
  smtp_authentication = 'login'
WHERE id = 2;
```

Run the command:
```bash
docker exec odoo19-db-1 psql -U odoo -d SGCTECHAI -c \
  "UPDATE ir_mail_server SET smtp_host='smtp.office365.com', smtp_pass='YOUR_PASSWORD' WHERE id=2;"
```

---

### Option 3: Using Custom SMTP Provider

If using another email provider (e.g., SendGrid, Mailgun, AWS SES):

#### Common SMTP Settings

**SendGrid:**
```sql
smtp_host = 'smtp.sendgrid.net'
smtp_port = 587
smtp_user = 'apikey'
smtp_pass = 'YOUR_SENDGRID_API_KEY'
```

**Mailgun:**
```sql
smtp_host = 'smtp.mailgun.org'
smtp_port = 587
smtp_user = 'postmaster@mg.scholarixglobal.com'
smtp_pass = 'YOUR_MAILGUN_PASSWORD'
```

**AWS SES:**
```sql
smtp_host = 'email-smtp.us-east-1.amazonaws.com'
smtp_port = 587
smtp_user = 'YOUR_AWS_SMTP_USERNAME'
smtp_pass = 'YOUR_AWS_SMTP_PASSWORD'
```

Update using:
```bash
docker exec odoo19-db-1 psql -U odoo -d SGCTECHAI -c \
  "UPDATE ir_mail_server SET smtp_host='YOUR_SMTP_HOST', smtp_port=587, smtp_user='YOUR_USERNAME', smtp_pass='YOUR_PASSWORD' WHERE id=2;"
```

---

## 🧪 Testing Mail Server

### Method 1: Via Odoo UI

1. Log in to Odoo: https://scholarixglobal.com
2. Go to **Settings** → **Technical** → **Email** → **Outgoing Mail Servers**
3. Click on "Scholarix Global Mail Server"
4. Click **Test Connection** button
5. If successful, you'll see: "Connection Test Succeeded!"

### Method 2: Via Command Line

```bash
docker exec odoo19-odoo-1 odoo shell -d SGCTECHAI --no-http << 'EOF'
# Send test email
mail_server = env['ir.mail_server'].browse(2)
try:
    mail_server.test_smtp_connection()
    print("✓ SMTP connection successful!")
except Exception as e:
    print(f"✗ SMTP connection failed: {e}")
EOF
```

### Method 3: Send Actual Test Email

```bash
docker exec odoo19-odoo-1 odoo shell -d SGCTECHAI --no-http << 'EOF'
# Send test email to yourself
env['mail.mail'].create({
    'email_from': 'noreply@scholarixglobal.com',
    'email_to': 'YOUR_EMAIL@example.com',
    'subject': 'Odoo Mail Server Test',
    'body_html': '<p>This is a test email from Scholarix Global Odoo instance.</p>',
}).send()
print("✓ Test email sent!")
env.cr.commit()
EOF
```

---

## 🔧 Troubleshooting

### Error: "Invalid Credentials"

**Cause:** Incorrect username or password

**Solution:**
1. Verify email address: `noreply@scholarixglobal.com`
2. If using Gmail, ensure you created an **App Password** (not regular password)
3. If using 2FA, app passwords are required
4. Check for typos in password (no spaces unless in app password format)

### Error: "SMTP AUTH extension not supported"

**Cause:** SMTP server doesn't support the authentication method

**Solution:**
```sql
UPDATE ir_mail_server SET smtp_authentication = 'plain' WHERE id = 2;
```

### Error: "Connection refused" or "Timeout"

**Cause:** Firewall blocking outgoing SMTP or wrong port

**Solutions:**
1. Check port 587 is allowed outbound
2. Try alternate port 465 with SSL:
```sql
UPDATE ir_mail_server SET smtp_port = 465, smtp_encryption = 'ssl' WHERE id = 2;
```

### Error: "TLS/SSL Error"

**Cause:** Certificate validation issues

**Solution:**
```bash
# Restart Odoo to reload SSL certificates
docker restart odoo19-odoo-1
```

### Gmail "Less Secure App" Error

**Cause:** Gmail blocks sign-ins from apps it doesn't recognize

**Solution:**
- Enable 2-Step Verification
- Use App Passwords (see Option 1 above)
- **Never** enable "Less secure app access" (deprecated by Google)

---

## 📋 Configuration Summary

### Current Database Values

Check current configuration:
```bash
docker exec odoo19-db-1 psql -U odoo -d SGCTECHAI -c \
  "SELECT id, name, smtp_host, smtp_port, smtp_user, smtp_encryption, smtp_authentication, active FROM ir_mail_server;"
```

### Mail System Parameters

```bash
docker exec odoo19-db-1 psql -U odoo -d SGCTECHAI -c \
  "SELECT key, value FROM ir_config_parameter WHERE key LIKE 'mail.%' ORDER BY key;"
```

---

## 🔐 Security Best Practices

### 1. Use App Passwords (Not Account Passwords)
- Never use your main email password
- Create app-specific passwords with limited scope
- Rotate passwords regularly (every 90 days)

### 2. Email Aliases
Configure separate aliases for different purposes:
- `noreply@scholarixglobal.com` - Automated notifications
- `support@scholarixglobal.com` - Customer support
- `crm@scholarixglobal.com` - CRM-related emails

### 3. SPF, DKIM, DMARC Records

Add DNS records for email authentication:

**SPF Record:**
```
v=spf1 include:_spf.google.com ~all
```

**DKIM:** Enable in Google Workspace → Apps → Gmail → Authenticate Email

**DMARC:**
```
v=DMARC1; p=quarantine; rua=mailto:dmarc@scholarixglobal.com
```

### 4. Monitor Email Logs

Check sent emails:
```bash
docker exec odoo19-db-1 psql -U odoo -d SGCTECHAI -c \
  "SELECT id, email_from, email_to, subject, state, failure_reason, create_date 
   FROM mail_mail 
   ORDER BY create_date DESC LIMIT 20;"
```

---

## 📊 Email Statistics

### View Email Queue
```sql
SELECT state, COUNT(*) 
FROM mail_mail 
GROUP BY state 
ORDER BY state;
```

### Failed Emails
```sql
SELECT id, email_to, subject, failure_reason, create_date 
FROM mail_mail 
WHERE state = 'exception' 
ORDER BY create_date DESC 
LIMIT 10;
```

### Recent Sent Emails
```sql
SELECT email_from, email_to, subject, create_date 
FROM mail_mail 
WHERE state = 'sent' 
ORDER BY create_date DESC 
LIMIT 20;
```

---

## 🚀 Next Steps

1. **Update Password** - Follow Option 1, 2, or 3 above
2. **Test Connection** - Use testing methods provided
3. **Configure Email Templates** - Go to Settings → Technical → Email Templates
4. **Set Up Notification Rules** - Configure user notification preferences
5. **Monitor Logs** - Check mail.mail table for delivery status

---

## 📞 Quick Commands Reference

### View Mail Server
```bash
docker exec odoo19-db-1 psql -U odoo -d SGCTECHAI -c \
  "SELECT * FROM ir_mail_server WHERE id=2;"
```

### Update Password Only
```bash
docker exec odoo19-db-1 psql -U odoo -d SGCTECHAI -c \
  "UPDATE ir_mail_server SET smtp_pass='NEW_PASSWORD' WHERE id=2;"
```

### Update Full Configuration
```bash
docker exec odoo19-db-1 psql -U odoo -d SGCTECHAI -c \
  "UPDATE ir_mail_server SET 
     smtp_host='smtp.gmail.com',
     smtp_port=587,
     smtp_user='noreply@scholarixglobal.com',
     smtp_pass='YOUR_APP_PASSWORD',
     smtp_encryption='starttls',
     smtp_authentication='login'
   WHERE id=2;"
```

### Delete and Recreate
```bash
# Delete existing
docker exec odoo19-db-1 psql -U odoo -d SGCTECHAI -c \
  "DELETE FROM ir_mail_server WHERE id=2;"

# Create new
docker exec odoo19-db-1 psql -U odoo -d SGCTECHAI -c \
  "INSERT INTO ir_mail_server 
   (name, smtp_host, smtp_port, smtp_user, smtp_pass, smtp_encryption, smtp_authentication, sequence, active, create_uid, write_uid, create_date, write_date) 
   VALUES 
   ('Scholarix Mail', 'smtp.gmail.com', 587, 'noreply@scholarixglobal.com', 'YOUR_PASSWORD', 'starttls', 'login', 10, true, 2, 2, now(), now());"
```

---

## ✅ Checklist

- [x] Mail server created in database
- [x] SMTP host configured (smtp.gmail.com)
- [x] Email address set (noreply@scholarixglobal.com)
- [x] Encryption enabled (STARTTLS)
- [x] System parameters configured
- [ ] **Password updated with real credentials**
- [ ] Connection tested successfully
- [ ] Test email sent and received
- [ ] DNS records configured (SPF/DKIM/DMARC)
- [ ] Email templates customized
- [ ] Monitoring set up

---

**Last Updated:** January 14, 2026  
**Status:** Awaiting password configuration  
**Next Action:** Update `smtp_pass` field with actual credentials

---

*For support, refer to Odoo documentation: https://www.odoo.com/documentation/19.0/applications/general/email_communication.html*
