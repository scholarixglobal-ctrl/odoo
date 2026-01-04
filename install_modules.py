#!/usr/bin/env python3
"""
Install essential OdooMates and Cybro modules into Odoo 19
"""
import os
import sys
sys.path.insert(0, '/odoo')

# Essential modules to install (minimal core set)
ESSENTIAL_MODULES = [
    # OdooMates core modules (if they exist)
    # 'base_address_extended',  # Extended address fields
    # 'account_banking',  # Banking features
    
    # Cybro essential modules
    'access_roles',                    # Role-based access control
    'base_accounting_kit',             # Accounting enhancements  
    'advanced_json_widget',            # JSON widget for forms
    'auto_database_backup',            # Automated database backups
    'dark_mode_backend',               # Dark mode UI
    'hide_chatter',                    # Hide chatter for cleaner UI
]

os.environ['PGHOST'] = 'db'
os.environ['PGUSER'] = 'odoo'
os.environ['PGPASSWORD'] = 'odoo'

if __name__ == '__main__':
    # Connect to Odoo and update module list
    import odoo
    from odoo.cli import main
    
    # Update module list first
    sys.argv = ['odoo', '--config=/etc/odoo/odoo.conf', '-d', 'scholarix', 
                '--db_host=db', '--db_user=odoo', '--db_password=odoo',
                '-u', ','.join(ESSENTIAL_MODULES), '--stop-after-init']
    
    try:
        main()
        print(f"\n✓ Successfully installed {len(ESSENTIAL_MODULES)} essential modules")
    except Exception as e:
        print(f"✗ Error installing modules: {e}")
        sys.exit(1)
