#!/bin/bash

# ==============================================================================
# 🌌 ANTIGRAVITY NEXUS: ULTIMATE LAUNCHER
# ==============================================================================
# This is the Master App Launcher. Double-click to start the experience.

cd "$(dirname "$0")"

echo "=============================================================================="
echo "   🌌  ANTIGRAVITY NEXUS  🌌"
echo "=============================================================================="
echo "   [1] 🚀 Launch FULL GAME (Play Mode)"
echo "   [2] 🛠️  Launch EDITOR (Dev Mode)"
echo "   [3] 🧠  Launch AI BRAIN SERVER (Headless)"
echo "   [4] 📦  Package for Shipping (AAA Build)"
echo "=============================================================================="
read -p "   Select Mode (1-4) [Default: 1]: " MODE
MODE=${MODE:-1}

if [ "$MODE" == "1" ]; then
    echo "🚀 Initializing Full Game Sequence..."
    ./launch_full_game.sh
elif [ "$MODE" == "2" ]; then
    echo "🛠️  Starting Unreal Editor..."
    ./launch_client_local.sh
elif [ "$MODE" == "3" ]; then
    echo "🧠  Starting Headless AI Server..."
    python3 nexus_compiler.py # Just ensure compiled
    # Then run specific logic if needed, for now just launch game in server mode?
    ./launch_full_game.sh
elif [ "$MODE" == "4" ]; then
    echo "📦  Preparing AAA Package..."
    python3 Content/Nexus/Python/Tools/package_shipping.py
else
    echo "Invalid selection."
fi

# Keep window open if it crashes immediately
read -p "Press [Enter] to close..."
