import json
import os

UNIVERSE_PATH = "/Users/joeywalter/antigravity-nexus/shader_overlay/universe_state.json"

def update_monitor():
    if not os.path.exists(UNIVERSE_PATH):
        return
        
    with open(UNIVERSE_PATH, "r") as f:
        data = json.load(f)
        
    # Injecting the IDE Extension node
    target_node = "UE C++ Snippets Extension"
    for node in data["nodes"]:
        if node["name"] == target_node:
            node["status"] = "PROPOSED"
            break
            
    with open(UNIVERSE_PATH, "w") as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    update_monitor()
