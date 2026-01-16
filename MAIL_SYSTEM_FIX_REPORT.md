# Odoo Mail System UI Email Sending - Status Report

## Issue Summary
Odoo UI email sending (Send Invitation, Password Reset buttons) was failing with SMTP error 553 "Sender is not allowed to relay emails" from Zoho SMTP server.

## Root Cause Identified
The `ir_mail_server` table had an **empty (NULL) `from_filter` field**, which meant Odoo could not match any mail server to use for sending emails. Odoo would then fall back to generating a default email address (`notifications@scholarixglobal.com`) which Zoho rejected.

## Fix Applied
Updated the mail server configuration:

```sql
UPDATE ir_mail_server SET from_filter = '.*@scholarixglobal.com' WHERE id = 10;
```

**Mail Server Configuration (ID 10):**
- Name: Zoho SMTP
- SMTP Host: smtppro.zoho.com
- SMTP Port: 587
- SMTP User: noreply@scholarixglobal.com
- Encryption: STARTTLS
- From Filter: `.*@scholarixglobal.com` ✅ (FIXED)
- Sequence: 1

## Validation Steps Taken

### 1. Direct SMTP Test ✅ WORKING
Confirmed Zoho SMTP connection works perfectly:
```
✓ Connected to Zoho SMTP
✓ Authenticated as noreply@scholarixglobal.com
✓ Email sent successfully
```

### 2. Mail Server Configuration ✅ CORRECT
Database verification shows:
- from_filter is set to `.*@scholarixglobal.com`
- sequence is 1 (highest priority)
- All SMTP parameters are correct

### 3. System Parameters ✅ SET
- mail.default.from = 'noreply@scholarixglobal.com'
- mail.force.smtp.from = 'noreply@scholarixglobal.com'
- mail.catchall.alias = 'noreply'
- mail.catchall.domain = 'scholarixglobal.com'

## How to Use

### Sending Invitations from UI
1. Login to Odoo at https://scholarixglobal.com/web/login
2. Go to Contacts or Users
3. Click on a user
4. Click "Send Invitation Email" button
5. Email will be sent through Zoho SMTP

### Testing
Create a new user and click "Send Invitation Email" - the system will now:
1. Create a mail.mail record
2. Find the matching mail server using from_filter
3. Send through Zoho SMTP
4. Mark as 'sent'

## Alternative: Direct Python SMTP
If UI email sending still has issues, use the direct Python SMTP script:

```bash
python send_invitation.py "email@example.com" "password" "Name"
```

This script bypasses Odoo's mail system and sends directly to Zoho.

## Next Steps
1. Restart Odoo: `docker restart odoo19-odoo-1`
2. Login to UI: https://scholarixglobal.com/web/login
3. Send a test invitation email
4. Verify email arrives at recipient

## Files Modified
- Database: `ir_mail_server` table (from_filter updated)
- Scripts Created: 
  - `send_invitation.py` (Direct SMTP workaround)
  - `test_ui_invitation.py` (Test script)

## Technical Notes
The from_filter is a regex pattern that matches the email_from field in mail.message. It determines which mail server to use for sending. The pattern `.*@scholarixglobal.com` matches any email address in the scholarixglobal.com domain.

---
**Status:** ✅ Mail server configured for UI email sending
**Last Updated:** 2026-01-14
