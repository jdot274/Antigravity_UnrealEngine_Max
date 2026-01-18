import os
import subprocess
import sys
import platform

def find_unreal_engine():
    """
    Attempts to locate the Unreal Engine ROOT path.
    """
    # Mac Default Check
    paths = [
        "/Users/Shared/Epic Games/UE_5.7/Engine",
        "/Users/Shared/Epic Games/UE_5.5/Engine",
        "/Users/Shared/Epic Games/UE_5.4/Engine"
    ]
    for p in paths:
        if os.path.exists(p):
            return p
    return None

def compile_nexus_project():
    """
    Automates the C++ Compilation of AntigravityTwin via UBT.
    """
    print("🛠️  Nexus AGI Compiler: Initializing...")
    
    # 1. Locate Engine
    engine_root = find_unreal_engine()
    if not engine_root:
        print("❌ Error: Could not auto-detect Unreal Engine. Please edit nexus_compiler.py.")
        sys.exit(1)
        
    print(f"   -> Engine Found: {engine_root}")
    
    # 2. Identify UBT Script
    sys_plat = platform.system()
    if sys_plat == "Darwin": # Mac
        build_tool = os.path.join(engine_root, "Build", "BatchFiles", "Mac", "Build.sh")
    elif sys_plat == "Windows":
        build_tool = os.path.join(engine_root, "Build", "BatchFiles", "Build.bat")
    else:
        print(f"❌ Error: Unsupported OS: {sys_plat}")
        sys.exit(1)
        
    if not os.path.exists(build_tool):
        print(f"❌ Error: Build Tool not found at {build_tool}")
        sys.exit(1)

    # 3. Construct Command
    project_file = os.path.abspath("AntigravityTwin.uproject")
    target_name = "AntigravityTwinEditor" # Editor target for dev
    config = "Development"
    
    cmd = [
        build_tool,
        target_name,
        "Mac" if sys_plat == "Darwin" else "Win64",
        config,
        f"-Project={project_file}",
        "-WaitMutex",
        "-FromMsBuild",
        "-Verbose" # User requested deep debugging
    ]
    
    print(f"🚀 Executing UBT: {' '.join(cmd)}")
    
    # 4. Execute
    try:
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Stream Output
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(f"   [UBT] {output.strip()}")
                
        rc = process.poll()
        if rc == 0:
            print("✅ C++ Compilation SUCCESS!")
            print("   -> You can now launch the engine.")
        else:
            print(f"❌ C++ Compilation FAILED (Exit Code {rc})")
            stderr_out = process.stderr.read()
            print(f"   [STDERR] {stderr_out}")
            
    except Exception as e:
        print(f"❌ Execution Error: {e}")

if __name__ == "__main__":
    compile_nexus_project()
