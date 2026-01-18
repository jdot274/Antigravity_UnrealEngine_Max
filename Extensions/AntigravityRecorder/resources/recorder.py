import time
import subprocess
import os
import datetime
import sys

def record_screen(duration_minutes=5):
    # Create the recordings directory if it doesn't exist
    home_dir = os.path.expanduser("~")
    save_dir = os.path.join(home_dir, "antigravity-nexus", "Recordings")
    os.makedirs(save_dir, exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"recording_{timestamp}.mp4"
    filepath = os.path.join(save_dir, filename)

    print(f"Starting recording: {filepath} for {duration_minutes} minutes")

    # FFmpeg command for macOS (avfoundation)
    # We capture the default screen (index 0 usually). 
    # Adjust "-i 0" if multiple screens are present and a specific one is targetted.
    # Framerate 30 to keep size reasonable.
    cmd = [
        "ffmpeg",
        "-f", "avfoundation",
        "-i", "1", # Capture screen 1 (often the main display on macs if 0 is webcam, verify this!)
        "-r", "30",
        "-t", str(duration_minutes * 60), # Duration in seconds
        "-y", # Overwrite if exists
        filepath
    ]

    try:
        # Run ffmpeg. This is a blocking call if we just run it, 
        # but the extension spawns this script in a detached process, 
        # so this script IS the background worker.
        subprocess.run(cmd, check=True)
        print(f"Recording saved to {filepath}")
    except subprocess.CalledProcessError as e:
        print(f"Error recording: {e}")
    except FileNotFoundError:
        print("FFmpeg not found. Please ensure ffmpeg is installed and in your PATH.")

if __name__ == "__main__":
    # Default to 5 minutes
    try:
        record_screen(5)
    except KeyboardInterrupt:
        print("Recording stopped by user.")
