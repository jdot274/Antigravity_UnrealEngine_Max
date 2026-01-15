import subprocess
import os
import sys

# Paths
ENGINE_PATH = "/Users/Shared/Epic Games/UE_5.7"
UAT_PATH = os.path.join(ENGINE_PATH, "Engine/Build/BatchFiles/RunUAT.sh")
PROJECT_PATH = "/Users/joeywalter/Documents/Unreal Projects/MyProject/MyProject.uproject"
ARCHIVE_PATH = "/Users/joeywalter/antigravity-nexus/native_builds"

def package_project():
    print(f"🚀 Starting AAA Native Packaging for macOS (Metal 3)...")
    
    if not os.path.exists(ARCHIVE_PATH):
        os.makedirs(ARCHIVE_PATH)

    # BuildCookRun command
    # -platform=Mac
    # -clientconfig=Development (Includes some debug/perf tools)
    # -cook, -build, -stage, -pak (Standard packaging flags)
    cmd = [
        UAT_PATH,
        "BuildCookRun",
        f"-project={PROJECT_PATH}",
        "-platform=Mac",
        "-clientconfig=Development",
        "-archivedirectory=" + ARCHIVE_PATH,
        "-cook",
        "-allmaps",
        "-build",
        "-stage",
        "-pak",
        "-archive"
    ]

    try:
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        for line in process.stdout:
            print(line, end='')
        
        process.wait()
        if process.returncode == 0:
            print(f"\n✅ SUCCESS: Native Mac App created at {ARCHIVE_PATH}/Mac")
        else:
            print(f"\n❌ FAILED: Check the logs above.")
            
    except Exception as e:
        print(f"Error executing packaging: {e}")

if __name__ == "__main__":
    package_project()
