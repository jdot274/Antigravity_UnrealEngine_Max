import unreal
import random
import math
import sys
import os

# Add current dir to path to allow importing sibling scripts if needed
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

import nexus_material_builder

def create_aaa_blueprint(asset_name, mesh_path, material_path):
    """
    Creates a new Blueprint asset with a StaticMesh component.
    """
    package_path = "/Game/Nexus/Blueprints/AAA_Artifacts"
    
    # 1. Ensure directory exists
    if not unreal.EditorAssetLibrary.does_directory_exist(package_path):
        unreal.EditorAssetLibrary.make_directory(package_path)
        
    full_path = f"{package_path}/{asset_name}"
    
    # 2. Check if exists, if so, load it
    if unreal.EditorAssetLibrary.does_asset_exist(full_path):
        print(f"♻️ Blueprint {asset_name} already exists. Updating...")
        # For simplicity in this script, we'll just load it. 
        # Real "AAA" pipeline might delete and recreate or update components.
        bp_asset = unreal.EditorAssetLibrary.load_asset(full_path)
    else:
        print(f"✨ Creating New AAA Blueprint: {asset_name}")
        factory = unreal.BlueprintFactory()
        factory.set_editor_property("parent_class", unreal.Actor)
        
        asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
        bp_asset = asset_tools.create_asset(asset_name, package_path, unreal.Blueprint, factory)

    # 3. Add/Update Static Mesh Component via SimpleConstructionScript (SCS)
    # This edits the Class Default Object's component tree
    scs = bp_asset.simple_construction_script
    
    # Check if we already have nodes (simplistic check)
    existing_nodes = scs.get_all_nodes()
    mesh_node = None
    
    if len(existing_nodes) > 0:
        # Assume first node is our mesh for this simple factory
        mesh_node = existing_nodes[0]
    else:
        # Create new node
        mesh_node = scs.create_simple_construction_script_node(unreal.StaticMeshComponent)
        scs.add_node(mesh_node)
        
    # 4. Configure the Component
    # We must access the ComponentTemplate to modify properties
    component = mesh_node.component_template
    
    # Load Mesh and Material
    mesh_asset = unreal.EditorAssetLibrary.load_asset(mesh_path)
    if not mesh_asset:
        print(f"⚠️ Warning: Mesh {mesh_path} not found. Using Cube.")
        mesh_asset = unreal.EditorAssetLibrary.load_asset("/Engine/BasicShapes/Cube")
        
    material_asset = unreal.EditorAssetLibrary.load_asset(material_path)
    
    if component:
        unreal.log(f"Setting mesh for {asset_name}...")
        component.set_static_mesh(mesh_asset)
        if material_asset:
            component.set_material(0, material_asset)
            
        # Make it look "AAA" - Enable heavy settings?
        # component.set_editor_property("cast_shadow", True)
    
    # Compile the Blueprint to save changes
    unreal.EditorAssetLibrary.save_asset(full_path)
    # unreal.BlueprintEditorLibrary.compile_blueprint(bp_asset) # Need compilation if available
    
    return bp_asset

def instantiate_in_level(bp_asset, index, total_count):
    """
    Spawns the blueprint in a showcase formation.
    """
    ell = unreal.EditorLevelLibrary
    
    # Circular formation
    radius = 1500
    angle = (index / total_count) * 2 * math.pi
    
    x = math.cos(angle) * radius
    y = math.sin(angle) * radius
    z = 300 # Float above ground
    
    location = unreal.Vector(x, y, z)
    rotation = unreal.Rotator(0, math.degrees(angle) + 90, 0) # Face outward
    
    actor = ell.spawn_actor_from_object(bp_asset, location, rotation)
    
    # Scale up for AAA impact
    if actor:
        actor.set_actor_scale3d(unreal.Vector(2.0, 2.0, 2.0))
        # Add a gentle spin or bob? (Requires Tick logic, skipping for asset instantiation)
        
    return actor

def main():
    print("🚀 Initiating AAA Mesh Instantiation Protocol...")
    
    # Ensure dependencies
    nexus_material_builder.create_nexus_glass_material()
    nexus_material_builder.create_neon_material("M_NeonBlue", (0, 0, 1))
    nexus_material_builder.create_neon_material("M_NeonPink", (1, 0, 0.5))
    nexus_material_builder.create_neon_material("M_NeonGold", (1, 0.8, 0))
    nexus_material_builder.create_neon_material("M_VoidBlack", (0, 0, 0))
    
    # List of 10 AAA Artifacts
    # Name, Mesh (try to use standard engine shapes or starter content), Material
    
    # Note: We rely on Engine content typically available.
    artifacts = [
        ("BP_ChronosBuffer", "/Engine/BasicShapes/Cube", "/Game/Nexus/Materials/M_NexusGlass"),
        ("BP_NebulaFragment", "/Engine/BasicShapes/Sphere", "/Game/Nexus/Materials/Neon/M_NeonBlue"),
        ("BP_VoidAnchor", "/Engine/BasicShapes/Cylinder", "/Game/Nexus/Materials/Neon/M_VoidBlack"),
        ("BP_LumenDrive", "/Engine/BasicShapes/Cone", "/Game/Nexus/Materials/Neon/M_NeonGold"),
        ("BP_HyperLens", "/Engine/BasicShapes/Sphere", "/Game/Nexus/Materials/M_NexusGlass"), 
        ("BP_GravityWell", "/Engine/BasicShapes/Torus", "/Game/Nexus/Materials/Neon/M_NeonPink"), # Torus might not be in BasicShapes, checking defaults fallback
        ("BP_QuantumShard", "/Engine/BasicShapes/Cone", "/Game/Nexus/Materials/Neon/M_NeonBlue"),
        ("BP_FluxCapacitor", "/Engine/BasicShapes/Cube", "/Game/Nexus/Materials/Neon/M_NeonGold"),
        ("BP_StellarPrism", "/Engine/BasicShapes/Cylinder", "/Game/Nexus/Materials/M_NexusGlass"),
        ("BP_OmegaKey", "/Engine/BasicShapes/Sphere", "/Game/Nexus/Materials/Neon/M_NeonPink"),
    ]
    
    spawned_count = 0
    
    for i, (name, mesh, mat) in enumerate(artifacts):
        # 1. Create/Get Blueprint
        bp = create_aaa_blueprint(name, mesh, mat)
        
        # 2. Spawn in Level
        if bp:
            instantiate_in_level(bp, i, len(artifacts))
            spawned_count += 1
            
    print(f"✅ Successfully instantiated {spawned_count} AAA Meshes in the Main Level.")

if __name__ == "__main__":
    main()
