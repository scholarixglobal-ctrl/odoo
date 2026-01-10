#!/bin/bash

# Test Voice Assistant Setup
echo "Testing Voice Assistant Module..."
echo "=================================="

# Check module registration
docker exec odoo19-odoo-1 python3 << 'PYEOF'
import sys
sys.path.insert(0, '/usr/lib/python3/dist-packages')

# Just verify openai is working
try:
    import openai
    print("✅ OpenAI package installed and working")
except Exception as e:
    print(f"❌ OpenAI import failed: {e}")

# List addons path
print("\n📁 Checking module location:")
import os
voice_path = '/mnt/custom-addons/voice_assistant'
if os.path.exists(voice_path):
    print(f"✅ Module found at: {voice_path}")
    print(f"   Files: {os.listdir(voice_path)}")
else:
    print(f"❌ Module not found at: {voice_path}")

PYEOF

echo ""
echo "=================================="
echo "Module Installation Steps:"
echo "1. Open: http://192.168.0.157:8069"
echo "2. Login with your admin credentials"
echo "3. Go to: Settings → Apps"
echo "4. Search: 'voice_assistant' or 'OpenAI'"
echo "5. Click Install"
echo "6. Go to: Voice Assistant → Voice Messages"
echo ""
echo "Ready to test!"
