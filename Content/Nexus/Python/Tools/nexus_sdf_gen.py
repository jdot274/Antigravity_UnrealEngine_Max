import unreal
import numpy as np
import math
import random

def create_sdf_actor(name, formula_type="gyroid", location=(0,0,0)):
    """
    Generates a dense point cloud or mesh proxy based on SDF formulas.
    Since we can't generate raw mesh buffers easily in Python without C++,
    we will use InstancedStaticMesh to visualize the 'Voxel Field' of the SDF.
    """
    ell = unreal.EditorLevelLibrary
    eal = unreal.EditorAssetLibrary

    # 1. Spawn a container actor
    actor = ell.spawn_actor_from_class(unreal.StaticMeshActor, unreal.Vector(*location), unreal.Rotator(0,0,0))
    actor.set_actor_label(f"SDF_{name}")
    
    # 2. Add HISM (Hierarchical Instanced Static Mesh) for performance
    hism = unreal.HierarchicalInstancedStaticMeshComponent()
    actor.add_instance_component(hism)
    hism.set_static_mesh(unreal.load_asset("/Game/Nexus/Meshes/Cube_Default")) # Fallback
    
    # Attempts to load a better mesh if available, or just use a small sphere
    sphere = unreal.load_asset("/Engine/BasicShapes/Sphere.Sphere")
    if sphere:
        hism.set_static_mesh(sphere)
    
    # Material (BSDF Priority)
    mat = unreal.load_asset("/Game/Nexus/Materials/M_Nexus_BSDF_Master_Inst")
    if not mat:
         # Fallback
         mat = unreal.load_asset("/Game/Nexus/Materials/M_OLED_Futuristic")
         
    if mat:
        hism.set_material(0, mat)

    unreal.log(f"∑ Calculating SDF Geometry: {formula_type}...")

    # 3. Generate Points using Numpy
    # Create a grid
    res = 20 # Resolution (20x20x20 = 8000 points)
    x = np.linspace(-math.pi, math.pi, res)
    y = np.linspace(-math.pi, math.pi, res)
    z = np.linspace(-math.pi, math.pi, res)
    X, Y, Z = np.meshgrid(x, y, z)
    
    # SDF Formulas
    if formula_type == "gyroid":
        # sin(x)cos(y) + sin(y)cos(z) + sin(z)cos(x) = 0
        S = np.sin(X)*np.cos(Y) + np.sin(Y)*np.cos(Z) + np.sin(Z)*np.cos(X)
        threshold = 0.5
    elif formula_type == "schwarz_p":
        # cos(x) + cos(y) + cos(z) = 0
        S = np.cos(X) + np.cos(Y) + np.cos(Z)
        threshold = 0.4
    elif formula_type == "fairway":
        # GOLF ENGINE: Smooth Rolling Hills (2D Sine interference)
        # Z - (sin(x/2) + cos(y/3)) = 0 (Heightmap style SDF)
        # Scaled to be large and walkable
        S = Z - (np.sin(X*0.5) + np.cos(Y*0.5))*0.8
        threshold = 0.2
    else:
        # Sphere
        S = np.sqrt(X**2 + Y**2 + Z**2) - 2.0
        threshold = 0.2

    # Filter points near the surface (Isosurface emulation)
    mask = np.abs(S) < threshold
    
    # Extract coordinates
    valid_x = X[mask]
    valid_y = Y[mask]
    valid_z = Z[mask]
    
    count = len(valid_x)
    unreal.log(f"   -> Surfaces Found: {count} voxels")

    # 4. Batch Add Instances
    transforms = []
    scale = 50.0 # Spacing multiplier
    
    for i in range(count):
        vx = float(valid_x[i]) * scale
        vy = float(valid_y[i]) * scale
        vz = float(valid_z[i]) * scale
        
        # Color variety based on position
        t = unreal.Transform()
        t.translation = unreal.Vector(vx, vy, vz)
        t.scale3d = unreal.Vector(0.15, 0.15, 0.15) # Small particles
        transforms.append(t)
        
    hism.add_instances(transforms, False)
    
    # Attach to root
    actor.set_root_component(hism)
    
    return actor

def generate_tool_garden():
    """
    Spawns SDF representations of the Gemini Tools.
    """
    tools = [
        # Analysis Layer
        {"name": "Codebase_Investigator", "shape": "gyroid", "loc": (0, 0, 200)},
        {"name": "Glob_Search", "shape": "sphere", "loc": (0, 300, 200)},
        {"name": "List_Directory", "shape": "schwarz_p", "loc": (0, 600, 200)},
        {"name": "Search_File_Content", "shape": "gyroid", "loc": (0, 900, 200)},
        
        # Action Layer
        {"name": "Replace_Tool", "shape": "schwarz_p", "loc": (400, 0, 200)},
        {"name": "Write_File", "shape": "sphere", "loc": (400, 300, 200)},
        {"name": "Run_Shell_Command", "shape": "gyroid", "loc": (400, 600, 200)},
        {"name": "Save_Memory", "shape": "schwarz_p", "loc": (400, 900, 200)},

        # External Layer
        {"name": "Google_Web_Search", "shape": "sphere", "loc": (800, 0, 200)},
        {"name": "Web_Fetch", "shape": "gyroid", "loc": (800, 300, 200)},
        {"name": "Read_File", "shape": "schwarz_p", "loc": (800, 600, 200)}
    ]
    
    for tool in tools:
        actor = create_sdf_actor(tool["name"], tool["shape"], tool["loc"])
        # Add a text label
        label = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.TextRenderActor, unreal.Vector(*tool["loc"]), unreal.Rotator(0,180,0))
        label.set_actor_label(f"Label_{tool['name']}")
        label.text_render.set_text(tool["name"].replace("_", " "))
        label.text_render.set_text_render_color(unreal.Color(0, 255, 255, 255))
        label.set_actor_scale3d(unreal.Vector(2,2,2))
        # Move label up
        l_loc = label.get_actor_location()
        l_loc.z += 150
        label.set_actor_location(l_loc, False, False)

if __name__ == "__main__":
    generate_tool_garden()
