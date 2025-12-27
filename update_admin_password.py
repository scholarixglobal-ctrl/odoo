#!/usr/bin/env python3
import sys
import os

# Add Odoo to path
sys.path.insert(0, os.path.dirname(__file__))

import odoo
from odoo import api, SUPERUSER_ID

# Configure Odoo
odoo.tools.config.parse_config(['-c', 'odoo.conf', '-d', 'odoo_db'])

# Initialize registry
with odoo.api.Environment.manage():
    registry = odoo.registry('odoo_db')
    with registry.cursor() as cr:
        env = api.Environment(cr, SUPERUSER_ID, {})

        # Find admin user
        admin = env['res.users'].search([('login', '=', 'admin')], limit=1)

        if admin:
            # Update password
            admin.write({'password': '8586583'})
            cr.commit()
            print(f"Password updated successfully for user: {admin.login}")
        else:
            print("Admin user not found!")

print("Done!")
