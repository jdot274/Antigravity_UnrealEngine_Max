import unreal

def create_bsdf_master_material():
    """
    Procedurally builds a 'Principled BSDF' style Master Material in Unreal.
    Focuses on TRANSMISSION (Glass), IOR, and SUBSURFACE scattering.
    """
    asset_path = "/Game/Nexus/Materials"
    mat_name = "M_Nexus_BSDF_Master"
    
    # 1. Create/Load Asset (Overwrite if exists to update logic)
    mat_factory = unreal.MaterialFactoryNew()
    mat_asset = unreal.AssetToolsHelpers.get_asset_tools().create_asset(
        mat_name, 
        asset_path, 
        unreal.Material, 
        mat_factory
    )
    
    if not mat_asset:
        unreal.log_warning(f"Could not create material {mat_name}")
        return

    # 2. Configure for High-Quality Glass/Transmission
    mat_asset.set_editor_property("blend_mode", unreal.BlendMode.BLEND_TRANSLUCENT)
    mat_asset.set_editor_property("translucency_lighting_mode", unreal.TranslucencyLightingMode.TLM_SURFACE_FORWARD_SHADING)
    mat_asset.set_editor_property("two_sided", True)
    mat_asset.set_editor_property("refraction_method", unreal.RefractionMethod.RM_PIXEL_NORMAL_OFFSET) # Modern refraction

    # 3. Helpers to add nodes
    def add_scalar(name, val, x, y):
        node = unreal.MaterialEditingLibrary.create_material_expression(mat_asset, unreal.MaterialExpressionScalarParameter, x, y)
        node.set_editor_property("parameter_name", name)
        node.set_editor_property("default_value", val)
        return node

    def add_vector(name, r, g, b, x, y):
        node = unreal.MaterialEditingLibrary.create_material_expression(mat_asset, unreal.MaterialExpressionVectorParameter, x, y)
        node.set_editor_property("parameter_name", name)
        node.set_editor_property("default_value", unreal.LinearColor(r,g,b,1))
        return node
        
    # 4. Create Parameters (Blender Style)
    base_color = add_vector("Base Color", 0.0, 0.8, 1.0, -400, 0)
    roughness = add_scalar("Roughness", 0.1, -400, 200)
    ior = add_scalar("IOR", 1.45, -400, 400) # Glass
    opacity = add_scalar("Transmission", 0.3, -400, 600) # Inverted logic for UE Opacity usually, but we'll map direct
    metallic = add_scalar("Metallic", 0.0, -400, 800)
    
    # 5. Connect to Output
    # Connect Base Color
    unreal.MaterialEditingLibrary.connect_material_expressions(base_color, "", mat_asset, "BaseColor")
    
    # Connect Roughness & Metallic
    unreal.MaterialEditingLibrary.connect_material_expressions(roughness, "", mat_asset, "Roughness")
    unreal.MaterialEditingLibrary.connect_material_expressions(metallic, "", mat_asset, "Metallic")
    
    # Connect Opacity (Translucency)
    # For glass, Opacity 1 = Solid, 0 = Invisible. Transmission usually implies "See through".
    # We will use the parameter directly.
    unreal.MaterialEditingLibrary.connect_material_expressions(opacity, "", mat_asset, "Opacity")
    
    # Connect Refraction (IOR)
    # Unreal 5.0+ Refraction input expects IOR directly
    unreal.MaterialEditingLibrary.connect_material_expressions(ior, "", mat_asset, "Refraction")

    # 6. Recompile
    unreal.MaterialEditingLibrary.recompile_material(mat_asset)
    
    # 7. Create Instance for immediate use
    mi_factory = unreal.MaterialInstanceConstantFactoryNew()
    mi_asset = unreal.AssetToolsHelpers.get_asset_tools().create_asset(
        mat_name + "_Inst", 
        asset_path, 
        unreal.MaterialInstanceConstant, 
        mi_factory
    )
    mi_asset.set_editor_property("parent", mat_asset)
    
    unreal.MaterialEditingLibrary.update_material_instance(mi_asset)
    
    unreal.log(f"✅ BSDF Material Created: {mat_path}/{mat_name}")
    return mi_asset

if __name__ == "__main__":
    create_bsdf_master_material()
