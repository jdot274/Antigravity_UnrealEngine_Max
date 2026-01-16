import unreal
import subprocess
import os
import sys

# Antigravity-Max: THE MASTER CONTAINER HOST
# This script runs inside Unreal and ensures all external 'Organs' are alive.

def launch_nexus_bridge():
    """
    Launches the MCP Bridge and UI Host from within Unreal.
    This effectively uses Unreal as the parent process (the container).
    """
    unreal.log("🛡️ Antigravity: Engine Container initializing orchestrator...")
    
    # Path to our dev hub
    nexus_dir = "/Users/joeywalter/antigravity-nexus"
    main_script = os.path.join(nexus_dir, "shader_overlay/main.py")
    
    if os.path.exists(main_script):
        # We launch the Python backend as a detached subprocess
        # This keeps the 'Bridge' alive as long as the engine is open.
        subprocess.Popen([sys.executable, main_script], cwd=nexus_dir)
        unreal.log("✅ Antigravity: Nexus Bridge detached and linked.")
    else:
        unreal.log_error(f"❌ Antigravity: Orchestrator not found at {main_script}")

def init_container():
    launch_nexus_bridge()
    # Run the live link server we built earlier
    import Antigravity_Nexus.unreal_ai_link as ai_link
    ai_link.start_nexus_link()

if __name__ == "__main__":
    init_container()
