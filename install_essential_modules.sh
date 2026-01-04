#!/bin/bash
# Install essential OdooMates and Cybro modules into Odoo 19
# This script marks modules for installation by updating their state in the database

echo "Installing essential modules into Odoo 19..."

# List of essential modules to install
MODULES="access_roles,base_accounting_kit,advanced_json_widget,auto_database_backup,dark_mode_backend,hide_chatter"

# Execute the Odoo upgrade command
cd /odoo
python odoo-bin \
  --config=/etc/odoo/odoo.conf \
  --db_host=db \
  --db_user=odoo \
  --db_password=odoo \
  -d scholarix \
  -u "$MODULES" \
  --without-demo=all \
  --stop-after-init

echo "Module installation complete!"
