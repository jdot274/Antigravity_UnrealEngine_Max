import subprocess
import time
import os
import sys

# All Antigravity Core Components
SCRIPTS = [
    "quantum_hud.py",
    "nexus_game_engine.py",
    "universe_monitor.py",
    "nexus_editor.py",
    "ai_engine_bridge.py",
    "manifest_sim.py"
]

VENV_PYTHON = "/Users/joeywalter/antigravity-nexus/shader_overlay/venv/bin/python3"
BASE_DIR = "/Users/joeywalter/antigravity-nexus/shader_overlay"

def main():
    print("🛸 SHADOW REVEAL: Manifesting the complete Nexus Stack...")
    processes = {}

    # Initial mass launch
    for script in SCRIPTS:
        print(f"📡 BOOTING: {script}...")
        path = os.path.join(BASE_DIR, script)
        processes[script] = subprocess.Popen([VENV_PYTHON, path], start_new_session=True)
        time.sleep(0.5) # Staggered entry

    print("🛡️ Eternal Guard active. Monitoring all rendering layers.")
    
    while True:
        for script in SCRIPTS:
            if script not in processes or processes[script].poll() is not None:
                print(f"♻️ PERSISTENCE TRIGGER: Relaunching {script}...")
                path = os.path.join(BASE_DIR, script)
                processes[script] = subprocess.Popen([VENV_PYTHON, path], start_new_session=True)
        
        time.sleep(3)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Guard shutting down...")
