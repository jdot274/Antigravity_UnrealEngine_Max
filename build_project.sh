#!/bin/bash
# Antigravity Nexus Compilation Script
# Compiles the C++ Modules (NexusRuntime) for Mac

echo "🛠️  NexusBuilder: Starting Compilation..."

# Path to Unreal Engine Build Tool
# Adjust version if needed (5.5, 5.6, 5.7)
UE_ENGINE_PATH="/Users/Shared/Epic Games/UE_5.7/Engine"
BUILD_SH="$UE_ENGINE_PATH/Build/BatchFiles/Mac/Build.sh"
PROJECT_PATH="$(pwd)/AntigravityTwin.uproject"

if [ ! -f "$BUILD_SH" ]; then
    echo "❌ Error: Build.sh not found at $BUILD_SH"
    echo "   Please check your Unreal Engine installation path."
    exit 1
fi

echo "   -> Target: AntigravityTwinEditor"
echo "   -> Platform: Mac"
echo "   -> Config: Development"

"$BUILD_SH" AntigravityTwinEditor Mac Development -Project="$PROJECT_PATH" -WaitMutex -FromMsBuild

if [ $? -eq 0 ]; then
    echo "✅ Compilation Complete. You can now launch the project."
    echo "   Run: ./launch_client_local.sh"
else
    echo "❌ Compilation Failed. See output above."
fi
