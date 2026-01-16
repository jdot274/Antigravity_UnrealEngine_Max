import unreal
import math

def build_spatial_interface():
    """
    Constructs the 'Nexus Spatial Command Room'.
    Spawns 3D Executable Icons (Spline Meshes) for each major tool.
    Each icon is tagged with 'NexusCmd:...' for interaction.
    """
    ell = unreal.EditorLevelLibrary
    eal = unreal.EditorAssetLibrary
    at = unreal.AssetToolsHelpers.get_asset_tools()
    
    unreal.log("🕸️ CONSTRUCTING SPATIAL EXECUTABLE INTERFACE...")
    
    # 1. Cleanup Old UI
    actors = ell.get_all_level_actors()
    for a in actors:
        if "SpatialIcon_" in a.get_actor_label() or "SpatialLabel_" in a.get_actor_label():
            ell.destroy_actor(a)
    
    # 2. Define Commands
    commands = [
        {"label": "BUILD LEVEL", "cmd": "nexus_tools._auto_build_level()", "color": (0, 1, 0)},
        {"label": "SCAN TWIN", "cmd": "nexus_tools._auto_scan_object()", "color": (0, 0, 1)},
        {"label": "PREDICT", "cmd": "nexus_tools._auto_predict_track()", "color": (1, 0.5, 0)},
        {"label": "ORACLE", "cmd": "nexus_tools._auto_consult_oracle()", "color": (1, 0, 1)},
        {"label": "ULTRA BRAIN", "cmd": "nexus_tools._auto_gen_solutions()", "color": (0, 1, 1)},
    ]
    
    # 3. Spawn Layout (Circle)
    center = unreal.Vector(0, 0, 400)
    radius = 600.0
    angle_step = 360.0 / len(commands)
    
    mesh = eal.load_asset("/Engine/BasicShapes/Torus") # Simulates a 'Spline Ring'
    if not mesh:
        mesh = eal.load_asset("/Engine/BasicShapes/Cube")
        
    for i, cmd in enumerate(commands):
        angle_rad = math.radians(i * angle_step)
        
        x = center.x + radius * math.cos(angle_rad)
        y = center.y + radius * math.sin(angle_rad)
        z = center.z
        
        # Spawn Icon
        icon = ell.spawn_actor_from_class(unreal.StaticMeshActor, unreal.Vector(x, y, z), unreal.Rotator(90, 0, 0))
        icon.set_actor_label(f"SpatialIcon_{cmd['label'].replace(' ','_')}")
        icon.static_mesh_component.set_static_mesh(mesh)
        icon.set_actor_scale3d(unreal.Vector(2.0, 2.0, 0.2)) # Ring shape
        
        # Tagging for Linking
        # Explicit Type Mapping
        icon.tags = [f"NexusCmd:{cmd['cmd']}", "NexusType:SpatialButton"]
        
        # Spawn Text Label
        text_actor = ell.spawn_actor_from_class(unreal.TextRenderActor, unreal.Vector(x, y, z + 150), unreal.Rotator(0, 180 + (i*angle_step), 0))
        text_actor.set_actor_label(f"SpatialLabel_{cmd['label']}")
        text_actor.text_render.set_text(cmd['label'])
        text_actor.text_render.set_text_render_color(unreal.Color(255, 255, 255, 255))
        text_actor.set_actor_scale3d(unreal.Vector(5, 5, 5))
        
        # Orientation: Look at center
        look_at = unreal.Rotator(0, (i * angle_step) + 180, 0) # Face inward
        icon.set_actor_rotation(unreal.Rotator(90, look_at.yaw, 0), False)
        text_actor.set_actor_rotation(unreal.Rotator(0, look_at.yaw, 0), False)

    unreal.log("✅ SPATIAL UI GENERATED: 5 Executable Spline Icons.")

if __name__ == "__main__":
    build_spatial_interface()
