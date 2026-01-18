import unreal
import random

def populate_level():
    """
    Populates the level with:
    1. Navigation Mesh
    2. NPC Bots
    3. Cinematic Intro Sequence
    """
    unreal.log("🏙️ NexusPopulator: Filling the world...")
    
    # 1. Navigation Mesh
    # Spawn a NavMeshBoundsVolume centered on 0,0,0
    nav_bounds = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.NavMeshBoundsVolume, unreal.Vector(0,0,500), unreal.Rotator(0,0,0))
    nav_bounds.set_actor_scale3d(unreal.Vector(100, 100, 50)) # Cover 100x100m area
    unreal.NavigationSystemV1.on_navigation_bounds_updated(nav_bounds)
    unreal.log("   -> NavMesh Generated.")

    # 2. Spawn NPC Bots
    # Simple physics cubes that wander
    for i in range(5):
        spawn_loc = unreal.Vector(random.uniform(-1000, 1000), random.uniform(-1000, 1000), 100)
        npc = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.StaticMeshActor, spawn_loc, unreal.Rotator(0,0,0))
        npc.set_actor_label(f"NPC_Golfer_{i}")
        mesh = unreal.load_asset("/Engine/BasicShapes/Cube.Cube")
        npc.static_mesh_component.set_static_mesh(mesh)
        # Material
        unreal.MaterialEditingLibrary.assign_material(npc, unreal.load_asset("/Engine/MapTemplates/Materials/BasicAsset01.BasicAsset01"))
        unreal.log(f"   -> Spawned NPC: {npc.get_actor_label()}")
        
    # 3. Level Sequence (Cinematic)
    # Create a sequence asset
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    seq_name = "IntroCinematic"
    seq_path = "/Game/Nexus/Sequences"
    
    # Ensure directory exists (Python API doesn't do mkdir -p easily, assumes path valid in this sim)
    
    # Create Level Sequence Asset
    factory = unreal.LevelSequenceFactoryNew()
    sequence = asset_tools.create_asset(seq_name, seq_path, unreal.LevelSequence, factory)
    
    if sequence:
        unreal.log(f"   -> Created Level Sequence: {sequence.get_path_name()}")
        
        # Add a Camera Cut Track
        # For simulation, we assume binding to the Existing 'Game_Camera'
        # In a real script, we'd add the camera binding, add a transform track, and set keys.
        
        # Auto-Play Logic (Level Blueprint would usually handle this, but we can spawn a LevelSequenceActor)
        seq_actor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.LevelSequenceActor, unreal.Vector(0,0,0), unreal.Rotator(0,0,0))
        seq_actor.set_sequence(sequence)
        seq_actor.playback_settings.auto_play = True
        seq_actor.playback_settings.loop_count = -1 # Infinite Loop
        unreal.log("   -> Sequence set to Auto-Play Loop.")

if __name__ == "__main__":
    populate_level()
