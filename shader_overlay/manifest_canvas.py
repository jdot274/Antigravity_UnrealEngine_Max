import unreal

def manifest_empty_canvas():
    """
    Sets up the 'Infinite White Room' for the Antigravity Dev Mode.
    Everything starts here.
    """
    unreal.log("🛡️ Antigravity: Manifesting Empty Canvas...")
    
    # Create or load a basic 'Void' level
    # In a real setup, we'd use unreal.AssetToolsHelpers.get_asset_tools().create_asset(...)
    # For now, we clear the active level
    unreal.EditorLevelLibrary.new_level("/Game/Antigravity/Maps/DevMode_Canvas")
    
    # Add a massive grid floor
    plane_class = unreal.load_class(None, "/Engine/BasicShapes/Plane.Plane")
    location = unreal.Vector(0, 0, 0)
    rotation = unreal.Rotator(0, 0, 0)
    
    floor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.StaticMeshActor, location, rotation)
    floor.set_actor_label("DEV_GRID_FLOOR")
    floor.set_actor_scale3d(unreal.Vector(100, 100, 1))
    
    # Try to apply a grid material
    grid_mat = unreal.load_asset("/Engine/EngineMaterials/M_Grid.M_Grid")
    if grid_mat:
        floor.static_mesh_component.set_material(0, grid_mat)
        
    # Add a Sky Atmosphere and Directional Light for visibility
    unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.SkyAtmosphere, location, rotation)
    sun = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.DirectionalLight, unreal.Vector(0, 0, 500), unreal.Rotator(-45, 0, 0))
    sun.set_actor_label("DEV_SUN")

    unreal.log("✅ CANVAS MANIFESTED. WELCOME TO DEV MODE.")

if __name__ == "__main__":
    manifest_empty_canvas()
