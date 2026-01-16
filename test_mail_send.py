#!/usr/bin/env python3
"""
Test mail sending through Odoo's mail.mail system
This script directly sends an email via the mail system
"""

import subprocess
import time

def send_test_mail():
    """Send a test email through Odoo's mail system"""
    
    # SQL to insert a mail record
    sql = """
INSERT INTO mail_mail (
    subject,
    body_html,
    email_from,
    email_to,
    reply_to,
    state,
    create_date,
    write_date,
    create_uid,
    write_uid
) VALUES (
    'Test: Odoo Mail System with Fixed from_filter',
    '<h2>Success Test</h2><p>This email was sent through Odoo mail system with from_filter=.*@scholarixglobal.com</p><p>The mail server selection should now work correctly!</p>',
    'noreply@scholarixglobal.com',
    'sarad.p@scholarixit.com',
    'noreply@scholarixglobal.com',
    'outgoing',
    NOW(),
    NOW(),
    2,
    2
)
RETURNING id;
"""
    
    print("[...] Sending test email through Odoo mail system...")
    
    # Execute SQL
    result = subprocess.run(
        [
            'docker', 'exec', 'odoo19-db-1',
            'psql', '-U', 'odoo', '-d', 'SGCTECHAI',
            '-c', sql
        ],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print(f"[✗] Database error: {result.stderr}")
        return False
    
    mail_id = result.stdout.strip().split('\n')[-2]
    print(f"[✓] Created mail record ID: {mail_id}")
    
    # Wait for email processing
    print("[...] Waiting for mail system to process email (15 seconds)...")
    time.sleep(15)
    
    # Check if email was sent
    check_sql = f"SELECT state FROM mail_mail WHERE id = {mail_id};"
    
    result = subprocess.run(
        [
            'docker', 'exec', 'odoo19-db-1',
            'psql', '-U', 'odoo', '-d', 'SGCTECHAI',
            '-c', check_sql
        ],
        capture_output=True,
        text=True
    )
    
    state_output = result.stdout.strip().split('\n')[-2]
    print(f"[*] Mail state: {state_output}")
    
    if 'sent' in state_output.lower():
        print("[✓✓✓] SUCCESS! Email was SENT!")
        return True
    elif 'exception' in state_output.lower() or 'failed' in state_output.lower():
        print("[✗] Email failed to send, checking logs...")
        return False
    else:
        print(f"[~] Email in state: {state_output}")
        return None

if __name__ == "__main__":
    print("=== Odoo Mail System Test ===\n")
    print("Testing mail sending with fixed from_filter configuration\n")
    
    result = send_test_mail()
    
    print("\n=== Test Complete ===")
    if result is True:
        print("✓ Mail system is working correctly!")
        print("✓ You can now send invitations from the Odoo UI!")
    else:
        print("✗ Mail system still has issues, checking Docker logs...")
        # Show relevant logs
        subprocess.run([
            'bash', '-c',
            'cd /c/odoo19 && docker logs odoo19-odoo-1 2>&1 | grep -i "mail\|from_filter\|zoho\|smtp" | tail -20'
        ])
