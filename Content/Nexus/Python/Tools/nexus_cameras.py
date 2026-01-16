import unreal

def spawn_ar_camera_rig():
    """
    Spawns an 'Enhanced' AR Camera Rig.
    Uses native CineCameraActors but calibrates them to match
    real-world AR hardware specifications (iPhone LIDAR, HoloLens).
    """
    ell = unreal.EditorLevelLibrary
    eal = unreal.EditorAssetLibrary
    
    unreal.log("🎥 SPAWNING ENHANCED AR CINE CAMERAS...")
    
    # 1. Device Profiles
    profiles = [
        {
            "name": "AR_Cam_iPhone14Pro",
            "sensor_width": 24.0, # Approximate
            "sensor_height": 18.0, 
            "focal_length": 24.0, # Main lens
            "aperture": 1.78,
            "grain": 0.5, # Pass-through noise
            "loc": unreal.Vector(-300, -100, 150)
        },
        {
            "name": "AR_Cam_HoloLens2",
            "sensor_width": 16.0, 
            "sensor_height": 9.0, 
            "focal_length": 18.0, # Wide
            "aperture": 2.8,
            "grain": 1.5, # Holographic grit
            "loc": unreal.Vector(-300, 100, 150)
        },
        {
            "name": "AR_Cam_VisionPro",
            "sensor_width": 24.0, # Micro-OLED Equivalent
            "sensor_height": 20.0,
            "focal_length": 21.0, 
            "aperture": 2.0,
            "grain": 0.1, # Extremely clean passthrough
            "loc": unreal.Vector(-300, 0, 200)
        }
    ]
    
    for p in profiles:
        # Spawn CineCameraActor
        cam_actor = ell.spawn_actor_from_class(unreal.CineCameraActor, p["loc"], unreal.Rotator(0,0,0))
        cam_actor.set_actor_label(p["name"])
        
        # "Wrap" with Enhanced Settings
        camera_comp = cam_actor.camera_component
        
        # Filmback (Sensor)
        filmback = camera_comp.filmback
        filmback.sensor_width = p["sensor_width"]
        filmback.sensor_height = p["sensor_height"]
        camera_comp.filmback = filmback
        
        # Lens
        lens = camera_comp.lens_settings
        lens.min_f_stop = 1.2
        lens.max_f_stop = 22.0
        camera_comp.lens_settings = lens
        
        camera_comp.current_focal_length = p["focal_length"]
        camera_comp.current_aperture = p["aperture"]
        
        # Focus (Simulate AR Autofocus)
        focus = camera_comp.focus_settings
        focus.focus_method = unreal.CameraFocusMethod.TRACKING
        camera_comp.focus_settings = focus
        
        # Post Process (Simulate AR Passthrough Artifacts)
        # Note: In Python we access the struct. Setting individual weighted blendables is complex, 
        # so we stick to main properties.
        pp = camera_comp.post_process_settings
        
        # Enable overrides
        # Setting values in Python API for FPostProcessSettings is direct
        pp.override_film_grain_intensity = True
        pp.film_grain_intensity = p["grain"]
        
        pp.override_vignette_intensity = True
        pp.vignette_intensity = 0.6 if "HoloLens" in p["name"] else 0.2
        
        pp.override_motion_blur_amount = True
        pp.motion_blur_amount = 0.0 # AR usually wants crisp frames for CV
        
        camera_comp.post_process_settings = pp
        
        # Tag as Neural AR
        # Explicit mapping to Unreal Object Type as requested
        cam_actor.tags = ["NexusAR", "NeuralInput", f"NexusType:{cam_actor.get_class().get_name()}"]
        
        unreal.log(f"   [+] Registered {p['name']} (Simulated Hardware)")

    unreal.log("✅ AR CINE RIG COMPLETE.")

if __name__ == "__main__":
    spawn_ar_camera_rig()
