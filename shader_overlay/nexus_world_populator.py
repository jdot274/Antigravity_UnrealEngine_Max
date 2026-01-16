import unreal
import random
import math

def populate_chaos_scene():
    """
    Populates the current level with a diverse array of 'Antigravity' assets.
    """
    print("🌌 Initiating Protocol: TOTAL_VIEWPORT_SATURATION")
    
    ell = unreal.EditorLevelLibrary
    eal = unreal.EditorAssetLibrary
    
    # Base Materials
    glass_mat = eal.load_asset("/Game/Nexus/Materials/M_NexusGlass")
    neon_blue = eal.load_asset("/Game/Nexus/Materials/Neon/M_NeonBlue")
    neon_pink = eal.load_asset("/Game/Nexus/Materials/Neon/M_NeonPink")

    # 1. Spawn The "Arena" (Floor)
    floor = ell.spawn_actor_from_class(unreal.StaticMeshActor, unreal.Vector(0, 0, 0), unreal.Rotator(0, 0, 0))
    floor.static_mesh_component.set_static_mesh(eal.load_asset("/Engine/BasicShapes/Plane"))
    floor.set_actor_scale3d(unreal.Vector(50, 50, 1))
    # floor.static_mesh_component.set_material(0, glass_mat)
    
    # 2. Spawn "Floaters" (Diverse Shapes)
    shapes = [
        "/Engine/BasicShapes/Cube",
        "/Engine/BasicShapes/Sphere",
        "/Engine/BasicShapes/Cylinder",
        "/Engine/BasicShapes/Cone"
    ]
    
    print("✨ Spawning 50 Floating Anomalies...")
    for i in range(50):
        # Random Position (Donut distribution)
        angle = random.uniform(0, 2 * math.pi)
        dist = random.uniform(500, 2500)
        z = random.uniform(200, 1200)
        
        pos = unreal.Vector(math.cos(angle) * dist, math.sin(angle) * dist, z)
        rot = unreal.Rotator(random.uniform(0, 360), random.uniform(0, 360), random.uniform(0, 360))
        
        # Spawn
        actor = ell.spawn_actor_from_class(unreal.StaticMeshActor, pos, rot)
        mesh_path = random.choice(shapes)
        mesh = eal.load_asset(mesh_path)
        actor.static_mesh_component.set_static_mesh(mesh)
        
        # Random Material
        if random.random() > 0.6:
            actor.static_mesh_component.set_material(0, random.choice([neon_blue, neon_pink]))
        else:
            actor.static_mesh_component.set_material(0, glass_mat)
            
        # Random Scale
        scale = random.uniform(0.5, 3.0)
        actor.set_actor_scale3d(unreal.Vector(scale, scale, scale))

    # 3. Lighting (Rect Lights for Cyberpunk feel)
    print("💡 Installing Lumens...")
    for i in range(4):
        pos = unreal.Vector(0, 0, 1000)
        # 4 corners
        x = 1000 if i % 2 == 0 else -1000
        y = 1000 if i < 2 else -1000
        
        light = ell.spawn_actor_from_class(unreal.RectLight, unreal.Vector(x, y, 600), unreal.Rotator(-45, 0, 0))
        # light.light_component.set_intensity(5000)
        # light.light_component.set_light_color(unreal.LinearColor(0, 1, 1, 1))

    # 4. Volumetric Fog (ExponentialHeightFog)
    fog = ell.spawn_actor_from_class(unreal.ExponentialHeightFog, unreal.Vector(0, 0, 0), unreal.Rotator(0, 0, 0))
    # fog.component.set_volumetric_fog(True)

    # 5. Post Process Volume (Global FX)
    print("🎥 Injecting Post-Process Volume...")
    pp_vol = ell.spawn_actor_from_class(unreal.PostProcessVolume, unreal.Vector(0, 0, 0), unreal.Rotator(0, 0, 0))
    pp_vol.unbound = True
    # We can't easily set complex struct props via Python API without strict knowledge of the struct layout,
    # but spawning it ensures the user can tweak Bloom/Exposure immediately.

    # 6. Procedural Mesh Clusters (Stacks)
    print("🏗️ Generative Construction: Mesh Stacks...")
    for i in range(10):
        base_pos = unreal.Vector(random.uniform(-2000, 2000), random.uniform(-2000, 2000), 0)
        for j in range(5):
            # Stack 'em up
            offset = unreal.Vector(0, 0, j * 110)
            actor = ell.spawn_actor_from_class(unreal.StaticMeshActor, base_pos + offset, unreal.Rotator(0, random.uniform(0, 90), 0))
            actor.static_mesh_component.set_static_mesh(eal.load_asset("/Engine/BasicShapes/Cube"))
            actor.static_mesh_component.set_material(0, neon_blue if j % 2 == 0 else neon_pink)

    # 7. Particles (Niagara/Cascade)
    # Attempting to spawn standard if available, or just placeholders
    print("✨ Igniting Particle Systems...")
    # Typically "/Game/StarterContent/Particles/P_Sparks"
    try:
        emitter = eal.load_asset("/Game/StarterContent/Particles/P_Sparks")
        if emitter:
            for k in range(5):
                ell.spawn_actor_from_object(emitter, unreal.Vector(random.uniform(-1000, 1000), random.uniform(-1000, 1000), 500))
    except:
        print("⚠️ Starter Content Particles not found. Skipping.")

    print("✅ Viewport Saturated. Ready for Antigravity.")
    
    # Save the chaos
    ell.save_current_level()
    print("💾 Level Saved.")

if __name__ == "__main__":
    populate_chaos_scene()
