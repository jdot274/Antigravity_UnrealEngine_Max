#!/bin/bash
# MCPViewer Compilation Script
# Compiles the C++ Modules for Mac

echo "🛠️  MCPViewer: Starting Compilation..."

# Path to Unreal Engine Build Tool
# Adjust version if needed (5.5, 5.6, 5.7)
UE_ENGINE_PATH="/Users/Shared/Epic Games/UE_5.7/Engine"
BUILD_SH="$UE_ENGINE_PATH/Build/BatchFiles/Mac/Build.sh"
PROJECT_PATH="$(pwd)/MCPViewer/MCPViewer.uproject"

if [ ! -f "$BUILD_SH" ]; then
    echo "❌ Error: Build.sh not found at $BUILD_SH"
    echo "   Please check your Unreal Engine installation path."
    exit 1
fi

echo "   -> Target: MCPViewerEditor"
echo "   -> Platform: Mac"
echo "   -> Config: Development"

"$BUILD_SH" MCPViewerEditor Mac Development -Project="$PROJECT_PATH" -WaitMutex -FromMsBuild

if [ $? -eq 0 ]; then
    echo "✅ Compilation Complete. You can now launch the project."
else
    echo "❌ Compilation Failed. See output above."
fi
