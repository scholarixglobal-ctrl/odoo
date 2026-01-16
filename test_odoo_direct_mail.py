#!/usr/bin/env python3
"""
Direct Odoo API test to send invitation emails
Run inside Odoo container
"""

import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Setup Odoo environment
import odoo
from odoo import api, fields, models
from odoo.cli import main

# Alternative: Just use system command to trigger email send
if __name__ == "__main__":
    # Start Odoo in a test mode with direct Python access
    import subprocess
    
    # Create Python snippet to execute
    python_code = """
import odoo
from odoo.sql_db import sql_db

# Setup environment
os.environ['ODOO_RC'] = '/etc/odoo/odoo.conf'

# Connect to database
db = odoo.sql_db.db_connect('SGCTECHAI')
cr = db.cursor()

# Get Odoo environment
from odoo.api import Environment
env = Environment(cr, 2, {})  # uid=2 is admin

# Get the mail.mail model
mail_obj = env['mail.mail']

# Create a test email
mail_values = {
    'subject': 'Test Email from Odoo UI',
    'body_html': '<p>This is a test email from Odoo UI</p>',
    'email_from': 'noreply@scholarixglobal.com',
    'email_to': 'sarad.p@scholarixit.com',
    'state': 'outgoing',
}

mail = mail_obj.create(mail_values)
print(f"[✓] Created mail record: {mail.id}")

# Send it
mail.send()
print("[✓] Email sent via Odoo mail system!")

cr.close()
"""
    
    # Write and execute
    with open('/tmp/test_send_mail.py', 'w') as f:
        f.write(python_code)
    
    subprocess.run(['python', '/tmp/test_send_mail.py'])
