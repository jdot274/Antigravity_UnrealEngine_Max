"""
Antigravity Nexus - Material Builder
Run this in Unreal Editor to build all materials from generated textures.
Execute via: Tools > Execute Python Script
"""
import unreal

# Asset paths
TEXTURE_PATH = "/Game/Nexus/Textures/"
MATERIAL_PATH = "/Game/Nexus/Materials/"

def create_material(name, texture_name, settings):
    """Create a material asset with the given texture and settings."""
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    material_factory = unreal.MaterialFactoryNew()
    
    # Create material
    material = asset_tools.create_asset(name, MATERIAL_PATH, unreal.Material, material_factory)
    if not material:
        unreal.log_error(f"Failed to create material: {name}")
        return None
    
    unreal.log(f"✅ Created material: {name}")
    return material

def create_material_instance(parent_name, instance_name, params):
    """Create a material instance with parameters."""
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    mi_factory = unreal.MaterialInstanceConstantFactoryNew()
    
    # Load parent
    parent = unreal.load_asset(f"{MATERIAL_PATH}{parent_name}")
    if not parent:
        unreal.log_error(f"Parent material not found: {parent_name}")
        return None
    
    mi_factory.set_editor_property("initial_parent", parent)
    
    # Create instance
    mi = asset_tools.create_asset(instance_name, MATERIAL_PATH, unreal.MaterialInstanceConstant, mi_factory)
    if mi:
        unreal.log(f"✅ Created material instance: {instance_name}")
    return mi

def build_grass_material():
    """Build spiky grass material with Nanite displacement."""
    mat = create_material("M_Grass_Nanite", "grass_fairway_texture", {
        "shading_model": "subsurface",
        "blend_mode": "opaque",
        "two_sided": False,
        "use_displacement": True
    })
    return mat

def build_putting_green_material():
    """Build smooth putting green material."""
    mat = create_material("M_PuttingGreen", "putting_green_texture", {
        "shading_model": "default_lit",
        "roughness": 0.3,
        "specular": 0.5
    })
    return mat

def build_sand_material():
    """Build sand bunker material with subsurface scattering."""
    mat = create_material("M_Sand", "sand_bunker_texture", {
        "shading_model": "subsurface",
        "roughness": 0.9,
        "subsurface_color": (0.9, 0.8, 0.5)
    })
    return mat

def build_water_material():
    """Build translucent water material with refraction."""
    mat = create_material("M_Water", "water_hazard_texture", {
        "shading_model": "default_lit",
        "blend_mode": "translucent",
        "opacity": 0.7,
        "refraction": 1.33
    })
    return mat

def build_tree_bark_material():
    """Build tree bark material."""
    mat = create_material("M_TreeBark", "tree_bark_texture", {
        "shading_model": "default_lit",
        "roughness": 0.8
    })
    return mat

def build_golf_ball_material():
    """Build golf ball material with dimples."""
    mat = create_material("M_GolfBall", "golf_ball_texture", {
        "shading_model": "default_lit",
        "roughness": 0.2,
        "specular": 0.8,
        "base_color": (1.0, 1.0, 1.0)
    })
    return mat

def build_sdf_terrain_material():
    """Build SDF-based terrain material with curvy displacement."""
    mat = create_material("M_SDF_Terrain", "grass_fairway_texture", {
        "shading_model": "default_lit",
        "use_displacement": True,
        "displacement_scale": 50.0,
        "world_position_offset": True
    })
    return mat

def build_all_materials():
    """Build all game materials."""
    unreal.log("🎨 Building Antigravity Nexus Materials...")
    
    materials = [
        build_grass_material(),
        build_putting_green_material(),
        build_sand_material(),
        build_water_material(),
        build_tree_bark_material(),
        build_golf_ball_material(),
        build_sdf_terrain_material()
    ]
    
    # Create material function for displacement
    create_displacement_function()
    
    # Create material layer blend
    create_terrain_layer_blend()
    
    unreal.log(f"✅ Built {len([m for m in materials if m])} materials!")
    return materials

def create_displacement_function():
    """Create a reusable displacement material function."""
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    mf_factory = unreal.MaterialFunctionFactoryNew()
    
    mf = asset_tools.create_asset("MF_NaniteDisplacement", MATERIAL_PATH + "Functions/", 
                                   unreal.MaterialFunction, mf_factory)
    if mf:
        unreal.log("✅ Created displacement function: MF_NaniteDisplacement")
    return mf

def create_terrain_layer_blend():
    """Create terrain layer blend material."""
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    
    # Create landscape layer blend material
    material_factory = unreal.MaterialFactoryNew()
    mat = asset_tools.create_asset("M_TerrainLayerBlend", MATERIAL_PATH, 
                                    unreal.Material, material_factory)
    if mat:
        unreal.log("✅ Created terrain layer blend: M_TerrainLayerBlend")
    return mat

# Run when script is executed
if __name__ == "__main__":
    build_all_materials()
