import unreal
import sys
import os

# Add local path to sys
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)
    
# ----------------------------------------------------------------------------------
# SYSTEM PATH CONFIGURATION - ROBUST ENV BRIDGING
# ----------------------------------------------------------------------------------
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
NEXUS_ENV_SITE = os.path.join(ROOT_DIR, ".nexus_env", "lib", "python3.14", "site-packages")

# If we are on a different python version, try to wildcard find it
if not os.path.exists(NEXUS_ENV_SITE):
    import glob
    possible_paths = glob.glob(os.path.join(ROOT_DIR, ".nexus_env", "lib", "python*", "site-packages"))
    if possible_paths:
        NEXUS_ENV_SITE = possible_paths[0]

if os.path.exists(NEXUS_ENV_SITE):
    if NEXUS_ENV_SITE not in sys.path:
        sys.path.append(NEXUS_ENV_SITE)
        unreal.log(f"✅ NexusBridge: Injected Virtual Env: {NEXUS_ENV_SITE}")
else:
    unreal.log_warning(f"⚠️ NexusBridge: Could not find .nexus_env at {NEXUS_ENV_SITE}")

# Continue with internal paths
sys.path.append(os.path.join(os.path.dirname(__file__), "Nexus/Python/Core"))
sys.path.append(os.path.join(os.path.dirname(__file__), "Nexus/Python/Tools"))
sys.path.append(os.path.join(os.path.dirname(__file__), "Nexus/Python/AI"))

# Import our utilities
try:
    import nexus_tools
    nexus_tools.run_setup()
    unreal.log("🚀 Antigravity Nexus Python Stack Loaded (Tools + CLI).")
    
    # Auto-Run User Request: Open Content Folder
    unreal.log("📂 Auto-Executing: fe content")
    nexus_tools.cli("fe content")
    
except Exception as e:
    unreal.log_error(f"❌ Failed to load Nexus Python Stack: {e}")

import nexus_tools; nexus_tools.build_slate_level()
import nexus_tools; nexus_tools.cli("gemini Testing Gemini integration with Nexus Tools")
import nexus_tools.mat_lidar_gen; nexus_tools.mat_lidar_gen.create_lidar_material()
