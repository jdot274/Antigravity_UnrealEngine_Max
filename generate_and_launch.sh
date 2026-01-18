#!/bin/bash
# Generate content and launch game
set -e

UE5_PATH="/Users/Shared/Epic Games/UE_5.7/Engine/Binaries/Mac/UnrealEditor.app/Contents/MacOS/UnrealEditor"
PROJECT_PATH="/Users/joeywalter/antigravity-nexus/AntigravityTwin.uproject"

echo "⚙️  GENERATING ASSETS (Running aaa_generator.py)..."
"$UE5_PATH" "$PROJECT_PATH" -run=PythonScript -script="Content/Python/utils/aaa_generator.py" -Unattended -Log

echo "🚀 LAUNCHING GAME (Antigravity_Showcase)..."
"$UE5_PATH" "$PROJECT_PATH" -game -map=/Game/FuturisticSystems/Maps/Antigravity_Showcase \
    -ResX=3840 -ResY=2160 -ForceRes \
    -FixedFPS=90 -UseFixedFPS=true \
    -log
