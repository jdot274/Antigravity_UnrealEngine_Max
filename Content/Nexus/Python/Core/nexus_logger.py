import unreal
import os
import datetime

LOG_FILE = os.path.join(unreal.Paths.project_dir(), "NexusGlobal.log")

def log(message, level="INFO"):
    """
    Persistent Logger. Writes to disk immediately.
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] [{level}] {message}"
    
    # 1. Write to Disk
    with open(LOG_FILE, "a") as f:
        f.write(entry + "\n")
        
    # 2. Write to Unreal Output Log (Console)
    if level == "ERROR":
        unreal.log_error(message)
    elif level == "WARNING":
        unreal.log_warning(message)
    else:
        unreal.log(message)

def init_logging():
    log("--------------------------------------------------")
    log("Nexus Persistent Logger Initialized.")
    log(f"Session Start. Log Path: {LOG_FILE}")
    log("--------------------------------------------------")

if __name__ == "__main__":
    init_logging()
