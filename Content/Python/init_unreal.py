import unreal
import sys
import os

unreal.log(f"🐍 Python Version: {sys.version}")
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
# --- NEXUS BOOTLOADER ---
def setup_python_paths():
    """
    Adds Nexus Python directories to sys.path so modules can be imported.
    """
    content_dir = unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_content_dir())
    nexus_root = os.path.join(content_dir, "Nexus", "Python")
    
    paths_to_add = [
        nexus_root,
        os.path.join(nexus_root, "Core"),
        os.path.join(nexus_root, "AI"),
        os.path.join(nexus_root, "Tools"),
        # Legacy Support
        os.path.join(content_dir, "Python", "utils") 
    ]
    
    for p in paths_to_add:
        if p not in sys.path:
            sys.path.append(p)
            unreal.log(f"🐍 NexusPath: Added {p}")

setup_python_paths()

# --- MODULE LOADING ---
def safe_import(module_name, func_name=None):
    try:
        mod = __import__(module_name)
        if func_name:
            if hasattr(mod, func_name):
                getattr(mod, func_name)()
            else:
                unreal.log_warning(f"⚠️ {module_name} has no function '{func_name}'")
        unreal.log(f"✅ Loaded: {module_name}")
        return mod
    except Exception as e:
        unreal.log_error(f"❌ Failed to load {module_name}: {e}")
        return None

# 1. Logger (Critical)
safe_import("nexus_logger", "init_logging")

# 2. Nexus Tools (Menu)
# safe_import("nexus_tools")

# 3. Input System (Uses EditorAssetLibrary?)
# safe_import("nexus_input_setup", "setup_enhanced_input")

# 4. Gemini Brain (Uses Editor Actors?)
# safe_import("nexus_brain_core")

# 5. Game Manager (Full Game Loop)
# Now uses C++ Runtime Bridge - safe for -game mode
safe_import("nexus_game_manager", "start_new_game")

# 6. AAA Content Generator (Permanent Storage Directive)
# Ensures the Spiral Gallery level is generated/loaded
safe_import("utils.aaa_generator", "run_script")

unreal.log("🚀 Nexus Python Environment Initialized.")
