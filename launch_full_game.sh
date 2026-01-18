#!/bin/bash
# Hard Reset Launch Script
# Kills stale processes and relaunches everything fresh.

# Ensure Node/NPM is available
export PATH="/Users/joeywalter/.nvm/versions/node/v24.11.1/bin:$PATH"

echo "🛑 KILLING ZOMBIE PROCESSES..."
pkill -9 "UnrealEditor"
pkill -9 "node" # Kills Signalling Server

echo "🧹 Cleaning session..."
sleep 2

# 1. Start Signal Server (Background)
echo "📡 Starting Signaling Server..."
# Assuming standard Pixel Streaming location
NODE_SERVER_PATH="/Users/Shared/Epic Games/UE_5.7/Engine/Plugins/Media/PixelStreaming/Resources/WebServers/SignallingWebServer/platform_scripts/bash/start.sh"

if [ -f "$NODE_SERVER_PATH" ]; then
    echo "📡 Starting Epic Signaling Server..."
    "$NODE_SERVER_PATH" --publicIp="127.0.0.1" --httpPort=8080 &
    SERVER_PID=$!
else
    echo "⚠️  Epic Server not found. Launching Local Bridge..."
    # Ensure dependencies are installed
    if [ ! -d "bridge/SignallingWebServer/node_modules" ]; then
        echo "📦 Installing Server Dependencies..."
        cd bridge/SignallingWebServer && npm install && cd ../..
    fi
    
    cd bridge/SignallingWebServer && npm start -- --publicIp="127.0.0.1" --httpPort=8080 &
    SERVER_PID=$!
    cd ../..
fi

sleep 3

# 2. Launch Client
echo "🚀 Launching Nexus Engine (Game Mode)..."

UE5_PATH="/Users/Shared/Epic Games/UE_5.7/Engine/Binaries/Mac/UnrealEditor.app/Contents/MacOS/UnrealEditor"
# Hardcoded absolute path to ensure accurate launching regardless of shell context
PROJECT_PATH="/Users/joeywalter/antigravity-nexus/AntigravityTwin.uproject"
PS_URL="ws://127.0.0.1:8888"

# Added -AudioMixer to ensure audio
# 4K (3840x2160) @ 90 FPS Configuration
"$UE5_PATH" "$PROJECT_PATH" -game -PixelStreamingURL="$PS_URL" \
    -ResX=3840 -ResY=2160 -ForceRes \
    -FixedFPS=90 -UseFixedFPS=true \
    -PixelStreamingEncoderRateControl=CBR \
    -PixelStreamingEncoderTargetBitrate=50000000 \
    -PixelStreamingWebRTCMaxBitrate=50000000 \
    -log

echo "✅ Session Ended."
