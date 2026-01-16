import time
import os
import subprocess
import datetime

# Configuration
SAVE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "artifacts", "neo_recording")

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def capture_loop():
    print(f"🎥 Neo Recorder Active. Saving framest to: {SAVE_DIR}")
    ensure_dir(SAVE_DIR)
    
    frame_count = 0
    
    try:
        while True:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"neo_frame_{timestamp}_{frame_count:04d}.png"
            filepath = os.path.join(SAVE_DIR, filename)
            
            # MacOS Screen Capture (silent, main monitor)
            cmd = ["screencapture", "-x", "-m", filepath]
            subprocess.run(cmd)
            
            print(f"📸 Captured Frame {frame_count}: {filename}")
            
            frame_count += 1
            time.sleep(10)
            
    except KeyboardInterrupt:
        print("\n🛑 Recording Stopped.")

if __name__ == "__main__":
    capture_loop()
