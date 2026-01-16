#!/usr/bin/env python3
"""
Send invitation emails to Scholarix Global CRM users
Usage: python send_invitation.py <email_address> [password]
"""

import smtplib
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Zoho SMTP Configuration
SMTP_HOST = "smtppro.zoho.com"
SMTP_PORT = 587
SMTP_USER = "noreply@scholarixglobal.com"
SMTP_PASSWORD = "0zustjGh3XR0"
SENDER_NAME = "Scholarix Global"
LOGIN_URL = "https://scholarixglobal.com/web/login"

def send_invitation(email, password=None, name=None):
    """Send invitation email to a user"""
    
    try:
        # Connect to Zoho SMTP
        smtp = smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=10)
        smtp.starttls()
        smtp.login(SMTP_USER, SMTP_PASSWORD)
        print(f"[✓] Connected to Zoho SMTP")
        
        # Create email
        msg = MIMEMultipart('alternative')
        msg['Subject'] = 'Scholarix Global - Account Invitation'
        msg['From'] = f'{SENDER_NAME} <{SMTP_USER}>'
        msg['To'] = email
        
        # Prepare content
        user_name = name if name else email.split('@')[0]
        password_line = f"<br>Password: <strong>{password}</strong>" if password else ""
        
        # Plain text
        text = f"""Dear {user_name},

You have been invited to join Scholarix Global CRM Platform.

Login Details:
URL: {LOGIN_URL}
Username: {email}
{f'Password: {password}' if password else '(Use password reset if needed)'}

Welcome to the team!

Scholarix Global Support Team"""
        
        # HTML
        html = f"""<html><body style="font-family: Arial; color: #333;">
<div style="max-width: 600px; margin: 0 auto; padding: 20px;">
<div style="background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%); color: white; padding: 30px; text-align: center; border-radius: 8px 8px 0 0;">
<h1 style="margin: 0; font-size: 28px;">Welcome to Scholarix Global</h1>
<p style="margin: 10px 0 0 0; opacity: 0.9;">CRM Platform</p>
</div>
<div style="background: #f9fafb; padding: 30px; border: 1px solid #e5e7eb;">
<p>Dear <strong>{user_name}</strong>,</p>
<p>You have been invited to join <strong>Scholarix Global CRM Platform</strong>.</p>
<div style="background: white; padding: 20px; border-left: 4px solid #10B981; border-radius: 4px; margin: 20px 0;">
<h3 style="color: #1E3A8A; margin-top: 0;">Login Details</h3>
<p><strong>URL:</strong> <a href="{LOGIN_URL}" style="color: #0066cc;">{LOGIN_URL}</a></p>
<p><strong>Username:</strong> {email}</p>{password_line}
</div>
<p style="margin-top: 30px;">Welcome to the team!<br><strong>Scholarix Global Support</strong></p>
</div>
<div style="background: #1E3A8A; color: white; padding: 20px; text-align: center; border-radius: 0 0 8px 8px; font-size: 12px;">
<p style="margin: 5px 0;">Scholarix Global - CRM Platform</p>
<p style="margin: 5px 0; opacity: 0.8;">© 2026 Scholarix Global. All rights reserved.</p>
</div>
</div>
</body></html>"""
        
        # Attach
        msg.attach(MIMEText(text, 'plain'))
        msg.attach(MIMEText(html, 'html'))
        
        # Send
        smtp.send_message(msg)
        smtp.quit()
        
        print(f"[✓] Invitation email sent to: {email}")
        return True
        
    except Exception as e:
        print(f"[✗] Error: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python send_invitation.py <email> [password] [name]")
        print()
        print("Example:")
        print('  python send_invitation.py sarad.p@scholarixit.com "CPR82@1nPe#0" "Sarad Pandeya"')
        sys.exit(1)
    
    email = sys.argv[1]
    password = sys.argv[2] if len(sys.argv) > 2 else None
    name = sys.argv[3] if len(sys.argv) > 3 else None
    
    success = send_invitation(email, password, name)
    sys.exit(0 if success else 1)
