#!/usr/bin/env python3
"""
Install essential modules using Odoo Python API
"""
import os
import sys
import django

# Set up environment
os.environ['DJANGO_SETTINGS_MODULE'] = 'odoo.settings'
os.environ.setdefault('PGHOST', 'db')
os.environ.setdefault('PGUSER', 'odoo')
os.environ.setdefault('PGPASSWORD', 'odoo')

sys.path.insert(0, '/odoo')

# Import after path is set
import odoo
from odoo import api, fields, models
from odoo.cli import main as odoo_main

# List of essential modules to install  
MODULES_TO_INSTALL = [
    'access_roles',
    'base_accounting_kit',
    'advanced_json_widget',
    'auto_database_backup',
    'dark_mode_backend',
    'hide_chatter'
]

def install_modules():
    """Install modules into Odoo database"""
    try:
        # Switch to odoo directory
        os.chdir('/odoo')
        
        # Run Odoo with module update flags
        sys.argv = [
            'odoo',
            '--config=/etc/odoo/odoo.conf',
            '--db_host=db',
            '--db_user=odoo',
            '--db_password=odoo',
            '-d', 'scholarix',
            '-u', ','.join(MODULES_TO_INSTALL),
            '--without-demo=all',
            '--stop-after-init'
        ]
        
        # Execute Odoo
        odoo_main()
        print(f"\n✓ Successfully installed {len(MODULES_TO_INSTALL)} modules!")
        return 0
        
    except Exception as e:
        print(f"✗ Error installing modules: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(install_modules())
