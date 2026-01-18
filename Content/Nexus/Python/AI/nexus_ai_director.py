import unreal
import nexus_sdf_gen
import nexus_ai_material
import random

import nexus_brain_core

def execute_directive(prompt):
    """
    The Central Brain (Upgraded with Real Gemini API).
    """
    unreal.log(f"🧠 Nexus Director Dispatching: '{prompt}'")
    
    # 1. Consult the Brain
    data = nexus_brain_core.BRAIN.think(prompt)
    unreal.log(f"   -> Thought: {data}")
    
    action = data.get("action", "UNKNOWN")
    
    # --- HANDLER: CREATE ---
    if action == "CREATE":
        objects = data.get("objects", [])
        physics = data.get("physics", False)
        
        # The provided snippet seems to be a simplified/alternative creation logic.
        # I will integrate the 'golf'/'fairway' logic into the existing structure.
        
        # If the prompt contains creation keywords, we can infer a shape type
        # This part of the provided snippet seems to be a fallback or simpler intent parsing
        # than the `data.get("objects")` structure.
        # For now, I'll assume the `data` from the brain will provide the `shape` type.
        
        for obj in objects:
            shape = obj.get("type", "cube")
            loc = obj.get("location", [0,0,0])
            col = obj.get("color", [1,1,1])
            
            # Spawn
            # Add 'fairway' to the SDF generation types
            if shape in ["gyroid", "schwarz_p", "fairway"]: # Added 'fairway' here
                 actor = nexus_sdf_gen.create_sdf_actor(obj.get("name", "AI_Gen"), shape, tuple(loc))
                 
                 # Golf Specific: Make it Green if not specified (assuming 'color' in obj is the spec)
                 if shape == "fairway" and not col: # Check if color was explicitly provided by the brain
                     unreal.log(f"   -> Applying default material for fairway.")
                     nexus_ai_material.text_to_material("Rough procedural grass green matte")
            else:
                 actor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.StaticMeshActor, unreal.Vector(*loc), unreal.Rotator(0,0,0))
                 # Simple mesh load logic
                 mesh_path = "/Engine/BasicShapes/Cube.Cube" 
                 if "sphere" in shape: mesh_path = "/Engine/BasicShapes/Sphere.Sphere"
                 actor.static_mesh_component.set_static_mesh(unreal.load_asset(mesh_path))
            
            # Apply Color (Quick Material)
            # In a real impl, we'd call text_to_material with the 'color' description
            
            # Physics
            if physics:
                apply_physics(actor, True)
                
    # --- HANDLER: TRANSLATE ---
    elif action == "TRANSLATE":
        # Just show an alert for now
        txt = data.get("text", "")
        tgt = data.get("target", "English")
        result = nexus_brain_core.BRAIN.translate(txt, tgt)
        unreal.log_warning(f"🗣️ Translation: {result}")
        
    # --- HANDLER: UNKNOWN ---
    else:
        unreal.log("   -> Brain was unsure. Fallback to basic heuristics.")
        # ... (Legacy logic could go here)

def apply_physics(actor, enable=True, restitution=0.5):
    """
    Enables physics simulation on the actor's root component.
    """
    root = actor.root_component
    if isinstance(root, unreal.PrimitiveComponent):
        root.set_simulate_physics(enable)
        if enable:
            # Enable collision if needed
            root.set_collision_enabled(unreal.CollisionEnabled.QUERY_AND_PHYSICS)
            
            # Simple physical material override (Concept)
            # In real code, we'd load a PhysMat asset
            unreal.log(f"   -> Physics Enabled. Restitution: {restitution}")
            
def demo_autopilot():
    """
    Simulates a sequence of complex user commands.
    """
    commands = [
        "Create a huge golden gyroid",
        "Make a bouncy transparent glass sphere",
        "Create a small red cube",
        "Select all and turn on gravity" # Complex selection logic skipped for simplicity
    ]
    
    # Just run one random command for the menu demo
    cmd = random.choice(commands)
    execute_directive(cmd)
    return cmd
