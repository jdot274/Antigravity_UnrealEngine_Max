import subprocess
import time
import os
import json

# Paths
VENV_PYTHON = "/Users/joeywalter/antigravity-nexus/shader_overlay/venv/bin/python3"
NOTIFIER_SCRIPT = "/Users/joeywalter/antigravity-nexus/shader_overlay/nexus_notifier.py"
EDITOR_SCRIPT = "/Users/joeywalter/antigravity-nexus/shader_overlay/nexus_editor.py"
MONITOR_SCRIPT = "/Users/joeywalter/antigravity-nexus/shader_overlay/universe_monitor.py"
AI_BRIDGE = "/Users/joeywalter/antigravity-nexus/shader_overlay/ai_engine_bridge.py"
PUSH_NOTIF = "/Users/joeywalter/antigravity-nexus/shader_overlay/push_notif.py"

def launch_all():
    print("🚀 Initializing Nexus Master Environment...")
    
    # 0. Launch AI Engine Bridge
    subprocess.Popen([VENV_PYTHON, AI_BRIDGE], start_new_session=True)
    time.sleep(1)

    # 1. Launch Notifier (Hidden stack)
    subprocess.Popen([VENV_PYTHON, NOTIFIER_SCRIPT], start_new_session=True)
    time.sleep(1)
    
    # 2. Launch Universe Monitor
    subprocess.Popen([VENV_PYTHON, MONITOR_SCRIPT], start_new_session=True)
    time.sleep(1)
    
    # 3. Launch Master Editor
    subprocess.Popen([VENV_PYTHON, EDITOR_SCRIPT], start_new_session=True)
    
    # 4. Push Level 002 Notifications
    time.sleep(2)
    push_msgs = [
        ["NEXUS MASTER EDITOR", "Central Command Hub integrated.", "SUCCESS"],
        ["ARCHITECTURE MAP", "D3.js radial tree generated for tech stack audit.", "INFO"],
        ["NOTIFICATION STACK", "Persistent HUD now tracking AI decision loops.", "TOOL"],
        ["LEVEL 002 START", "Transitioning to Mission Pod Implementation.", "WARNING"]
    ]
    
    from push_notif import push_notification
    for m in push_msgs:
        push_notification(m[0], m[1], m[2])
        time.sleep(1)

if __name__ == "__main__":
    launch_all()
