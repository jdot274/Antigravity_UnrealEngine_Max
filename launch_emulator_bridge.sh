#!/bin/bash
# Antigravity Nexus Emulator Bridge
# Bridges the Local Host ports to a connected Android Emulator / Device via ADB

echo "bridge: Initializing Nexus <-> Android Link..."

# Check ADB
if ! command -v adb &> /dev/null; then
    echo "❌ Error: ADB not found. Please install Android Studio Platform Tools."
    echo "   brew install android-platform-tools"
    exit 1
fi

DEVICE=$(adb devices | grep -w "device" | head -n 1)

if [ -z "$DEVICE" ]; then
    echo "⚠️  No active Android Device/Emulator found."
    echo "   Please launch Android Studio Emulator or connect a device with USB Debugging."
    exit 1
fi

echo "✅ Device Detected. Configuring Reverse Port Forwarding..."

# 1. Signalling Server (WebSocket)
# Setup: Node.js (8888) -> Android (8888)
adb reverse tcp:8888 tcp:8888

# 2. Web Server (HTTP)
# Setup: Web Server (80 or 8000) -> Android (same)
# Assuming SignallingWebServer also serves HTTP on 80
adb reverse tcp:80 tcp:80
adb reverse tcp:8000 tcp:8000

echo "🔗 Bridge Established!"
echo "   On Emulator, open Chrome and navigate to: http://localhost:80"
echo "   The Touch Controller events will be forwarded to Unreal Engine."
