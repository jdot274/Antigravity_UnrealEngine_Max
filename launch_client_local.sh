#!/bin/bash
# Local Launch Script for Antigravity Nexus with Pixel Streaming
# Connects to the locally running Signalling Server (ws://127.0.0.1:8888)

# Paths (Adjust if your UE5 installation is elsewhere)
UE5_PATH="/Users/Shared/Epic Games/UE_5.5/Engine/Binaries/Mac/UnrealEditor.app/Contents/MacOS/UnrealEditor"
PROJECT_PATH="$(pwd)/AntigravityTwin.uproject"

# Configuration from Manifest (Hardcoded here for shell simplicity, but matches JSON)
PS_URL="ws://127.0.0.1:8888"

echo "🚀 Launching Antigravity Nexus Client..."
echo "🔗 Connecting to Signalling Server at $PS_URL"

# Launch Command
# -game: Run in game mode (standalone)
# -PixelStreamingURL: Connect to the server
# -RenderOffscreen: Optional, keeps it headless if you only view via Web
# -ResX=1920 -ResY=1080: Standard resolution

"$UE5_PATH" "$PROJECT_PATH" -game -PixelStreamingURL="$PS_URL" -ResX=1920 -ResY=1080 -log

echo "✅ Client Launched."
