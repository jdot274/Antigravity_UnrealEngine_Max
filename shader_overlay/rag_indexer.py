import json
import time
import os

UNIVERSE_PATH = "/Users/joeywalter/antigravity-nexus/shader_overlay/universe_state.json"

def update_node_status(node_name, new_status):
    if not os.path.exists(UNIVERSE_PATH):
        return
        
    with open(UNIVERSE_PATH, "r") as f:
        data = json.load(f)
        
    found = False
    for node in data["nodes"]:
        if node["name"] == node_name:
            node["status"] = new_status
            found = True
            break
            
    if not found:
        data["nodes"].append({"name": node_name, "status": new_status})
        
    with open(UNIVERSE_PATH, "w") as f:
        json.dump(data, f, indent=4)
    print(f"Updated {node_name} to {new_status}")

def simulate_rag_flow():
    # 1. Start Vectorizing UE Docs
    update_node_status("UE 5.7 Documentation", "RESEARCH")
    time.sleep(2)
    
    # 2. Index Context 7
    update_node_status("Context 7 Protocol", "RESEARCH")
    time.sleep(2)
    
    # 3. Propose the Integration
    update_node_status("UE 5.7 Documentation", "PROPOSED")
    update_node_status("Context 7 Protocol", "PROPOSED")
    print("RAG Indexer: Intelligence Proposed. Waiting for brain sync...")

if __name__ == "__main__":
    simulate_rag_flow()
