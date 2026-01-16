import subprocess
import os
import time
import webbrowser
import sys

# Paths
ROOT_DIR = "/Users/joeywalter/antigravity-nexus"
BRIDGE_DIR = os.path.join(ROOT_DIR, "bridge")
SS_SCRIPT = os.path.join(BRIDGE_DIR, "SignallingWebServer/platform_scripts/bash/start.sh")
UNREAL_PATH = "/Users/Shared/Epic Games/UE_5.7/Engine/Binaries/Mac/UnrealEditor.app/Contents/MacOS/UnrealEditor"
UPROJECT_PATH = os.path.join(ROOT_DIR, "AntigravityTwin.uproject")

def launch_stream():
    print("🚀 Initiating ANTIGRAVITY STREAM...")
    
    # 0. Build Infrastructure (Just in case)
    # We assume 'npm install' and 'npm run build' happened or will happen.
    
    # 1. Start Signaling Server
    print("📡 Launching Signaling Server...")
    # launching directly with node might be safer if bash scripts are flaky with paths
    # But start.sh usually handles arguments.
    # Let's try start.sh first.
    
    ss_process = subprocess.Popen(
        ["bash", "start.sh"], 
        cwd=os.path.dirname(SS_SCRIPT),
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE
    )
    
    # Wait for server to be ready?
    time.sleep(3)
    if ss_process.poll() is not None:
        print("❌ Signaling Server failed to start.")
        # Try fallback: npm run start inside SignallingWebServer
        print("🔄 Attempting fallback: npm run start...")
        ss_dir = os.path.join(BRIDGE_DIR, "SignallingWebServer")
        ss_process = subprocess.Popen(
            ["npm", "run", "start"], 
            cwd=ss_dir
        )
        
    print("✅ Signaling Server Active (PID: Unknown, detached)")

    # 2. Launch Unreal Engine
    print("🎮 Launching Unreal Engine (Stream Mode)...")
    
    # Flags for Pixel Streaming
    # -PixelStreamingIP=localhost -PixelStreamingPort=8888 
    # -RenderOffScreen (Optional, keeps window hidden?) No, user might want to see both.
    # -ForceRes? -ResX=1920 -ResY=1080
    
    ue_cmd = [
        UNREAL_PATH,
        UPROJECT_PATH,
        "-PixelStreamingIP=localhost",
        "-PixelStreamingPort=8888",
        "-AudioMixer",
        "-AllowPixelStreamingCommands",
        "-game",
        "-windowed",
        "-ResX=1280",
        "-ResY=720"
    ]
    
    ue_process = subprocess.Popen(ue_cmd, start_new_session=True)
    print("✅ Unreal Engine Stream Initiated.")

    # 3. Open Browser
    print("🌐 Connecting via Chrome...")
    time.sleep(10) # Wait for UE to load and connect
    webbrowser.open("http://localhost:80")

if __name__ == "__main__":
    launch_stream()
