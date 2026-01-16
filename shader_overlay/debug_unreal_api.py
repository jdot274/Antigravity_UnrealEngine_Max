import unreal
import os

def debug_api():
    print("--- Debugging Unreal Python API ---")
    
    actor = unreal.Actor()
    print(f"Actor methods: {[m for m in dir(actor) if 'component' in m]}")
    
    comp = unreal.InstancedStaticMeshComponent()
    print(f"Component methods: {[m for m in dir(comp) if 'register' in m]}")

if __name__ == "__main__":
    debug_api()
