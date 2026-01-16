import json
import os
import time
import sys
import subprocess

# Define the manifest path
MANIFEST_PATH = os.path.join(os.path.dirname(__file__), "nexus_manifest.json")

def load_manifest():
    """Reads the Project DNA (JSON)"""
    if not os.path.exists(MANIFEST_PATH):
        print(f"❌ Manifest not found at {MANIFEST_PATH}")
        return None
    
    with open(MANIFEST_PATH, 'r') as f:
        data = json.load(f)
    print(f"✅ Loaded Manifest: {data['project_name']} v{data['version']}")
    return data

def execute_build(manifest):
    """
    Parses the JSON and executes the 'Build' or 'Setup' logic.
    This replaces hardcoded logic with data-driven logic.
    """
    print("🔧 ANTIGRAVITY BUILD PROTOCOL INITIATED")
    
    root_path = os.path.dirname(os.path.abspath(__file__))
    
    # 1. Validate Modules
    print("\n--- Phase 1: Module Validation ---")
    active_modules = []
    for mod in manifest['modules']:
        status = "🟢 ON" if mod['enabled'] else "🔴 OFF"
        print(f"{status} [{mod['id']}] {mod['name']}")
        
        if mod['enabled']:
            # Verify script exists
            script_path = os.path.join(root_path, manifest['paths']['scripts'], mod['script_entry'])
            if os.path.exists(script_path):
                active_modules.append(mod)
            else:
                print(f"   ⚠️ Warning: Script not found at {script_path}")

    # 2. Simulate Build/Launch Sequence
    print("\n--- Phase 2: Execution Sequence ---")
    for step in manifest['launch_sequence']:
        if 'module_id' in step:
            # Find the module
            mod = next((m for m in active_modules if m['id'] == step['module_id']), None)
            if mod:
                print(f"🚀 Launching Module: {mod['name']}...")
                
                # Construct the command
                script_path = os.path.join(root_path, manifest['paths']['scripts'], mod['script_entry'])
                venv_python = os.path.join(root_path, "shader_overlay/venv/bin/python3")
                
                # Verify Venv exists, fallback to sys.executable if not
                cmd_executable = venv_python if os.path.exists(venv_python) else sys.executable
                
                cmd = [cmd_executable, script_path]
                
                try:
                    # Launch as a separate process (start_new_session=True works on Unix to detach)
                    # We use Popen so we don't block
                    subprocess.Popen(cmd, start_new_session=True)
                    print(f"   PID Spawning... OK")
                except Exception as e:
                    print(f"   ❌ FAILED to launch: {e}")
            else:
                print(f"   (Skipping disabled/missing module {step['module_id']})")
                
        elif 'action' in step and step['action'] == 'notify':
            print(f"🔔 NOTIFICATION: {step['message']}")
            # Optional: Hook into push_notif if available
            try:
                sys.path.append(os.path.join(root_path, "shader_overlay"))
                from push_notif import push_notification
                push_notification("NEXUS BUILDER", step['message'], "INFO")
            except ImportError:
                pass
            
        if 'wait_time_ms' in step:
            time.sleep(step['wait_time_ms'] / 1000.0)
            
    print("\n🎉 Build & Setup Complete from JSON Definition.")

if __name__ == "__main__":
    data = load_manifest()
    if data:
        execute_build(data)
