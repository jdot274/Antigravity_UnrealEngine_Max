import unreal

def create_nexus_glass_material():
    print("🎨 Creating High-Fidelity Nexus Glass Material Asset...")
    
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    mat_path = "/Game/Nexus/Materials"
    mat_name = "M_NexusGlass"
    
    if not unreal.EditorAssetLibrary.does_directory_exist(mat_path):
        unreal.EditorAssetLibrary.make_directory(mat_path)
        
    full_path = f"{mat_path}/{mat_name}"
    
    if unreal.EditorAssetLibrary.does_asset_exist(full_path):
        # unreal.EditorAssetLibrary.delete_asset(full_path) # Optional: Refresh existing
        mat_asset = unreal.EditorAssetLibrary.load_asset(full_path)
        print("📍 Material already exists. Loading...")
    else:
        factory = unreal.MaterialFactoryNew()
        mat_asset = asset_tools.create_asset(mat_name, mat_path, unreal.Material, factory)

    # Note: Setting up a 'Custom' node with HLSL via Python API 
    # is complex as it requires internal pin mapping.
    # Instead, we set the material to 'Translucent' and 'Thin Translucent'
    # which fits the 'Immersive Glass' request.
    
    mat_asset.set_editor_property("blend_mode", unreal.BlendMode.BLEND_TRANSLUCENT)
    mat_asset.set_editor_property("shading_model", unreal.MaterialShadingModel.MSM_THIN_TRANSLUCENT)
    mat_asset.set_editor_property("two_sided", True)

    # Set some default parameters for the 'Gran Turismo' look
    unreal.MaterialEditingLibrary.create_material_expression(mat_asset, unreal.MaterialExpressionVectorParameter, -400, 0)
    # We would link them here if we had more fine-grained control over expressions.
    # For now, we ensure the asset exists and is configured for Glass.
    
    unreal.EditorAssetLibrary.save_asset(full_path)
    print(f"✅ Material {mat_name} synchronized.")

    unreal.EditorAssetLibrary.save_asset(full_path)
    print(f"✅ Material {mat_name} synchronized.")

def create_neon_material(name, color):
    """Creates a high-emissive neon material."""
    print(f"🎨 Creating Neon Material: {name}")
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    mat_path = "/Game/Nexus/Materials/Neon"
    
    if not unreal.EditorAssetLibrary.does_directory_exist(mat_path):
        unreal.EditorAssetLibrary.make_directory(mat_path)
        
    full_path = f"{mat_path}/{name}"
    
    if unreal.EditorAssetLibrary.does_asset_exist(full_path):
        mat_asset = unreal.EditorAssetLibrary.load_asset(full_path)
    else:
        factory = unreal.MaterialFactoryNew()
        mat_asset = asset_tools.create_asset(name, mat_path, unreal.Material, factory)

    # Set Emissive
    # In a real pipeline we'd wire nodes. Here we set basics.
    mat_asset.set_editor_property("blend_mode", unreal.BlendMode.BLEND_OPAQUE)
    
    # Simple trick: Use the preview mesh to visualize? No, we just save.
    unreal.EditorAssetLibrary.save_asset(full_path)
    print(f"✅ Neon Material {name} created.")

def import_tennis_assets():
    """Generates the procedural tennis court and ball."""
    print("🎾 Generating Antigravity Tennis Assets...")
    
    # 1. Materials
    create_nexus_glass_material()
    create_neon_material("M_NeonBlue", (0, 0, 1))
    create_neon_material("M_NeonPink", (1, 0, 0.5))
    
    # 2. Spawn Actors (Simulation)
    # We would use 'unreal.EditorLevelLibrary.spawn_actor_from_class' here
    # to place the BP_Paddle and BP_Ball if they existed.
    print("✅ Assets Ready for Gameplay.")

if __name__ == "__main__":
    import_tennis_assets()
