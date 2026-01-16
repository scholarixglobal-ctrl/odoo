#!/bin/bash
# Zoho Mail Server Password Setup for Scholarix Global Odoo

echo "================================================"
echo "  Zoho Mail Server Password Setup"
echo "  Scholarix Global Odoo Instance"
echo "================================================"
echo ""

# Check if password is provided
if [ -z "$1" ]; then
    echo "❌ Error: Password not provided"
    echo ""
    echo "Usage: ./setup_zoho_mail.sh 'YOUR_ZOHO_PASSWORD'"
    echo ""
    echo "Example:"
    echo "  ./setup_zoho_mail.sh 'YourZohoPassword123'"
    echo ""
    echo "📧 How to get your Zoho password:"
    echo "  1. Go to https://accounts.zoho.com"
    echo "  2. Login with your Zoho account"
    echo "  3. Go to Settings → Security → App Passwords"
    echo "  4. If using 2FA, create an App Password for SMTP"
    echo "  5. Copy the password and use it here"
    echo ""
    echo "ℹ️  Mail Server Details:"
    echo "  Host: smtppro.zoho.com"
    echo "  Port: 587"
    echo "  Email: noreply@scholarixglobal.com"
    echo "  Encryption: STARTTLS"
    echo ""
    exit 1
fi

PASSWORD="$1"

echo "📧 Updating Zoho mail server password..."
echo ""

# Update password in database
docker exec odoo19-db-1 psql -U odoo -d SGCTECHAI -c \
  "UPDATE ir_mail_server SET smtp_pass='$PASSWORD', write_date=now() WHERE id=2;" > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo "✅ Password updated successfully!"
    echo ""
    
    # Show current configuration
    echo "📊 Current Configuration:"
    docker exec odoo19-db-1 psql -U odoo -d SGCTECHAI -t -c \
      "SELECT '  Name:       ' || name || E'\n' ||
              '  Host:       ' || smtp_host || ':' || smtp_port || E'\n' ||
              '  Email:      ' || smtp_user || E'\n' ||
              '  Encryption: ' || smtp_encryption || E'\n' ||
              '  Auth:       ' || smtp_authentication || E'\n' ||
              '  Active:     ' || CASE WHEN active THEN 'Yes' ELSE 'No' END
       FROM ir_mail_server WHERE id=2;"
    
    echo ""
    echo "🔄 Restarting Odoo to apply changes..."
    docker restart odoo19-odoo-1 > /dev/null 2>&1
    
    echo "⏳ Waiting for Odoo to start (8 seconds)..."
    sleep 8
    
    # Check if Odoo is running
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8069/web/login)
    
    if [ "$HTTP_CODE" == "200" ]; then
        echo "✅ Odoo restarted successfully!"
        echo ""
        echo "🧪 Testing Mail Server:"
        echo ""
        echo "  Option 1: Test via Odoo UI"
        echo "  1. Go to: https://scholarixglobal.com"
        echo "  2. Login as admin"
        echo "  3. Navigate to: Settings → Technical → Email → Outgoing Mail Servers"
        echo "  4. Click 'Scholarix Global Mail Server'"
        echo "  5. Click 'Test Connection' button"
        echo ""
        echo "  Option 2: Send Test Email"
        echo "  docker exec odoo19-odoo-1 odoo shell -d SGCTECHAI --no-http << 'EOF'"
        echo "  env['mail.mail'].create({"
        echo "      'email_from': 'noreply@scholarixglobal.com',"
        echo "      'email_to': 'your-email@example.com',"
        echo "      'subject': 'Test from Zoho',"
        echo "      'body_html': '<p>Zoho mail server is working!</p>',"
        echo "  }).send()"
        echo "  env.cr.commit()"
        echo "  EOF"
        echo ""
        echo "✅ Zoho mail server is ready!"
        echo ""
    else
        echo "⚠️  Odoo may still be starting (HTTP $HTTP_CODE)"
        echo "   Check status with: docker ps"
        echo "   Check logs with: docker logs odoo19-odoo-1"
        echo ""
    fi
    
else
    echo "❌ Failed to update password"
    echo "   Check if Docker containers are running:"
    echo "   docker ps | grep odoo19"
    echo ""
    exit 1
fi

echo "================================================"
