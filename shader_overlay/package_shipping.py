import subprocess
import os
import sys

# === CONFIRMED PATHS ===
ENGINE_ROOT = "/Users/Shared/Epic Games/UE_5.7"
UAT_SCRIPT = os.path.join(ENGINE_ROOT, "Engine/Build/BatchFiles/RunUAT.sh")
PROJECT_FILE = "/Users/joeywalter/antigravity-nexus/AntigravityTwin.uproject"
BUILD_DIR = "/Users/joeywalter/antigravity-nexus/Builds/Shipping"

def build_shipping_app():
    print("📦 INITIALIZING SHIPPING BUILD PROTOCOL: Antigravity Twin [Mac Metal 3]")
    print(f"   Target: {BUILD_DIR}")
    
    # Ensure build dir exists
    if not os.path.exists(BUILD_DIR):
        os.makedirs(BUILD_DIR)

    # Command arguments for a Shipping Build
    # -utf8output ensures logs are readable
    cmd = [
        "bash", UAT_SCRIPT,
        "BuildCookRun",
        f"-project={PROJECT_FILE}",
        "-noP4",
        "-platform=Mac",
        "-clientconfig=Shipping",
        "-serverconfig=Shipping",
        "-cook",
        "-allmaps",
        "-build",
        "-stage",
        "-pak",
        "-archive",
        f"-archivedirectory={BUILD_DIR}",
        "-utf8output"
    ]
    
    # Print the command for verification
    print(f"   CMD: {' '.join(cmd)}")
    print("   ⏳ This process may take 10-30 minutes depending on shader compilation...")

    try:
        # We run this and stream output so the user can see progress if run in terminal
        # For the agent environment, we might just fire and forget or wait.
        # Since the user challenged us, we'll try to run it.
        process = subprocess.Popen(
            cmd, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT, 
            text=True
        )
        
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip())
                
        rc = process.poll()
        
        if rc == 0:
            print("\n✅ SHIPPING BUILD SUCCESSFUL!")
            print(f"   App located at: {BUILD_DIR}/Mac")
        else:
            print(f"\n❌ BUILD FAILED with exit code {rc}")

    except Exception as e:
        print(f"❌ EXECUTION ERROR: {e}")

if __name__ == "__main__":
    build_shipping_app()
