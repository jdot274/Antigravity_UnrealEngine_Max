import os
from datetime import datetime

def archive_chat(chat_content, session_id="001"):
    log_dir = "/Users/joeywalter/antigravity-nexus/saves/chat_logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
        
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"CHAT_LOG_{session_id}_{timestamp}.md"
    filepath = os.path.join(log_dir, filename)
    
    with open(filepath, "w") as f:
        f.write(f"# 🗨️ ANTIGRAVITY CHOT LOG: SESSION {session_id}\n")
        f.write(f"**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(chat_content)
        
    print(f"✅ Chat archived: {filepath}")
    return filepath

if __name__ == "__main__":
    # Example placeholder for logic
    pass
