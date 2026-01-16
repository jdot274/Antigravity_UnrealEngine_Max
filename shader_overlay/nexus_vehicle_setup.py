import unreal

def setup_nx_vehicle():
    print("🏎️  Configuring Nexus GT x RL Vehicle Physics...")
    
    # 1. Load the Vehicle Blueprint Base or Actor
    # In a real project, we'd have a specific Skeletal Mesh. 
    # For this procedural build, we will use a Cube as a proxy for the body
    # and 4 Spheres as wheels, but with high-fidelity physics settings.
    
    editor_lib = unreal.EditorLevelLibrary
    asset_lib = unreal.EditorAssetLibrary
    
    actor_name = "NX_Drift_Interceptor"
    car_actor = editor_lib.spawn_actor_from_class(unreal.StaticMeshActor, unreal.Vector(0,0,100))
    car_actor.set_actor_label(actor_name)
    
    body_mesh = asset_lib.load_asset("/Engine/BasicShapes/Cube.Cube")
    car_actor.static_mesh_component.set_static_mesh(body_mesh)
    car_actor.set_actor_scale3d(unreal.Vector(2.0, 1.2, 0.5))
    
    # Enable High-Fidelity Physics
    smc = car_actor.static_mesh_component
    smc.set_simulate_physics(True)
    smc.set_mass_override_in_kg("Body", 1200.0) # GT weight
    smc.set_linear_damping(0.01)
    smc.set_angular_damping(0.5) # Stable drifting
    
    # 2. Add 'Glass HUD' Component
    # This attaches a plane in front of the car view for the volumetric shader
    hud_plane = unreal.StaticMeshComponent()
    car_actor.add_instance_component(hud_plane)
    hud_plane.register_component()
    hud_plane.set_static_mesh(asset_lib.load_asset("/Engine/BasicShapes/Plane.Plane"))
    hud_plane.attach_to_component(car_actor.root_component, unreal.AttachmentTransformRules(unreal.AttachmentRule.KEEP_RELATIVE, False))
    hud_plane.set_relative_location(unreal.Vector(150, 0, 80))
    hud_plane.set_relative_rotation(unreal.Rotator(0, 0, -90))
    hud_plane.set_relative_scale3d(unreal.Vector(1, 1.77, 1)) # 16:9 Aspect
    
    # 3. Setup PS4 6DOF Controls
    set_up_inputs()

    print("✅ Vehicle Physics & Glass HUD Integrated.")

def set_up_inputs():
    """Configures project input settings for 6DOF PS4 Controller logic."""
    input_settings = unreal.InputSettings.get_input_settings()
    
    # helper to add axis mapping
    def add_axis(name, key, scale=1.0):
        mapping = unreal.InputAxisKeyMapping()
        mapping.axis_name = name
        mapping.key = unreal.InputKey(key)
        mapping.scale = scale
        input_settings.add_axis_mapping(mapping, True) # True = force rebuild

    print("🎮 Configuring PS4 6DOF Inputs...")
    
    # Forward / Backward (Thrust) - R2 / L2
    add_axis("Thrust", "Gamepad_RightTriggerAxis", 1.0)
    add_axis("Thrust", "Gamepad_LeftTriggerAxis", -1.0)
    
    # Yaw (Turn Left/Right) - Left Stick X
    add_axis("Yaw", "Gamepad_LeftX", 1.0)
    
    # Pitch (Nose Up/Down) - Left Stick Y
    add_axis("Pitch", "Gamepad_LeftY", -1.0) # Inverted for intuitive flight/drive
    
    # Roll (Barrel Roll) - L1 / R1
    add_axis("Roll", "Gamepad_RightShoulder", 1.0)
    add_axis("Roll", "Gamepad_LeftShoulder", -1.0)
    
    # Strafe (Side to Side) - Right Stick X
    add_axis("Strafe", "Gamepad_RightX", 1.0)
    
    # Vertical (Up/Down) - Right Stick Y
    add_axis("Vertical", "Gamepad_RightY", 1.0)
    add_axis("Vertical", "Gamepad_FaceButton_Bottom", 1.0) # X or A
    add_axis("Vertical", "Gamepad_FaceButton_Right", -1.0) # Circle or B

    # Force save
    unreal.EditorAssetLibrary.save_asset("/Engine/Input/InputSettings")

if __name__ == "__main__":
    setup_nx_vehicle()
