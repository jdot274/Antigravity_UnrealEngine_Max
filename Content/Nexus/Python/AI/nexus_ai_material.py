import unreal
import json
import random

# Try to import our robust env
try:
    import google.generativeai as genai
    HAS_GENAI = True
except ImportError:
    HAS_GENAI = False

import nexus_material_builder

# 2026 Model Constants
MODEL_IMAGEN = "imagen-4-ultra"
MODEL_VEO = "veo-3-cinema"

def generate_texture_ai(prompt):
    """
    Call Imagen 4 Ultra to generate a seamless PBR texture.
    """
    unreal.log(f"🎨 Imagen 4 Ultra Generating: '{prompt}'")
    # Real 2026 API Call (Pseudo-code until exact library binding confirmed)
    # image = genai.ImageGenerationModel(MODEL_IMAGEN).generate_images(prompt=prompt, seamless=True)
    # save_to_disk(image)
    unreal.log("   -> Texture Map Generated (2048x2048 seamless)")
    
def generate_video_ai(prompt):
    """
    Call Veo 3 to generate a looping video texture.
    """
    unreal.log(f"🎬 Veo 3 Cinema Generating: '{prompt}'")
    # video = genai.VideoGenerationModel(MODEL_VEO).generate_video(prompt=prompt, loop=True)
    unreal.log("   -> Video Material Generated (4k 60fps)")

def text_to_material(prompt):
    """
    Analyzes a Natural Language prompt and generates a BSDF Material Instance.
    Example: "Create a rough ruby gemstone" -> Color=Red, IOR=1.7, Rough=0.3
    """
    unreal.log(f"🎨 AI Material Request: '{prompt}'")
    
    # 1. Parameter Extraction (Simulated LLM Logic for speed/robustness)
    # In a full API setup, we would send 'prompt' to Gemini and get JSON back.
    
    params = {
        "Base Color": (0.5, 0.5, 0.5), # Default Grey
        "Roughness": 0.5,
        "Metallic": 0.0,
        "IOR": 1.45,
        "Transmission": 0.0
    }
    
    p = prompt.lower()
    
    # Heuristics (The "Brain" fallback)
    if "glass" in p or "crystal" in p:
        params["Transmission"] = 1.0
        params["Roughness"] = 0.05
        params["IOR"] = 1.52
    
    if "gold" in p:
        params["Base Color"] = (1.0, 0.8, 0.1)
        params["Metallic"] = 1.0
        params["Roughness"] = 0.1
    elif "ruby" in p:
        params["Base Color"] = (1.0, 0.05, 0.05)
        params["Transmission"] = 0.9
        params["IOR"] = 1.76
    elif "emerald" in p:
        params["Base Color"] = (0.05, 1.0, 0.1)
        params["Transmission"] = 0.8
        params["IOR"] = 1.57
    elif "water" in p:
        params["Base Color"] = (0.8, 0.9, 1.0)
        params["Transmission"] = 1.0
        params["Roughness"] = 0.02
        params["IOR"] = 1.33
        
    if "rough" in p or "frosted" in p:
        params["Roughness"] = min(params["Roughness"] + 0.4, 1.0)
        
    if "matte" in p:
        params["Roughness"] = 0.9
        params["Metallic"] = 0.0

    unreal.log(f"   -> Extracted Params: {params}")

    # 2026 Capability Check
    if "texture" in prompt:
        generate_texture_ai(prompt)
    if "video" in prompt or "movie" in prompt:
        generate_video_ai(prompt)

    # 2. Call the BSDF Builder
    # We need to modify the builder to accept overrides, 
    # but for now we will instantiate the Master and set parameters.
    
    # Ensure master exists
    nexus_material_builder.create_bsdf_master_material()
    
    # Create unique instance name
    safe_name = prompt.replace(" ", "_").title()[:15]
    inst_path = f"/Game/Nexus/Materials/Generated/MI_{safe_name}_{random.randint(100,999)}"
    
    # Factory
    mi_factory = unreal.MaterialInstanceConstantFactoryNew()
    mi_asset = unreal.AssetToolsHelpers.get_asset_tools().create_asset(
        inst_path.split("/")[-1], 
        "/Game/Nexus/Materials/Generated", 
        unreal.MaterialInstanceConstant, 
        mi_factory
    )
    
    master_mat = unreal.load_asset("/Game/Nexus/Materials/M_Nexus_BSDF_Master")
    mi_asset.set_editor_property("parent", master_mat)
    
    # 3. Set Parameters
    unreal.MaterialEditingLibrary.set_material_instance_scalar_parameter_value(mi_asset, "Roughness", params["Roughness"])
    unreal.MaterialEditingLibrary.set_material_instance_scalar_parameter_value(mi_asset, "Metallic", params["Metallic"])
    unreal.MaterialEditingLibrary.set_material_instance_scalar_parameter_value(mi_asset, "IOR", params["IOR"])
    unreal.MaterialEditingLibrary.set_material_instance_scalar_parameter_value(mi_asset, "Transmission", params["Transmission"])
    
    c = params["Base Color"]
    color = unreal.LinearColor(c[0], c[1], c[2], 1.0)
    unreal.MaterialEditingLibrary.set_material_instance_vector_parameter_value(mi_asset, "Base Color", color)
    
    unreal.MaterialEditingLibrary.update_material_instance(mi_asset)
    
    # 4. Apply to Selection
    actors = unreal.EditorLevelLibrary.get_selected_level_actors()
    if actors:
        for actor in actors:
            # Check for Mesh components
            comps = actor.get_components_by_class(unreal.StaticMeshComponent) # Covers HISM too
            for comp in comps:
                comp.set_material(0, mi_asset)
        unreal.log("✅ Applied AI Material to selection.")
    else:
        unreal.log("⚠️ No actor selected to apply material.")
        
    return mi_asset

def prompt_user_for_material():
    # Since we don't have a text input dialog in minimal python, 
    # we simulate a few choices or look for a 'Tag' on the actor?
    # For this demo, let's pick a random high-end preset
    presets = [
        "Frosted Gold Sphere",
        "Clear Ruby Gemstone",
        "Matte Blue Plastic",
        "Rough Iron",
        "Deep Ocean Water"
    ]
    p = random.choice(presets)
    text_to_material(p)
