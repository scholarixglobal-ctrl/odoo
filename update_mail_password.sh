#!/bin/bash
# Mail Server Password Update Script for Scholarix Global Odoo

echo "================================================"
echo "  Scholarix Global Mail Server Password Setup  "
echo "================================================"
echo ""

# Check if password is provided
if [ -z "$1" ]; then
    echo "❌ Error: Password not provided"
    echo ""
    echo "Usage: ./update_mail_password.sh 'YOUR_APP_PASSWORD'"
    echo ""
    echo "Examples:"
    echo "  Gmail App Password:        ./update_mail_password.sh 'abcd efgh ijkl mnop'"
    echo "  Microsoft 365:             ./update_mail_password.sh 'your-password'"
    echo "  Other SMTP:                ./update_mail_password.sh 'api-key-or-password'"
    echo ""
    echo "For Gmail:"
    echo "  1. Go to https://myaccount.google.com/security"
    echo "  2. Enable 2-Step Verification"
    echo "  3. Go to App Passwords"
    echo "  4. Create new app password for 'Mail' on 'Odoo Server'"
    echo "  5. Copy the 16-character password"
    echo ""
    exit 1
fi

PASSWORD="$1"

echo "📧 Updating mail server password..."
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
      "SELECT '  Host:       ' || smtp_host || ':' || smtp_port || E'\n' ||
              '  Email:      ' || smtp_user || E'\n' ||
              '  Encryption: ' || smtp_encryption || E'\n' ||
              '  Auth:       ' || smtp_authentication || E'\n' ||
              '  Active:     ' || CASE WHEN active THEN 'Yes' ELSE 'No' END
       FROM ir_mail_server WHERE id=2;"
    
    echo ""
    echo "🔄 Restarting Odoo to apply changes..."
    docker restart odoo19-odoo-1 > /dev/null 2>&1
    
    echo "⏳ Waiting for Odoo to start..."
    sleep 8
    
    # Check if Odoo is running
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8069/web/login)
    
    if [ "$HTTP_CODE" == "200" ]; then
        echo "✅ Odoo restarted successfully!"
        echo ""
        echo "🧪 Next Steps:"
        echo "  1. Go to: https://scholarixglobal.com"
        echo "  2. Login as admin"
        echo "  3. Navigate to: Settings → Technical → Email → Outgoing Mail Servers"
        echo "  4. Click 'Scholarix Global Mail Server'"
        echo "  5. Click 'Test Connection' button"
        echo ""
        echo "  Or send a test email:"
        echo "  docker exec odoo19-odoo-1 odoo shell -d SGCTECHAI --no-http << 'EOF'"
        echo "  env['mail.mail'].create({"
        echo "      'email_from': 'noreply@scholarixglobal.com',"
        echo "      'email_to': 'your-email@example.com',"
        echo "      'subject': 'Test from Odoo',"
        echo "      'body_html': '<p>Mail server is working!</p>',"
        echo "  }).send()"
        echo "  env.cr.commit()"
        echo "  EOF"
        echo ""
    else
        echo "⚠️  Odoo may still be starting (HTTP $HTTP_CODE)"
        echo "   Check status with: docker ps"
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
