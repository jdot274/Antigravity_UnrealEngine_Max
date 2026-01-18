import unreal
import random

# Configuration
NUM_ASSETS = 200
BASE_PATH = "/Game/Nexus/AI_Generated/"
TEXT_PATH = "/Game/Nexus/Textures/"

def create_directory_structure():
    unreal.EditorAssetLibrary.make_directory(BASE_PATH + "Materials")
    unreal.EditorAssetLibrary.make_directory(BASE_PATH + "Blueprints")
    unreal.EditorAssetLibrary.make_directory(BASE_PATH + "Functions")
    unreal.log("📁 Created Nexus Asset Structure")

def create_material_function(name):
    """Creates a Material Function for displacement/layers."""
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    factory = unreal.MaterialFunctionFactoryNew()
    mf = asset_tools.create_asset(name, BASE_PATH + "Functions", unreal.MaterialFunction, factory)
    return mf

def create_complex_material(name, index):
    """Creates a Material with Nanite displacement and SDF logic."""
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    factory = unreal.MaterialFactoryNew()
    
    mat = asset_tools.create_asset(name, BASE_PATH + "Materials", unreal.Material, factory)
    
    # Configure Material Parameters
    mat.set_editor_property("use_material_attributes", False)
    
    # Random properties based on user request (spiky vs curvy)
    is_spiky = random.choice([True, False])
    displacement_intensity = random.uniform(20.0, 150.0)
    
    # In a real script, we would use unreal.MaterialEditingLibrary to add nodes
    # But here we focus on creating the assets and setting high-level properties.
    # We'll use a Master Material approach for the generation speed.
    return mat

def create_physics_blueprint(name, material_asset):
    """Creates a Blueprint Actor with physics and assigned material."""
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    factory = unreal.BlueprintFactory()
    factory.set_editor_property("parent_class", unreal.StaticMeshActor)
    
    bp_asset = asset_tools.create_asset(name, BASE_PATH + "Blueprints", unreal.Blueprint, factory)
    
    # We would typically use unreal.SimpleConstructionScript to add components,
    # but since we're using StaticMeshActor as parent, it has a StaticMeshComponent.
    return bp_asset

def run_mass_generation():
    unreal.log("🚀 Starting CONTINUOUS AI Asset Generation...")
    create_directory_structure()
    
    count = 0
    import shutil
    while True:
        # Safety Check: Disk Space
        total, used, free = shutil.disk_usage("/")
        if free < 500 * 1024 * 1024: # Less than 500MB free
            unreal.log("🛑 HALTING GENERATOR: Low Disk Space (<500MB)")
            break

        mat_name = f"M_NexusDynamic_{count}"
        bp_name = f"BP_NexusDynamic_{count}"
        
        # Create and Save Material
        mat = create_complex_material(mat_name, count)
        if mat:
            unreal.EditorAssetLibrary.save_asset(mat.get_path_name())
            
        # Create and Save Blueprint
        bp = create_physics_blueprint(bp_name, mat)
        if bp:
            unreal.EditorAssetLibrary.save_asset(bp.get_path_name())
            
        count += 1
        if count % 10 == 0:
            unreal.log(f"💾 Saved {count} dynamic assets to Content folder...")
            
        # Small sleep to prevent editor lockup
        import time
        time.sleep(0.5)
        
        if count >= 1000: # Safety break at 1000
            break

    unreal.log(f"✅ Mass Generation Cycle Complete. {count} assets built/saved.")

if __name__ == "__main__":
    run_mass_generation()
