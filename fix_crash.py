import json
import os

PROJECT_FILE = "AntigravityTwin.uproject"

def disable_heavy_plugins():
    if not os.path.exists(PROJECT_FILE):
        print(f"❌ Error: {PROJECT_FILE} not found in {os.getcwd()}")
        return

    print(f"🔧 Analyzing {PROJECT_FILE} for heavy plugins...")
    
    with open(PROJECT_FILE, 'r') as f:
        data = json.load(f)

    # List of plugins to temporarily disable for stability
    heavy_hitters = ["Water", "Landmass", "PCG", "AnywhereXR", "AndroidFileServer", "GooglePAD"]
    
    changed = False
    
    if "Plugins" in data:
        for plugin in data["Plugins"]:
            if plugin["Name"] in heavy_hitters and plugin.get("Enabled", False):
                print(f"   -> Disabling {plugin['Name']} (Cause of potential hang)")
                plugin["Enabled"] = False
                changed = True
                
    if changed:
        with open(PROJECT_FILE, 'w') as f:
            json.dump(data, f, indent=4)
        print("✅ Project file patched. Try launching now!")
    else:
        print("ℹ️ No active heavy plugins found. Project should be safe.")

if __name__ == "__main__":
    disable_heavy_plugins()
