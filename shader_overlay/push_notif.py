import json
import os

QUEUE_FILE = "/Users/joeywalter/antigravity-nexus/shader_overlay/notifier_queue.json"

def push_notification(title, message, type="INFO"):
    notifications = []
    if os.path.exists(QUEUE_FILE):
        try:
            with open(QUEUE_FILE, "r") as f:
                notifications = json.load(f)
        except Exception:
            notifications = []
            
    notifications.append({
        "title": title,
        "message": message,
        "type": type
    })
    
    with open(QUEUE_FILE, "w") as f:
        json.dump(notifications, f)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2:
        push_notification(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "INFO")
