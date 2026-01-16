import json
import os
import time
import subprocess

# Paths
BRIDGE_DIR = "/Users/joeywalter/antigravity-nexus/shader_overlay"
QUEUE_FILE = os.path.join(BRIDGE_DIR, "ai_command_queue.json")
RESPONSE_FILE = os.path.join(BRIDGE_DIR, "ai_response_log.json")
UNIVERSE_STATE = os.path.join(BRIDGE_DIR, "universe_state.json")

def send_to_engine(command_type, payload):
    """Pushes a response or code snippet to the Unreal UI."""
    data = {
        "timestamp": time.time(),
        "type": command_type, # 'CHAT' or 'CODE'
        "content": payload
    }
    
    responses = []
    if os.path.exists(RESPONSE_FILE):
        try:
            with open(RESPONSE_FILE, "r") as f:
                responses = json.load(f)
        except: pass
        
    responses.append(data)
    # Keep only last 20
    responses = responses[-20:]
    
    with open(RESPONSE_FILE, "w") as f:
        json.dump(responses, f)
    print(f"📡 AI Response Broadcast: {command_type}")

def poll_from_engine():
    """Reads user prompts from the Unreal EUW."""
    if not os.path.exists(QUEUE_FILE):
        return None
        
    try:
        with open(QUEUE_FILE, "r") as f:
            queue = json.load(f)
            
        if not queue:
            return None
            
        # Process first item
        item = queue.pop(0)
        
        # Save back the remaining
        with open(QUEUE_FILE, "w") as f:
            json.dump(queue, f)
            
        return item
    except Exception as e:
        print(f"Error polling engine: {e}")
        return None

def update_ui_status(status):
    """Updates the shared state to show AI agent activity."""
    try:
        with open(UNIVERSE_STATE, "r") as f:
            state = json.load(f)
            
        found = False
        for node in state.get("nodes", []):
            if node["name"] == "AI Agent Status":
                node["status"] = status
                found = True
                break
        
        if not found:
            state["nodes"].append({
                "name": "AI Agent Status",
                "status": status,
                "notes": "Real-time engine integration active."
            })
            
        with open(UNIVERSE_STATE, "w") as f:
            json.dump(state, f, indent=4)
    except: pass

if __name__ == "__main__":
    print("🤖 Antigravity AI-Engine Bridge Running...")
    update_ui_status("ACTIVE")
    
    while True:
        prompt = poll_from_engine()
        if prompt:
            print(f"📥 Received Prompt from Unreal: {prompt['text']}")
            update_ui_status("RESEARCH")
            
            # Simple Echo for now (The AI assistant will handle the logic in practice)
            # In a real tool workflow, the agent would pick this up
            response = f"Acknowledged from Engine Context: {prompt['text']}"
            send_to_engine("CHAT", response)
            update_ui_status("ACTIVE")
            
        time.sleep(1)
