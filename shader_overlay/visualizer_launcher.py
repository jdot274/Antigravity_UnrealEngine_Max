import subprocess
import json
import sys
import os

def launch_visualizer(options):
    options_json = json.dumps(options)
    # Using the venv python to ensure PySide6 is available
    venv_python = "/Users/joeywalter/antigravity-nexus/shader_overlay/venv/bin/python3"
    script_path = "/Users/joeywalter/antigravity-nexus/shader_overlay/visualizer_engine.py"
    
    # Run in background
    cmd = [venv_python, script_path, options_json]
    subprocess.Popen(cmd, start_new_session=True)
    print("🚀 Visualizer Mode Active: Bubbles manifest on screen.")

if __name__ == "__main__":
    # Context: UNREAL TENNIS BALL PHYSICS ARCHITECTURE
    options = [
        {
            "id": "METAL_HUD",
            "title": "METAL 3 PHYSICS HUD",
            "description": "Render tennis ball physics via Native Metal. High frequency, zero collision lag with OS windows."
        },
        {
            "id": "UE_CONTAINER",
            "title": "UNREAL CONTAINER BOX",
            "description": "Spawn a dedicated Level Instance pod. Frameless transparent bridge window shows the ball in isolation."
        },
        {
            "id": "SOCKET_PROXY",
            "title": "PYBULLET SOCKET PROXY",
            "description": "Independent physics solver. Predicts ball bounce outside of Unreal, then syncs coordinates to the main engine."
        },
        {
            "id": "SPATIAL_PORTAL",
            "title": "SPATIAL AUDIT PORTAL",
            "description": "A 'Magic Mirror' window. The ball stays in Unreal but is visually projected anywhere on your macOS desktop."
        }
    ]
    launch_visualizer(options)
