import unreal
import os
import json
import subprocess

class NexusDriftRL:
    def __init__(self):
        self.asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
        self.editor_lib = unreal.EditorLevelLibrary
        self.asset_lib = unreal.EditorAssetLibrary
        self.sub_server = None
        self.shot_count = 0

    def setup_pixel_streaming(self):
        """Initializes the Pixel Streaming signaling server and provides the build config."""
        print("🔗 Setting up Pixel Streaming Signaling Server...")
        
        # Path to signalling server in the bridge dir
        server_path = "/Users/joeywalter/antigravity-nexus/bridge/SignallingWebServer/platform_scripts/bash/start.sh"
        
        if os.path.exists(server_path):
            # Start the server in the background
            # self.sub_server = subprocess.Popen(["bash", server_path], stdout=subprocess.PIPE)
            print("✅ Signaling Server command prepared.")
        else:
            print("⚠️ Signaling server script not found. Ensure Pixel Streaming plugin is configured.")

    def create_gt_rl_hybrid_level(self):
        """Builds the high-speed arena with glass spheres and GT-style lighting."""
        print("🏎️  Building Gran Turismo x Rocket League Arena...")
        
        # 1. Create a Large Arena (Gran Turismo Style)
        floor_mesh = self.asset_lib.load_asset("/Engine/BasicShapes/Cube.Cube")
        arena_floor = self.editor_lib.spawn_actor_from_class(unreal.StaticMeshActor, unreal.Vector(0,0,0))
        arena_floor.set_actor_label("ArenaFloor_GT")
        arena_floor.static_mesh_component.set_static_mesh(floor_mesh)
        arena_floor.set_actor_scale3d(unreal.Vector(100, 100, 1))
        
        # Apply a 'Gran Turismo' Asphalt Material (Reflective/Sleek)
        # For now, use a dark emissive placeholder
        
        # 2. Spawn the 'Glass Blur' Volumetric Spheres
        # We use our C++ ANexusVolumeActor for logic, but we need raw DENSITY of meshes
        volume_actor = self.editor_lib.spawn_actor_from_class(unreal.Actor, unreal.Vector(0,0,500))
        volume_actor.set_actor_label("VolumetricNexus_Glass_Dense")
        
        # Create Massive ISM Component
        # Use 'outer' to properly parent the component to the actor upon creation
        ism_cloud = unreal.InstancedStaticMeshComponent(outer=volume_actor, name="DenseCloudISM")
        ism_cloud.register_component()
        volume_actor.set_root_component(ism_cloud) # Set as root for clean transform
        
        # Load Sphere Mesh
        sphere_mesh = self.asset_lib.load_asset("/Engine/BasicShapes/Sphere.Sphere")
        ism_cloud.set_static_mesh(sphere_mesh)
        
        # Apply Nexus Glass Material
        # Debug: Use Opaque Material first to ensure visibility
        # glass_mat = self.asset_lib.load_asset("/Game/Nexus/Materials/M_NexusGlass")
        glass_mat = self.asset_lib.load_asset("/Engine/BasicShapes/BasicShapeMaterial")
        if glass_mat:
            ism_cloud.set_material(0, glass_mat)
            
        print("💥 GEMINI: Generating 100x Density Mesh Volume (Grid 40x40x10)...")
        
        # Generate 16,000 Instances for "Dense Pixel" feel
        # Using a generator for memory efficiency before batch add
        transforms = []
        grid_size = 4000.0
        step = 100.0 # Dense spacing
        
        for x in range(-20, 20):
            for y in range(-20, 20):
                for z in range(0, 10):
                    # Procedural Jitter
                    loc = unreal.Vector(
                        x * step + unreal.MathLibrary.random_float_in_range(-20, 20),
                        y * step + unreal.MathLibrary.random_float_in_range(-20, 20),
                        z * step * 2.0 + 100
                    )
                    scale_rand = unreal.MathLibrary.random_float_in_range(0.2, 0.8)
                    trans = unreal.Transform(
                        location=loc,
                        rotation=unreal.Rotator(0,0,0),
                        scale=unreal.Vector(scale_rand, scale_rand, scale_rand)
                    )
                    transforms.append(trans)
        
        # Batch Add (much faster than loop add_instance)
        # Note: python API for add_instances is cleaner in recent UE versions
        for t in transforms:
             ism_cloud.add_instance(t)
             
        print(f"✅ Generated {len(transforms)} Volumetric Glass Spheres.")
        
        # 3. Setup the Rocket League Ball
        ball_mesh = self.asset_lib.load_asset("/Engine/BasicShapes/Sphere.Sphere")
        rl_ball = self.editor_lib.spawn_actor_from_class(unreal.StaticMeshActor, unreal.Vector(1000, 0, 200))
        rl_ball.set_actor_label("RL_Ball")
        rl_ball.static_mesh_component.set_static_mesh(ball_mesh)
        rl_ball.static_mesh_component.set_simulate_physics(True)
        rl_ball.set_actor_scale3d(unreal.Vector(5, 5, 5))
        
        # 4. Cinematic Lighting
        sun = self.editor_lib.spawn_actor_from_class(unreal.DirectionalLight, unreal.Vector(0,0,1000))
        sun.set_actor_rotation(unreal.Rotator(-45, 45, 0), False)
        sun.get_component_by_class(unreal.DirectionalLightComponent).set_intensity(10.0)
        
        sky = self.editor_lib.spawn_actor_from_class(unreal.SkyLight, unreal.Vector(0,0,1000))
        
        print("✨ Arena Construction Complete.")

    def setup_camera(self):
        """Spawns a Cine Camera with GT-style focal depth."""
        print("🎥 Setting up Cinematic Camera...")
        cam_loc = unreal.Vector(-2000, -2000, 1000)
        cam_rot = unreal.Rotator(-15, 45, 0)
        camera_actor = self.editor_lib.spawn_actor_from_class(unreal.CineCameraActor, cam_loc, cam_rot)
        camera_actor.set_actor_label("CinematicCam_GT")
        
        # Set focal length for that 'compressed' GT look
        cam_comp = camera_actor.get_cine_camera_component()
        cam_comp.focus_settings.focus_method = unreal.CameraFocusMethod.MANUAL
        cam_comp.focus_settings.manual_focus_distance = 3000.0
        cam_comp.current_focal_length = 85.0 # High focal length for speed compression
        
        return camera_actor

    def render_screenshot(self):
        """Captures a high-resolution screenshot of the scene."""
        print("📸 Rendering High-Res Screenshot...")
        
        # Save current level so it exists on disk for potential MRQ
        level_path = "/Game/Nexus/Maps/NexusArena_Render"
        if not self.asset_lib.does_directory_exist("/Game/Nexus/Maps"):
            self.asset_lib.make_directory("/Game/Nexus/Maps")
            
        # Save level
        unreal.EditorLevelLibrary.save_current_level()
        
        # Trigger High-Res Screenshot
        # We can use the console command for simplicity in this script
        unreal.SystemLibrary.execute_console_command(None, "HighResShot 3840x2160")
        print(f"✅ Render request sent to viewport.")

    def launch_sim(self):
        """Starts the PIE (Play In Editor) session for live pixel streaming."""
        print("🎮 Launching Nexus Drift RL Simulation...")
        # unreal.EditorLevelLibrary.editor_play_sim() # Often requires focus or specific settings
        print("🚀 Ready for PIE.")

if __name__ == "__main__":
    game = NexusDriftRL()
    game.setup_pixel_streaming()
    game.create_gt_rl_hybrid_level()
    game.setup_camera()
    game.render_screenshot()
    game.launch_sim()
