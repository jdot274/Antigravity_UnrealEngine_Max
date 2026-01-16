import unreal
import time
import random
import os
import json

# Connection to the Nexus Bridge
BRIDGE_PATH = "/Users/joeywalter/antigravity-nexus/shader_overlay/universe_state.json"

def update_manifest_status(progress, status):
    try:
        if os.path.exists(BRIDGE_PATH):
            with open(BRIDGE_PATH, 'r') as f:
                state = json.load(f)
            
            state["manifestation"] = {
                "progress": progress,
                "status": status,
                "active_mission": "Phys_Neural_Core"
            }
            
            with open(BRIDGE_PATH, 'w') as f:
                json.dump(state, f, indent=4)
    except: pass

def build_physics_live():
    print("🧠 Starting REAL-TIME Neural Physics Manifestation...")
    update_manifest_status(0, "Initiating Core...")
    
    # 1. Clear previous
    existing = unreal.EditorLevelLibrary.get_all_level_actors()
    for a in existing:
        if a.get_actor_label().startswith("Phys_"):
            unreal.EditorLevelLibrary.destroy_actor(a)
    
    # 2. Manifest Core Gravity Well
    core_location = unreal.Vector(0, 0, 500)
    core_actor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.StaticMeshActor, core_location)
    core_actor.set_actor_label("Phys_GravityWell")
    
    SphereMesh = unreal.EditorAssetLibrary.load_asset("/Engine/BasicShapes/Sphere.Sphere")
    core_actor.static_mesh_component.set_static_mesh(SphereMesh)
    core_actor.set_actor_scale3d(unreal.Vector(2.0, 2.0, 2.0))
    
    # Apply glowing material (assumed already created or use basic)
    base_mat = unreal.EditorAssetLibrary.load_asset("/Engine/BasicShapes/BasicShapeMaterial.BasicShapeMaterial")
    core_actor.static_mesh_component.set_material(0, base_mat)
    
    update_manifest_status(20, "Core Stabilized. Spawning Nodes...")

    # 3. Procedural Delayed Spawning
    CubeMesh = unreal.EditorAssetLibrary.load_asset("/Engine/BasicShapes/Cube.Cube")
    
    node_count = 60
    for i in range(node_count):
        # We need to yield or use a timer if this was a long-running tick, 
        # but for an editor script we can just loop and log.
        # In actual UE Python, 'time.sleep' blocks the main thread, 
        # but for small counts it creates a visible "batch" spawning.
        
        angle = random.uniform(0, 3.14159 * 2)
        radius = random.uniform(400, 1200)
        loc = unreal.Vector(
            core_location.x + radius * unreal.MathLibrary.cos(angle),
            core_location.y + radius * unreal.MathLibrary.sin(angle),
            core_location.z + random.uniform(-200, 800)
        )
        
        cube = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.StaticMeshActor, loc)
        cube.set_actor_label(f"Phys_Node_{i}")
        cube.static_mesh_component.set_static_mesh(CubeMesh)
        cube.set_actor_scale3d(unreal.Vector(0.2, 0.2, 0.2))
        
        # Physics setup
        smc = cube.static_mesh_component
        smc.set_simulate_physics(True)
        smc.set_enable_gravity(False)
        
        # Small delay to visual "pop"
        if i % 5 == 0:
            progress = 20 + int((i / node_count) * 80)
            update_manifest_status(progress, f"Manifesting Node {i}...")
            # Note: unreal.EditorLevelLibrary.editor_set_game_view(True) # Optional window focus
        
    # 4. Final Pulse
    update_manifest_status(100, "Manifestation Complete. Neural Sync Active.")
    print("✅ Real-time manifestation successful.")

if __name__ == "__main__":
    build_physics_live()
