import json
import os

def register_accepted_intelligence():
    # Update the Universe Monitor
    universe_path = "/Users/joeywalter/antigravity-nexus/shader_overlay/universe_state.json"
    if not os.path.exists(universe_path):
        return

    with open(universe_path, "r") as f:
        data = json.load(f)
        
    # Update Statuses to ACCEPTED (Green)
    for node in data["nodes"]:
        if "Documentation" in node["name"] or "Context 7" in node["name"] or "Snippet" in node["name"]:
            node["status"] = "ACCEPTED"
            
    # Add a NOTE/FAILED node (Red)
    failed_node = {
        "name": "Legacy Hot-Reload Method",
        "status": "FAILED",
        "notes": "Redundant when using Live Coding and Context 7 injection."
    }
    
    # Add a RESEARCH node (Grey)
    research_node = {
        "name": "Nanite Tessellation API",
        "status": "RESEARCH",
        "notes": "Analyzing memory impact for procedural terrain."
    }
    
    # Ensure they exist in the list
    if not any(n["name"] == failed_node["name"] for n in data["nodes"]):
        data["nodes"].append(failed_node)
    if not any(n["name"] == research_node["name"] for n in data["nodes"]):
        data["nodes"].append(research_node)
            
    with open(universe_path, "w") as f:
        json.dump(data, f, indent=4)
    print("✅ Universe Monitor Status Layer Updated.")

if __name__ == "__main__":
    register_accepted_intelligence()
    
# Unreal logic (only runs when called INSIDE Unreal)
try:
    import unreal
    class UnrealSnippetHelper:
        SUPPORTED_SNIPPETS = {
            "ulog": "UE_LOG(LogTemp, Warning, TEXT(\"{message}\"));",
        }
except ImportError:
    pass
