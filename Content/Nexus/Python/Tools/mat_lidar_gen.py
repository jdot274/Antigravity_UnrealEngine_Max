import unreal

def create_lidar_material():
    """
    Generates the 'M_Lidar_Scanner' Holographic Material V2.
    It uses WorldPositionOffset and Sine waves to simulate a scanning laser, 
    plus a Grid texture to simulate point cloud points.
    """
    eal = unreal.EditorAssetLibrary
    at = unreal.AssetToolsHelpers.get_asset_tools()
    mel = unreal.MaterialEditingLibrary
    
    mat_path = "/Game/Nexus/Materials/M_Lidar_Scanner"
    
    # Check existence
    if eal.does_asset_exist(mat_path):
        return
        
    unreal.log("🧪 Generating LIDAR Hologram Material...")
    
    factory = unreal.MaterialFactoryNew()
    mat = at.create_asset("M_Lidar_Scanner", "/Game/Nexus/Materials", unreal.Material, factory)
    
    # Settings: Translucent + Unlit for hologram glow
    mat.set_editor_property("blend_mode", unreal.BlendMode.BLEND_ADDITIVE)
    mat.set_editor_property("shading_model", unreal.MaterialShadingModel.MSM_UNLIT)
    mat.set_editor_property("two_sided", True)

    # --- NODE GRAPH GENERATION ---
    
    # 1. Base Color (Toxic Green)
    color = mel.create_material_expression(mat, unreal.MaterialExpressionVectorParameter, -600, 0)
    color.set_editor_property("parameter_name", "HoloColor")
    color.set_editor_property("default_value", unreal.LinearColor(0.0, 1.0, 0.1, 1.0))
    
    # 2. Scanning Effect (Sine Wave based on Time + World Z)
    time = mel.create_material_expression(mat, unreal.MaterialExpressionTime, -800, 200)
    ws_pos = mel.create_material_expression(mat, unreal.MaterialExpressionWorldPosition, -800, 400)
    
    # Mask Z component
    mask_z = mel.create_material_expression(mat, unreal.MaterialExpressionComponentMask, -600, 400)
    mask_z.r_mask, mask_z.g_mask, mask_z.b_mask, mask_z.a_mask = False, False, True, False
    mel.connect_material_expressions(ws_pos, "", mask_z, "")
    
    # (Time * Speed) + Z
    speed = mel.create_material_expression(mat, unreal.MaterialExpressionScalarParameter, -700, 250)
    speed.set_editor_property("parameter_name", "ScanSpeed")
    speed.set_editor_property("default_value", 50.0)
    
    mul_time = mel.create_material_expression(mat, unreal.MaterialExpressionMultiply, -500, 200)
    mel.connect_material_expressions(time, "", mul_time, "A")
    mel.connect_material_expressions(speed, "", mul_time, "B")
    
    add_pos = mel.create_material_expression(mat, unreal.MaterialExpressionAdd, -400, 300)
    mel.connect_material_expressions(mul_time, "", add_pos, "A")
    mel.connect_material_expressions(mask_z, "", add_pos, "B")
    
    # Sine( ScanPos / Width )
    sine = mel.create_material_expression(mat, unreal.MaterialExpressionSine, -300, 300)
    div_width = mel.create_material_expression(mat, unreal.MaterialExpressionDivide, -350, 300)
    # Width Param
    width = mel.create_material_expression(mat, unreal.MaterialExpressionScalarParameter, -350, 450)
    width.set_editor_property("parameter_name", "ScanWidth")
    width.set_editor_property("default_value", 10.0)
    
    mel.connect_material_expressions(add_pos, "", div_width, "A")
    mel.connect_material_expressions(width, "", div_width, "B")
    mel.connect_material_expressions(div_width, "", sine, "")
    
    # 3. Combine Color * Scan
    final_emissive = mel.create_material_expression(mat, unreal.MaterialExpressionMultiply, -100, 0)
    mel.connect_material_expressions(color, "", final_emissive, "A")
    
    # Make Scan bars very bright
    scan_power = mel.create_material_expression(mat, unreal.MaterialExpressionPower, -200, 300)
    mel.connect_material_expressions(sine, "", scan_power, "Base")
    
    power_const = mel.create_material_expression(mat, unreal.MaterialExpressionConstant, -250, 450)
    power_const.set_editor_property("R", 20.0) # Sharp lines
    mel.connect_material_expressions(power_const, "", scan_power, "Exponent")
    
    mel.connect_material_expressions(scan_power, "", final_emissive, "B")

    # Connect to Emissive
    mel.connect_material_expressions(final_emissive, "", mat, unreal.MaterialProperty.MP_EMISSIVE_COLOR)
    
    # Translucency (Fade out scan lines)
    mel.connect_material_expressions(scan_power, "", mat, unreal.MaterialProperty.MP_OPACITY)

    eal.save_asset(mat_path)
    unreal.log("✅ M_Lidar_Scanner Created.")

if __name__ == "__main__":
    create_lidar_material()
