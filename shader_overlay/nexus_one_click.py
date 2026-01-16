import subprocess
import os
import sys

# Paths
UNREAL_PATH = "/Users/Shared/Epic Games/UE_5.7/Engine/Binaries/Mac/UnrealEditor.app/Contents/MacOS/UnrealEditor"
UPROJECT_PATH = "/Users/joeywalter/antigravity-nexus/AntigravityTwin.uproject"
NOTIF_SCRIPT = "/Users/joeywalter/antigravity-nexus/shader_overlay/push_notif.py"

def launch_twin():
    print(f"🚀 Triggering One-Click Unreal Startup...")
    
    if not os.path.exists(UNREAL_PATH):
        error_msg = f"Unreal Editor not found at: {UNREAL_PATH}"
        print(error_msg)
        subprocess.run(["python3", NOTIF_SCRIPT, "Launch Error", error_msg, "CRITICAL"])
        return

    # Notify external HUD
    subprocess.run(["python3", NOTIF_SCRIPT, "Twin Sync", "Launching Unreal Twin Project...", "WARNING"])
    
    # Launch Unreal as a detached process
    # We use -skipcompile for speed if needed, but standard launch is safer
    cmd = [UNREAL_PATH, UPROJECT_PATH]
    
    try:
        subprocess.Popen(cmd, start_new_session=True)
        print("✅ Unreal Engine process initiated.")
    except Exception as e:
        print(f"❌ Failed to launch: {str(e)}")

if __name__ == "__main__":
    launch_twin()
