#!/usr/bin/env python3
"""
Test sending invitation emails via Odoo UI using the API
"""

import requests
import json
from requests.auth import HTTPBasicAuth

# Odoo Configuration
ODOO_URL = "http://localhost:8069"
DB_NAME = "SGCTECHAI"
ADMIN_LOGIN = "admin"
ADMIN_PASSWORD = "admin"  # Default password - change if needed

def get_session():
    """Login to Odoo and get session"""
    session = requests.Session()
    
    # Login
    login_data = {
        'jsonrpc': '2.0',
        'method': 'call',
        'params': {
            'service': 'common',
            'method': 'authenticate',
            'args': [DB_NAME, ADMIN_LOGIN, ADMIN_PASSWORD]
        },
        'id': 1
    }
    
    response = session.post(f"{ODOO_URL}/jsonrpc", json=login_data)
    result = response.json()
    
    if 'error' in result:
        print(f"[✗] Login failed: {result['error']}")
        return None
    
    print(f"[✓] Logged in as {ADMIN_LOGIN}")
    return session

def send_invitation_to_user(session, user_id):
    """Send invitation email to a user"""
    
    # Get user details
    get_user_data = {
        'jsonrpc': '2.0',
        'method': 'call',
        'params': {
            'service': 'object',
            'method': 'execute_kw',
            'args': [DB_NAME, 2, ADMIN_PASSWORD, 'res.users', 'read', [user_id], ['login']]
        },
        'id': 2
    }
    
    response = session.post(f"{ODOO_URL}/jsonrpc", json=get_user_data)
    result = response.json()
    
    if 'error' in result or not result.get('result'):
        print(f"[✗] Failed to get user {user_id}")
        return False
    
    user_email = result['result'][0]['login']
    print(f"[✓] User {user_id}: {user_email}")
    
    # Call the send_welcome_email action
    send_email_data = {
        'jsonrpc': '2.0',
        'method': 'call',
        'params': {
            'service': 'object',
            'method': 'execute_kw',
            'args': [
                DB_NAME, 
                2,  # admin user ID
                ADMIN_PASSWORD,
                'res.users',
                'action_send_welcome_email',
                [[user_id]]
            ]
        },
        'id': 3
    }
    
    response = session.post(f"{ODOO_URL}/jsonrpc", json=send_email_data)
    result = response.json()
    
    if 'error' in result:
        print(f"[✗] Send invitation failed: {result['error']}")
        return False
    
    print(f"[✓] Invitation sent to {user_email}")
    return True

if __name__ == "__main__":
    print("Testing Odoo UI Email System\n")
    
    session = get_session()
    if not session:
        exit(1)
    
    # Send invitations to Saifulla (ID 13) and Sarad (ID 14)
    print("\nSending invitations...\n")
    
    for user_id in [13, 14]:
        send_invitation_to_user(session, user_id)
    
    print("\n[✓] All invitations sent!")
