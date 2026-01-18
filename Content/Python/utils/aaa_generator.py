import unreal
import math
import json
import os
import random

# CONFIGURATION
BASE_PATH = "/Game/FuturisticSystems"
X_SPACING = 500.0
SPIRAL_RADIUS_START = 800.0
SPIRAL_GROWTH = 300.0
Z_STEP = 150.0

def create_directory(path):
    if not unreal.EditorAssetLibrary.does_directory_exist(path):
        unreal.EditorAssetLibrary.make_directory(path)
        unreal.log(f"Created directory: {path}")

def generate_ai_solutions():
    """Simulates the Gemini Ultra Brain output inline for robustness."""
    solutions = [
        {"title": "Gemini Ultra Neural Link", "desc": "Real-time PPO Latency Prediction"},
        {"title": "Infinite Nanite Labyrinth", "desc": "Procedural Geometry via Emotion Analysis"},
        {"title": "Voice-to-Shader Compiler", "desc": "Whisper API -> HLSL Graph"},
        {"title": "NPC Dream Layer", "desc": "Offline Python Simulation of Social Bias"},
        {"title": "Biometric Gravity", "desc": "Twitch Heartrate -> Physics Z-Gravity"},
        {"title": "Chaos Monkey QA", "desc": "Automated 100x Speed Playtesting"},
        {"title": "Semantic Audio Synth", "desc": "Texture Density -> Granular Synthesis"},
        {"title": "GI Hallucination", "desc": "GAN-based Fake Raytracing"},
        {"title": "Narrative Self-Healing", "desc": "Dynamic Lore Rewrites via LLM"},
        {"title": "Codebase Auto-Fix", "desc": "Stack Trace -> C++ Recompile"},
        {"title": "4D Hyper-Inventory", "desc": "Tesseract UI Folding"},
        {"title": "Swarm Light Baking", "desc": "Distributed WebGPU Lightmass"},
        {"title": "Style Transfer Viewport", "desc": "Live Cyberpunk Filter"},
        {"title": "LIDAR Segmentation", "desc": "Point Cloud -> Gameplay Cover"},
        {"title": "Context Tutorial", "desc": "Input Analysis -> TTS Advice"},
        {"title": "NLP Fluid Sim", "desc": "Language -> Niagara Vector Fields"},
        {"title": "Generative Loading", "desc": "Battle Recap -> Concept Art"},
        {"title": "Economy Monte Carlo", "desc": "Inflation Prediction Model"},
        {"title": "Haptic Synthesis", "desc": "Audio Waveform -> Rumble Buffer"},
        {"title": "The Antigravity Algo", "desc": "Flow State Movement Assist"},
        {"title": "C++ Hot Reload", "desc": "Live Module Patching"},
        {"title": "Python API Bridge", "desc": "Subprocess Communication"}
    ]
    return solutions

def spawn_floating_text(world, text, location, rotation, color=(0.0, 1.0, 1.0)):
    """Spawns a TextRenderActor to display info in 3D space."""
    actor_class = unreal.TextRenderActor
    actor = unreal.EditorLevelLibrary.spawn_actor_from_class(actor_class, location, rotation)
    
    if not actor:
        return None
        
    actor.set_actor_label(f"AI_Info_{text[:10]}")
    actor.text_render.set_text(text)
    actor.text_render.set_text_render_color(unreal.Color(r=int(color[0]*255), g=int(color[1]*255), b=int(color[2]*255), a=255))
    actor.text_render.set_world_scale3d(unreal.Vector(5, 5, 5)) # Make it BIG
    
    return actor

def setup_spiral_gallery():
    """Creates a Fibonacci spiral of AI concepts."""
    solutions = generate_ai_solutions()
    world = unreal.EditorLevelLibrary.get_editor_world()
    
    # Origin
    origin = unreal.Vector(0, 0, 500)
    
    # Golden Angle
    phi = math.pi * (3.0 - math.sqrt(5.0)) 
    
    for i, sol in enumerate(solutions):
        y = i * Z_STEP  # Go up/down or keep flat? Let's go UP
        radius = SPIRAL_RADIUS_START + (i * 20.0) # Slowly grow out
        theta = i * phi * 10.0 # Tighter spiral
        
        x = origin.x + radius * math.cos(theta)
        z = origin.y + radius * math.sin(theta) # Flattened on Z plane usually, but let's use Y for depth
        
        # Unreal Coordinates: Z is Up, X is Forward, Y is Right
        # Let's map circle to X,Y and step up in Z
        
        loc_x = radius * math.cos(theta)
        loc_y = radius * math.sin(theta)
        loc_z = 300.0 + (i * 100.0)
        
        location = unreal.Vector(loc_x, loc_y, loc_z)
        
        # Look at 0,0,Z
        rotator = unreal.MathLibrary.find_look_at_rotation(location, unreal.Vector(0,0,loc_z))
        # Flip text to face outward or inward? Let's face inward (reader is in center)
        # TextRenderActor default orientation might require adjustment
        rotator.yaw += 180.0 
        
        # 1. Spawn Title
        title_text = f"[{i+1:02d}] {sol['title']}"
        spawn_floating_text(world, title_text, location, rotator, color=(0.0, 1.0, 0.5))
        
        # 2. Spawn Desc (slightly below)
        desc_loc = unreal.Vector(location.x, location.y, location.z - 40.0)
        desc_actor = spawn_floating_text(world, sol['desc'], desc_loc, rotator, color=(0.8, 0.8, 0.8))
        if desc_actor:
            desc_actor.text_render.set_world_scale3d(unreal.Vector(2.5, 2.5, 2.5))

        # 3. Add a structural mesh anchor (Cube)
        mesh_loc = unreal.Vector(location.x, location.y, location.z - 80.0)
        mesh_actor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.StaticMeshActor, mesh_loc, rotator)
        cube_mesh = unreal.EditorAssetLibrary.load_asset("/Engine/BasicShapes/Cube.Cube")
        if mesh_actor and cube_mesh:
            mesh_actor.static_mesh_component.set_static_mesh(cube_mesh)
            mesh_actor.set_actor_scale3d(unreal.Vector(0.5, 0.5, 0.05)) # Platform
            
    unreal.log("--- AI Spiral Gallery Generated ---")

def enable_aaa_rendering():
    """Forces high-fidelity rendering settings via Console Variables."""
    cmds = [
        "r.DynamicGlobalIlluminationMethod 1", # Lumen
        "r.ReflectionMethod 1",                # Lumen
        "r.Lumen.Reflections.AllowRayTracing 1",
        "r.Lumen.TranslucencyReflections.FrontLayer.Enable 1",
        "r.Shadow.Virtual.Enable 1",           # Virtual Shadow Maps
        "r.Nanite 1",
        "r.HighQualityLightMaps 1",
        "r.PostProcessing.PropagateAlpha 1",   # For UI compositing
        "r.NGX.DLSS.Enable 1",                 # DLSS (if plugin active)
        "r.NGX.DLSS.Quality 0",                # 0=Auto/Quality
        "r.DistanceFieldGI 1",
        "r.GenerateMeshDistanceFields 1"
    ]
    for cmd in cmds:
        unreal.SystemLibrary.execute_console_command(None, cmd)
    unreal.log("🚀 AAA RENDERING PIPELINE ACTIVATED: Lumen + Nanite + VSM + DLSS")

def setup_post_process_volume(world):
    """Spawns an Unbound PostProcessVolume for Cinematic Grading."""
    pp_actor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.PostProcessVolume, unreal.Vector(0,0,0))
    pp_actor.set_actor_label("Global_Cinematic_PP")
    pp_actor.unbound = True
    
    # Python API for PP settings is verbose, we set key values via reflection if needed
    # Or rely on the default settings which usually inherit the Project Settings we just forced.
    # But let's try to set exposure to reasonable fixed values to avoid 'auto-exposure blinding'
    
    # Note: Accessing struct properties deeply via Python is tricky. 
    # We will trust the CVARs for the heavy lifting.
    unreal.log("🎥 Cinematic Post-Process Volume Created.")

def ensure_level_exists_and_load(map_path):
    """Ensures the target level exists and opens it."""
    # Check if asset exists
    if not unreal.EditorAssetLibrary.does_asset_exist(map_path):
        unreal.log(f"Creating NEW Level: {map_path}")
        unreal.EditorLevelLibrary.new_level(map_path)
    else:
        unreal.log(f"Loading EXISTING Level: {map_path}")
        unreal.EditorLevelLibrary.load_level(map_path)

def run_script():
    unreal.log("--- Initiating Antigravity AAA Content Generator ---")
    
    TARGET_MAP = "/Game/FuturisticSystems/Maps/Antigravity_Showcase"
    
    with unreal.ScopedEditorTransaction("GenAAAContent"):
        # 1. PERMANENT STORAGE: Create/Load specific Level
        ensure_level_exists_and_load(TARGET_MAP)
        
        # 2. Setup Directories
        create_directory(BASE_PATH)
        create_directory("/Game/FuturisticSystems/Maps")
        
        # 3. RENDER CONFIG: Force AAA
        enable_aaa_rendering()
        setup_post_process_volume(unreal.EditorLevelLibrary.get_editor_world())
        
        # 4. Generate Content
        # Clean up previous actors in this level to prevent duplicates if re-run
        # (Optional: clear_level_actors())
        
        setup_spiral_gallery()
        
        # 5. STARTUP VIEW: Set camera to a good spot
        # (Optional: Spawn a camera or move viewport)
        
    # 6. PERMANENT STORAGE: Force Save
    unreal.log("💾 SAVING ALL ASSETS TO DISK...")
    unreal.EditorLoadingAndSavingUtils.save_current_level()
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(save_map_packages=True, save_content_packages=True)
    unreal.log(f"✅ PERMANENTLY STORED: {TARGET_MAP}")
    unreal.log("--- Generation Complete. World populated with AI Models. ---")

if __name__ == "__main__":
    run_script()
