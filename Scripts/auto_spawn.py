import unreal

def auto_boot():
    print("🚀 [AutoSpawn] Initializing Antigravity Nexus...")
    # Trigger the C++ Bridge to spawn the Golf Course + AI Console
    result = unreal.NexusBridge.execute_runtime_cpp("SPAWN_GAME", "AutoBoot")
    print(f"✅ [AutoSpawn] Result: {result}")

if __name__ == "__main__":
    auto_boot()
