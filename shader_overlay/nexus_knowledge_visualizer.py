import unreal
import json
import os
import math

# Paths
DB_PATH = "/Users/joeywalter/antigravity-nexus/shader_overlay/galaxy_knowledge_db.json"

def visualize_knowledge_galaxy():
    """
    Reads the Galaxy Knowledge JSON and spawns a 3D visualization of the data
    inside the Unreal Engine level.
    """
    print("🌌 Materializing Galaxy Knowledge in 3D Space...")
    
    if not os.path.exists(DB_PATH):
        print(f"❌ Database not found at {DB_PATH}")
        return

    with open(DB_PATH, 'r') as f:
        knowledge_nodes = json.load(f)
        
    ell = unreal.EditorLevelLibrary
    eal = unreal.EditorAssetLibrary
    
    # Anchor point
    center_loc = unreal.Vector(0, 0, 1000)
    radius = 500.0
    
    # Clear previous visualization if any (Basic cleanup by tag/label could be added here)
    # For now, we just spawn new ones.
    
    count = len(knowledge_nodes)
    if count == 0:
        print("Galaxy is empty.")
        return

    # Golden Ratio spiral for galaxy layout
    phi = (1 + math.sqrt(5)) / 2
    
    for i, node in enumerate(knowledge_nodes):
        # Calculate Position (Spiral)
        angle = 2 * math.pi * i / phi
        dist = radius * math.sqrt(i + 1)
        
        x = center_loc.x + dist * math.cos(angle)
        y = center_loc.y + dist * math.sin(angle)
        z = center_loc.z + (i * 50) # Slight spiral upwards
        
        location = unreal.Vector(x, y, z)
        rotation = unreal.Rotator(0, math.degrees(angle) + 90, 0)
        
        # Spawn Text Render Actor for Label
        text_actor = ell.spawn_actor_from_class(unreal.TextRenderActor, location, rotation)
        text_actor.text_render.set_text(node['topic'])
        text_actor.text_render.set_text_render_color(unreal.Color(0, 255, 255, 255))
        text_actor.set_actor_scale3d(unreal.Vector(5, 5, 5))
        text_actor.set_actor_label(f"KnowledgeNode_{i}")
        
        # Spawn Representation Mesh (Sphere/Cube based on Category)
        mesh_actor = ell.spawn_actor_from_class(unreal.StaticMeshActor, location + unreal.Vector(0,0,-50), rotation)
        
        shape_path = "/Engine/BasicShapes/Sphere"
        color_path = "/Game/Nexus/Materials/Neon/M_NeonBlue"
        
        if node['category'] == "Task":
            shape_path = "/Engine/BasicShapes/Cube"
            color_path = "/Game/Nexus/Materials/Neon/M_NeonGold" # Gold for Tasks
        elif node['category'] == "Idea":
            shape_path = "/Engine/BasicShapes/Cone"
            color_path = "/Game/Nexus/Materials/Neon/M_NeonPink" # Pink for Ideas
            
        mesh = eal.load_asset(shape_path)
        mat = eal.load_asset(color_path)
        
        if mesh:
            mesh_actor.static_mesh_component.set_static_mesh(mesh)
        if mat:
            mesh_actor.static_mesh_component.set_material(0, mat)
            
        mesh_actor.set_actor_label(f"KnowledgeOrb_{i}")
        
        # Add metadata tags so we can potentially retrieve content later in Blueprint
        # (Tags are arrays of strings)
        mesh_actor.tags.append(f"Content:{node['content'][:20]}...") # Truncated for tag
        
    print(f"✅ Materialized {count} Knowledge Nodes in the level.")

if __name__ == "__main__":
    visualize_knowledge_galaxy()
