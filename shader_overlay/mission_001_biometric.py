import unreal
import json
import os

def build_biometric_scene():
    print("🚀 Initiating Mission 001: Biometric Entry...")
    
    # 1. Load Point Cloud Data
    json_path = "/Users/joeywalter/antigravity-nexus/Content/biometric_cloud.json"
    if not os.path.exists(json_path):
        unreal.log_error(f"Missing point cloud at {json_path}")
        return

    with open(json_path, 'r') as f:
        points = json.load(f)
        
    # 2. Setup Level
    # Create or Find the Scanner Actor
    actor_name = "BiometricScanner_Holo"
    existing = unreal.EditorLevelLibrary.get_all_level_actors()
    scanner_actor = None
    
    for a in existing:
        if a.get_actor_label() == actor_name:
            unreal.EditorLevelLibrary.destroy_actor(a) # Cleanup previous run
            
    scanner_actor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.StaticMeshActor, unreal.Vector(0,0,100), unreal.Rotator(0,0,0))
    scanner_actor.set_actor_label(actor_name)
    
    # 3. Create Instanced Mesh
    # We use the RootComponent (StaticMeshComponent) or add a new ISM
    # Ideally, replace the static mesh comp with an ISM, or add it
    
    # Python API: We can't easily 'replace' root in spawned actor via simple script without blueprint factory, 
    # but we can add a component.
    
    ism_comp = unreal.InstancedStaticMeshComponent()
    scanner_actor.add_instance_component(ism_comp)
    ism_comp.register_component()
    ism_comp.attach_to_component(scanner_actor.root_component, unreal.AttachmentTransformRules(unreal.AttachmentRule.KEEP_RELATIVE, False))
    
    # ... (Previous code)
    
    # 3b. Procedural Hologram Material
    # We will create a Material Instance Dynamic (MID) or Asset if possible, 
    # but for editor scripts, creating a new Asset is better.
    
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    mat_path = "/Game/Materials"
    if not unreal.EditorAssetLibrary.does_directory_exist(mat_path):
        unreal.EditorAssetLibrary.make_directory(mat_path)
        
    mat_name = "MI_HoloCyan"
    full_mat_path = f"{mat_path}/{mat_name}"
    
    # Base Material (Engine Basic)
    base_mat = unreal.EditorAssetLibrary.load_asset("/Engine/BasicShapes/BasicShapeMaterial")
    mi_asset = unreal.EditorAssetLibrary.load_asset(full_mat_path)
    
    if not mi_asset and base_mat:
        # Create Material Instance
        factory = unreal.MaterialInstanceConstantFactoryNew()
        mi_asset = asset_tools.create_asset(mat_name, mat_path, unreal.MaterialInstanceConstant, factory)
        unreal.MaterialEditingLibrary.set_material_instance_parent(mi_asset, base_mat)
        
        # Set Parameters (Emissive/Color)
        # Note: BasicShapeMaterial usually has 'Color' vector param.
        # We'll set it to Cyan Emissive-ish
        unreal.MaterialEditingLibrary.set_material_instance_vector_parameter_value(mi_asset, "Color", unreal.LinearColor(0.0, 5.0, 10.0, 1.0)) # Bright Cyan
        
    # Set Mesh & Material
    SphereMesh = unreal.EditorAssetLibrary.load_asset("/Engine/BasicShapes/Sphere.Sphere")
    if SphereMesh:
        ism_comp.set_static_mesh(SphereMesh)
        if mi_asset:
            ism_comp.set_material(0, mi_asset)
        
    # 4. Generate Instances
    print(f"✨ Manifesting {len(points)} holographic voxels...")
    
    for p in points:
        t_data = p["t"]
        # Scale down the sphere to be a small dot
        transform = unreal.Transform(
            location=unreal.Vector(t_data[0], t_data[1], t_data[2]),
            rotation=unreal.Rotator(0,0,0),
            scale=unreal.Vector(0.04, 0.04, 0.04) 
        )
        ism_comp.add_instance(transform)
        
    # 5. Framing Camera
    # Look at the center of the fingerprint
    cam_location = unreal.Vector(-200, 0, 200) 
    cam_rotation = unreal.Rotator(-45, 0, 0) # Pitch, Yaw, Roll
    
    cam_actor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.CineCameraActor, cam_location, cam_rotation)
    cam_actor.set_actor_label("Biometric_Camera_entry")
    
    # Focus
    cam_comp = cam_actor.camera_component
    cam_comp.focus_settings.manual_focus_distance = 300.0
    cam_comp.current_focal_length = 50.0 # Portrait lens
    
    print("✅ Biometric Scene Constructed with MI_HoloCyan.")

if __name__ == "__main__":
    build_biometric_scene()
