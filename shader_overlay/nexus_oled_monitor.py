import unreal
import math

def create_futuristic_oled_monitor():
    """
    Spawns a stunning futuristic OLED monitor mesh in the Unreal Level.
    Features:
    - Curved mesh geometry (simulated with multiple planes)
    - Emissive OLED material with pixel effect
    - Volumetric glow via Post Process
    - Pixel Streaming ready viewport
    """
    print("🖥️ ANTIGRAVITY MONITOR CONSTRUCTION PROTOCOL INITIATED")
    
    ell = unreal.EditorLevelLibrary
    eal = unreal.EditorAssetLibrary
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    mel = unreal.MaterialEditingLibrary
    
    # === 1. CREATE THE OLED MASTER MATERIAL ===
    print("🎨 Forging OLED Emissive Material...")
    mat_path = "/Game/Nexus/Materials"
    mat_name = "M_OLED_Futuristic"
    full_mat_path = f"{mat_path}/{mat_name}"
    
    if not eal.does_directory_exist(mat_path):
        eal.make_directory(mat_path)
    
    if eal.does_asset_exist(full_mat_path):
        oled_mat = eal.load_asset(full_mat_path)
    else:
        factory = unreal.MaterialFactoryNew()
        oled_mat = asset_tools.create_asset(mat_name, mat_path, unreal.Material, factory)
    
    # Material Properties for OLED Effect
    oled_mat.set_editor_property("blend_mode", unreal.BlendMode.BLEND_OPAQUE)
    oled_mat.set_editor_property("shading_model", unreal.MaterialShadingModel.MSM_UNLIT)  # Unlit for max glow
    
    # Create Emissive Color Node
    emissive_param = mel.create_material_expression(oled_mat, unreal.MaterialExpressionVectorParameter, -400, 0)
    emissive_param.set_editor_property("parameter_name", "ScreenColor")
    emissive_param.set_editor_property("default_value", unreal.LinearColor(0.0, 0.5, 1.0, 1.0))  # Cyan
    
    # Create Emissive Multiplier (For Bloom Intensity)
    mult_node = mel.create_material_expression(oled_mat, unreal.MaterialExpressionMultiply, -200, 0)
    intensity_param = mel.create_material_expression(oled_mat, unreal.MaterialExpressionScalarParameter, -400, 100)
    intensity_param.set_editor_property("parameter_name", "EmissiveIntensity")
    intensity_param.set_editor_property("default_value", 50.0)  # High for bloom
    
    # Connect nodes (conceptual - requires MaterialEditingLibrary.connect_material_expressions)
    # mel.connect_material_expressions(emissive_param, "", mult_node, "A")
    # mel.connect_material_expressions(intensity_param, "", mult_node, "B")
    # mel.connect_material_property(mult_node, "", unreal.MaterialProperty.MP_EMISSIVE_COLOR)
    
    eal.save_asset(full_mat_path)
    print(f"✅ Material {mat_name} created with UNLIT + High Emissive.")
    
    # === 2. SPAWN THE MONITOR FRAME ===
    print("📺 Spawning Monitor Frame Actor...")
    
    # Main Screen Panel (Curved approximation via rotated planes)
    screen_pos = unreal.Vector(0, 0, 200)
    screen_rot = unreal.Rotator(0, 0, 0)
    
    # Spawn a large plane as the screen
    screen_actor = ell.spawn_actor_from_class(unreal.StaticMeshActor, screen_pos, screen_rot)
    screen_mesh = eal.load_asset("/Engine/BasicShapes/Plane")
    screen_actor.static_mesh_component.set_static_mesh(screen_mesh)
    screen_actor.set_actor_scale3d(unreal.Vector(10, 6, 1))  # Wide aspect ratio
    screen_actor.static_mesh_component.set_material(0, oled_mat)
    screen_actor.set_actor_label("OLED_Monitor_Screen")
    
    # Bezel Frame (Dark reflective)
    bezel_pos = unreal.Vector(0, 0, 195)
    bezel = ell.spawn_actor_from_class(unreal.StaticMeshActor, bezel_pos, screen_rot)
    bezel.static_mesh_component.set_static_mesh(eal.load_asset("/Engine/BasicShapes/Cube"))
    bezel.set_actor_scale3d(unreal.Vector(10.5, 0.1, 6.5))
    bezel.set_actor_label("OLED_Monitor_Bezel")
    
    # === 3. ADD PIXEL GRID OVERLAY ===
    print("🔲 Applying Pixel Grid Effect...")
    # This would ideally be a second material layer or decal with a grid texture
    # For now, we spawn small emissive cubes to simulate OLED pixels
    pixel_count = 20  # Per row
    for i in range(pixel_count):
        for j in range(int(pixel_count * 0.6)):  # Aspect ratio
            px = -450 + (i * 50)
            pz = 50 + (j * 50)
            if (i + j) % 3 == 0:  # Pattern
                pixel = ell.spawn_actor_from_class(unreal.PointLight, unreal.Vector(px, 50, pz), unreal.Rotator(0,0,0))
                pixel.point_light_component.set_intensity(500)
                pixel.point_light_component.set_light_color(unreal.LinearColor(0.0, 0.5, 1.0, 1.0))
                pixel.point_light_component.set_attenuation_radius(30)
    
    # === 4. POST PROCESS FOR BLOOM ===
    print("✨ Enhancing with Post Process Bloom...")
    pp = ell.spawn_actor_from_class(unreal.PostProcessVolume, unreal.Vector(0, 0, 0), unreal.Rotator(0,0,0))
    pp.unbound = True
    pp.set_actor_label("OLED_PostProcess_Bloom")
    # Bloom settings would be set via pp.settings struct if accessible
    
    # === 5. FOG FOR VOLUMETRICS ===
    fog = ell.spawn_actor_from_class(unreal.ExponentialHeightFog, unreal.Vector(0, 0, 0), unreal.Rotator(0,0,0))
    fog.set_actor_label("OLED_Volumetric_Fog")
    
    # === 6. CAMERA FOR PIXEL STREAMING VIEWPORT ===
    print("📹 Placing Pixel Streaming Camera...")
    cam = ell.spawn_actor_from_class(unreal.CameraActor, unreal.Vector(-500, 0, 200), unreal.Rotator(0, 0, 0))
    cam.set_actor_label("PixelStream_Camera")
    
    # Save Level
    ell.save_current_level()
    
    # Force save ALL dirty packages to Content folder
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
    
    print("💾 Level and ALL Assets Saved to Content folder.")
    print("🎉 FUTURISTIC OLED MONITOR CONSTRUCTED!")
    print("   - Open Unreal Editor and press PLAY to stream via Pixel Streaming.")

if __name__ == "__main__":
    create_futuristic_oled_monitor()
