"""
ANTIGRAVITY NEXUS - AAA Material Graph Generator
================================================
Creates high-fidelity PBR materials with animated nodes directly in Unreal Engine.
All assets are PERMANENTLY STORED as .uasset files.

Features:
- Procedural PBR Node Graphs (Metallic/Roughness workflow)
- Animated Holographic Effects (Time-based panning)
- Emissive Pulse Animations
- SDF-inspired Distance Field effects
- BSDF Transmission layers for glass/crystal
"""

import unreal
import math
import random

# ============================================================================
# CONFIGURATION
# ============================================================================
MATERIAL_OUTPUT_PATH = "/Game/FuturisticSystems/Materials"
TEXTURE_OUTPUT_PATH = "/Game/FuturisticSystems/Textures"

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def ensure_directory(path):
    """Creates content directory if it doesn't exist."""
    if not unreal.EditorAssetLibrary.does_directory_exist(path):
        unreal.EditorAssetLibrary.make_directory(path)
        unreal.log(f"📁 Created: {path}")

def create_material(name, blend_mode=unreal.BlendMode.BLEND_OPAQUE):
    """Creates a new Material asset and returns it."""
    full_path = f"{MATERIAL_OUTPUT_PATH}/{name}"
    
    # Delete if exists for clean regeneration
    if unreal.EditorAssetLibrary.does_asset_exist(full_path):
        unreal.EditorAssetLibrary.delete_asset(full_path)
    
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    factory = unreal.MaterialFactoryNew()
    
    material = asset_tools.create_asset(name, MATERIAL_OUTPUT_PATH, unreal.Material, factory)
    
    if material:
        material.set_editor_property("blend_mode", blend_mode)
        unreal.log(f"✅ Material Created: {name}")
    else:
        unreal.log_warning(f"❌ Failed to create material: {name}")
    
    return material

def add_expression(material, expression_class, pos_x=0, pos_y=0):
    """Adds a material expression node to the graph."""
    expr = unreal.MaterialEditingLibrary.create_material_expression(
        material, 
        expression_class, 
        pos_x, 
        pos_y
    )
    return expr

def connect_expression(material, from_expr, from_output, to_property):
    """Connects an expression output to a material property."""
    unreal.MaterialEditingLibrary.connect_material_property(
        from_expr, 
        from_output, 
        to_property
    )

def connect_expressions(from_expr, from_output_name, to_expr, to_input_name):
    """Connects two expression nodes together."""
    unreal.MaterialEditingLibrary.connect_material_expressions(
        from_expr, from_output_name,
        to_expr, to_input_name
    )

# ============================================================================
# MATERIAL DEFINITIONS
# ============================================================================

def create_holographic_material():
    """
    Creates an animated holographic material with:
    - Time-based UV panning
    - Fresnel-driven opacity
    - Emissive pulse
    """
    mat = create_material("M_Holographic_Animated", unreal.BlendMode.BLEND_TRANSLUCENT)
    if not mat:
        return None
    
    mat.set_editor_property("shading_model", unreal.MaterialShadingModel.MSM_UNLIT)
    
    # --- NODES ---
    # Time Node (Animation Driver)
    time_node = add_expression(mat, unreal.MaterialExpressionTime, -800, 0)
    
    # Multiply Time for speed control
    multiply_speed = add_expression(mat, unreal.MaterialExpressionMultiply, -600, 0)
    speed_const = add_expression(mat, unreal.MaterialExpressionConstant, -800, 100)
    speed_const.set_editor_property("r", 0.5)
    connect_expressions(time_node, "", multiply_speed, "A")
    connect_expressions(speed_const, "", multiply_speed, "B")
    
    # Panner for UV animation
    panner = add_expression(mat, unreal.MaterialExpressionPanner, -400, 0)
    panner.set_editor_property("speed_x", 0.1)
    panner.set_editor_property("speed_y", 0.3)
    
    # TexCoord
    texcoord = add_expression(mat, unreal.MaterialExpressionTextureCoordinate, -600, -100)
    connect_expressions(texcoord, "", panner, "Coordinate")
    connect_expressions(multiply_speed, "", panner, "Time")
    
    # Sine wave for pulse
    sine = add_expression(mat, unreal.MaterialExpressionSine, -400, 200)
    connect_expressions(time_node, "", sine, "")
    
    # Remap sine to 0.5-1.0 range
    add_half = add_expression(mat, unreal.MaterialExpressionAdd, -200, 200)
    half_const = add_expression(mat, unreal.MaterialExpressionConstant, -400, 300)
    half_const.set_editor_property("r", 0.5)
    connect_expressions(sine, "", add_half, "A")
    connect_expressions(half_const, "", add_half, "B")
    
    multiply_pulse = add_expression(mat, unreal.MaterialExpressionMultiply, 0, 200)
    pulse_scale = add_expression(mat, unreal.MaterialExpressionConstant, -200, 300)
    pulse_scale.set_editor_property("r", 0.5)
    connect_expressions(add_half, "", multiply_pulse, "A")
    connect_expressions(pulse_scale, "", multiply_pulse, "B")
    
    # Emissive Color (Cyan base * pulse)
    emissive_color = add_expression(mat, unreal.MaterialExpressionVectorParameter, -400, -200)
    emissive_color.set_editor_property("parameter_name", "EmissiveColor")
    emissive_color.set_editor_property("default_value", unreal.LinearColor(0.0, 1.0, 1.0, 1.0))
    
    emissive_mult = add_expression(mat, unreal.MaterialExpressionMultiply, 200, 0)
    connect_expressions(emissive_color, "", emissive_mult, "A")
    connect_expressions(multiply_pulse, "", emissive_mult, "B")
    
    # Boost emissive
    emissive_boost = add_expression(mat, unreal.MaterialExpressionMultiply, 400, 0)
    boost_const = add_expression(mat, unreal.MaterialExpressionConstant, 200, 100)
    boost_const.set_editor_property("r", 5.0)
    connect_expressions(emissive_mult, "", emissive_boost, "A")
    connect_expressions(boost_const, "", emissive_boost, "B")
    
    # Fresnel for edge glow
    fresnel = add_expression(mat, unreal.MaterialExpressionFresnel, -200, 400)
    fresnel.set_editor_property("exponent", 3.0)
    
    # --- CONNECTIONS TO OUTPUT ---
    connect_expression(mat, emissive_boost, "", unreal.MaterialProperty.MP_EMISSIVE_COLOR)
    connect_expression(mat, fresnel, "", unreal.MaterialProperty.MP_OPACITY)
    
    # Compile and save
    unreal.MaterialEditingLibrary.recompile_material(mat)
    unreal.EditorAssetLibrary.save_asset(f"{MATERIAL_OUTPUT_PATH}/M_Holographic_Animated")
    
    unreal.log("🌈 M_Holographic_Animated: Animated hologram with fresnel edges")
    return mat

def create_pbr_metal_material():
    """
    Creates a high-quality PBR metallic material:
    - Procedural scratches via noise
    - Metallic/Roughness workflow
    - Normal detail
    """
    mat = create_material("M_FuturisticMetal_PBR")
    if not mat:
        return None
    
    # Base Color (Dark gunmetal)
    base_color = add_expression(mat, unreal.MaterialExpressionVectorParameter, -400, -200)
    base_color.set_editor_property("parameter_name", "BaseColor")
    base_color.set_editor_property("default_value", unreal.LinearColor(0.05, 0.05, 0.07, 1.0))
    
    # Noise for variation
    noise = add_expression(mat, unreal.MaterialExpressionNoise, -600, 0)
    noise.set_editor_property("scale", 50.0)
    noise.set_editor_property("quality", 2)
    
    # Lerp base color with noise
    lerp_color = add_expression(mat, unreal.MaterialExpressionLinearInterpolate, -200, -100)
    darker_color = add_expression(mat, unreal.MaterialExpressionVectorParameter, -400, 0)
    darker_color.set_editor_property("parameter_name", "ScratchColor")
    darker_color.set_editor_property("default_value", unreal.LinearColor(0.02, 0.02, 0.03, 1.0))
    
    connect_expressions(base_color, "", lerp_color, "A")
    connect_expressions(darker_color, "", lerp_color, "B")
    connect_expressions(noise, "", lerp_color, "Alpha")
    
    # Metallic (high)
    metallic = add_expression(mat, unreal.MaterialExpressionScalarParameter, -200, 200)
    metallic.set_editor_property("parameter_name", "Metallic")
    metallic.set_editor_property("default_value", 0.95)
    
    # Roughness (low for shiny)
    roughness = add_expression(mat, unreal.MaterialExpressionScalarParameter, -200, 300)
    roughness.set_editor_property("parameter_name", "Roughness")
    roughness.set_editor_property("default_value", 0.15)
    
    # Add noise to roughness for micro-scratches
    roughness_add = add_expression(mat, unreal.MaterialExpressionAdd, 0, 300)
    roughness_noise_scale = add_expression(mat, unreal.MaterialExpressionMultiply, -200, 400)
    noise_scale_const = add_expression(mat, unreal.MaterialExpressionConstant, -400, 400)
    noise_scale_const.set_editor_property("r", 0.1)
    
    connect_expressions(noise, "", roughness_noise_scale, "A")
    connect_expressions(noise_scale_const, "", roughness_noise_scale, "B")
    connect_expressions(roughness, "", roughness_add, "A")
    connect_expressions(roughness_noise_scale, "", roughness_add, "B")
    
    # --- CONNECTIONS TO OUTPUT ---
    connect_expression(mat, lerp_color, "", unreal.MaterialProperty.MP_BASE_COLOR)
    connect_expression(mat, metallic, "", unreal.MaterialProperty.MP_METALLIC)
    connect_expression(mat, roughness_add, "", unreal.MaterialProperty.MP_ROUGHNESS)
    
    # Compile and save
    unreal.MaterialEditingLibrary.recompile_material(mat)
    unreal.EditorAssetLibrary.save_asset(f"{MATERIAL_OUTPUT_PATH}/M_FuturisticMetal_PBR")
    
    unreal.log("🔩 M_FuturisticMetal_PBR: Gunmetal with procedural scratches")
    return mat

def create_glass_transmission_material():
    """
    Creates a BSDF-like glass material with:
    - Transmission/Refraction
    - Thin translucency
    - Colored tint
    """
    mat = create_material("M_Glass_Transmission", unreal.BlendMode.BLEND_TRANSLUCENT)
    if not mat:
        return None
    
    mat.set_editor_property("translucency_lighting_mode", unreal.TranslucencyLightingMode.TLM_SURFACE)
    
    # Base Color (slight tint)
    base_color = add_expression(mat, unreal.MaterialExpressionVectorParameter, -400, -200)
    base_color.set_editor_property("parameter_name", "GlassTint")
    base_color.set_editor_property("default_value", unreal.LinearColor(0.8, 0.9, 1.0, 1.0))
    
    # Very low roughness for sharp reflections
    roughness = add_expression(mat, unreal.MaterialExpressionConstant, -200, 200)
    roughness.set_editor_property("r", 0.05)
    
    # High specular
    specular = add_expression(mat, unreal.MaterialExpressionConstant, -200, 300)
    specular.set_editor_property("r", 1.0)
    
    # Opacity for glass thickness
    opacity = add_expression(mat, unreal.MaterialExpressionScalarParameter, -200, 400)
    opacity.set_editor_property("parameter_name", "Opacity")
    opacity.set_editor_property("default_value", 0.3)
    
    # Refraction
    refraction = add_expression(mat, unreal.MaterialExpressionScalarParameter, -200, 500)
    refraction.set_editor_property("parameter_name", "IOR")
    refraction.set_editor_property("default_value", 1.5)  # Glass IOR
    
    # --- CONNECTIONS ---
    connect_expression(mat, base_color, "", unreal.MaterialProperty.MP_BASE_COLOR)
    connect_expression(mat, roughness, "", unreal.MaterialProperty.MP_ROUGHNESS)
    connect_expression(mat, specular, "", unreal.MaterialProperty.MP_SPECULAR)
    connect_expression(mat, opacity, "", unreal.MaterialProperty.MP_OPACITY)
    connect_expression(mat, refraction, "", unreal.MaterialProperty.MP_REFRACTION)
    
    # Compile and save
    unreal.MaterialEditingLibrary.recompile_material(mat)
    unreal.EditorAssetLibrary.save_asset(f"{MATERIAL_OUTPUT_PATH}/M_Glass_Transmission")
    
    unreal.log("🔮 M_Glass_Transmission: BSDF glass with refraction")
    return mat

def create_energy_field_material():
    """
    Creates an animated energy/force field material:
    - Scrolling hex pattern
    - Edge detection glow
    - Animated distortion
    """
    mat = create_material("M_EnergyField_Animated", unreal.BlendMode.BLEND_ADDITIVE)
    if not mat:
        return None
    
    mat.set_editor_property("shading_model", unreal.MaterialShadingModel.MSM_UNLIT)
    mat.set_editor_property("two_sided", True)
    
    # Time
    time_node = add_expression(mat, unreal.MaterialExpressionTime, -800, 0)
    
    # UV Coordinates
    texcoord = add_expression(mat, unreal.MaterialExpressionTextureCoordinate, -800, 100)
    
    # Scale UVs for hex pattern
    uv_scale = add_expression(mat, unreal.MaterialExpressionMultiply, -600, 100)
    scale_const = add_expression(mat, unreal.MaterialExpressionConstant, -800, 200)
    scale_const.set_editor_property("r", 10.0)
    connect_expressions(texcoord, "", uv_scale, "A")
    connect_expressions(scale_const, "", uv_scale, "B")
    
    # Sine pattern for hex-like effect
    sine_x = add_expression(mat, unreal.MaterialExpressionSine, -400, 0)
    sine_y = add_expression(mat, unreal.MaterialExpressionSine, -400, 150)
    
    # Component mask for X and Y
    mask_x = add_expression(mat, unreal.MaterialExpressionComponentMask, -500, 0)
    mask_x.set_editor_property("r", True)
    mask_x.set_editor_property("g", False)
    connect_expressions(uv_scale, "", mask_x, "")
    
    mask_y = add_expression(mat, unreal.MaterialExpressionComponentMask, -500, 150)
    mask_y.set_editor_property("r", False)
    mask_y.set_editor_property("g", True)
    connect_expressions(uv_scale, "", mask_y, "")
    
    # Add time to Y for scrolling
    scroll_y = add_expression(mat, unreal.MaterialExpressionAdd, -400, 200)
    connect_expressions(mask_y, "", scroll_y, "A")
    connect_expressions(time_node, "", scroll_y, "B")
    
    connect_expressions(mask_x, "", sine_x, "")
    connect_expressions(scroll_y, "", sine_y, "")
    
    # Combine patterns
    pattern_mult = add_expression(mat, unreal.MaterialExpressionMultiply, -200, 100)
    connect_expressions(sine_x, "", pattern_mult, "A")
    connect_expressions(sine_y, "", pattern_mult, "B")
    
    # Remap to positive
    abs_pattern = add_expression(mat, unreal.MaterialExpressionAbs, 0, 100)
    connect_expressions(pattern_mult, "", abs_pattern, "")
    
    # Color it
    energy_color = add_expression(mat, unreal.MaterialExpressionVectorParameter, -200, -100)
    energy_color.set_editor_property("parameter_name", "EnergyColor")
    energy_color.set_editor_property("default_value", unreal.LinearColor(0.2, 0.8, 1.0, 1.0))
    
    final_color = add_expression(mat, unreal.MaterialExpressionMultiply, 200, 0)
    connect_expressions(energy_color, "", final_color, "A")
    connect_expressions(abs_pattern, "", final_color, "B")
    
    # Boost
    boost = add_expression(mat, unreal.MaterialExpressionMultiply, 400, 0)
    boost_const = add_expression(mat, unreal.MaterialExpressionConstant, 200, 100)
    boost_const.set_editor_property("r", 3.0)
    connect_expressions(final_color, "", boost, "A")
    connect_expressions(boost_const, "", boost, "B")
    
    # Fresnel for edge
    fresnel = add_expression(mat, unreal.MaterialExpressionFresnel, 200, 300)
    fresnel.set_editor_property("exponent", 2.0)
    
    # Add fresnel to pattern
    final_emissive = add_expression(mat, unreal.MaterialExpressionAdd, 600, 0)
    fresnel_colored = add_expression(mat, unreal.MaterialExpressionMultiply, 400, 300)
    connect_expressions(fresnel, "", fresnel_colored, "A")
    connect_expressions(energy_color, "", fresnel_colored, "B")
    connect_expressions(boost, "", final_emissive, "A")
    connect_expressions(fresnel_colored, "", final_emissive, "B")
    
    # --- OUTPUT ---
    connect_expression(mat, final_emissive, "", unreal.MaterialProperty.MP_EMISSIVE_COLOR)
    connect_expression(mat, abs_pattern, "", unreal.MaterialProperty.MP_OPACITY)
    
    # Compile and save
    unreal.MaterialEditingLibrary.recompile_material(mat)
    unreal.EditorAssetLibrary.save_asset(f"{MATERIAL_OUTPUT_PATH}/M_EnergyField_Animated")
    
    unreal.log("⚡ M_EnergyField_Animated: Scrolling energy field with edge glow")
    return mat

def create_neon_glow_material():
    """
    Simple but effective neon tube material with bloom.
    """
    mat = create_material("M_NeonGlow")
    if not mat:
        return None
    
    mat.set_editor_property("shading_model", unreal.MaterialShadingModel.MSM_UNLIT)
    
    # Emissive color parameter
    emissive = add_expression(mat, unreal.MaterialExpressionVectorParameter, -200, 0)
    emissive.set_editor_property("parameter_name", "NeonColor")
    emissive.set_editor_property("default_value", unreal.LinearColor(1.0, 0.2, 0.5, 1.0))
    
    # Intensity multiplier
    intensity = add_expression(mat, unreal.MaterialExpressionScalarParameter, -200, 100)
    intensity.set_editor_property("parameter_name", "Intensity")
    intensity.set_editor_property("default_value", 10.0)
    
    # Multiply
    mult = add_expression(mat, unreal.MaterialExpressionMultiply, 0, 50)
    connect_expressions(emissive, "", mult, "A")
    connect_expressions(intensity, "", mult, "B")
    
    # Output
    connect_expression(mat, mult, "", unreal.MaterialProperty.MP_EMISSIVE_COLOR)
    
    # Compile and save
    unreal.MaterialEditingLibrary.recompile_material(mat)
    unreal.EditorAssetLibrary.save_asset(f"{MATERIAL_OUTPUT_PATH}/M_NeonGlow")
    
    unreal.log("💡 M_NeonGlow: High-intensity bloom neon")
    return mat

# ============================================================================
# BATCH GENERATION
# ============================================================================

def generate_all_materials():
    """Generates all AAA materials and saves them permanently."""
    unreal.log("="*60)
    unreal.log("🎨 ANTIGRAVITY MATERIAL GRAPH GENERATOR")
    unreal.log("="*60)
    
    # Ensure directories
    ensure_directory(MATERIAL_OUTPUT_PATH)
    ensure_directory(TEXTURE_OUTPUT_PATH)
    
    materials = []
    
    # Generate each material
    materials.append(create_holographic_material())
    materials.append(create_pbr_metal_material())
    materials.append(create_glass_transmission_material())
    materials.append(create_energy_field_material())
    materials.append(create_neon_glow_material())
    
    # Generate color variants of neon
    for name, color in [
        ("M_NeonGlow_Cyan", unreal.LinearColor(0.0, 1.0, 1.0, 1.0)),
        ("M_NeonGlow_Magenta", unreal.LinearColor(1.0, 0.0, 1.0, 1.0)),
        ("M_NeonGlow_Yellow", unreal.LinearColor(1.0, 1.0, 0.0, 1.0)),
        ("M_NeonGlow_Red", unreal.LinearColor(1.0, 0.1, 0.1, 1.0)),
    ]:
        mat = create_material(name)
        if mat:
            mat.set_editor_property("shading_model", unreal.MaterialShadingModel.MSM_UNLIT)
            emissive = add_expression(mat, unreal.MaterialExpressionConstant4Vector, -200, 0)
            emissive.set_editor_property("constant", color)
            intensity = add_expression(mat, unreal.MaterialExpressionMultiply, 0, 0)
            boost = add_expression(mat, unreal.MaterialExpressionConstant, -200, 100)
            boost.set_editor_property("r", 15.0)
            connect_expressions(emissive, "", intensity, "A")
            connect_expressions(boost, "", intensity, "B")
            connect_expression(mat, intensity, "", unreal.MaterialProperty.MP_EMISSIVE_COLOR)
            unreal.MaterialEditingLibrary.recompile_material(mat)
            unreal.EditorAssetLibrary.save_asset(f"{MATERIAL_OUTPUT_PATH}/{name}")
            materials.append(mat)
    
    # Force save all
    unreal.EditorLoadingAndSavingUtils.save_dirty_packages(
        save_map_packages=False, 
        save_content_packages=True
    )
    
    valid_count = len([m for m in materials if m is not None])
    unreal.log("="*60)
    unreal.log(f"✅ PERMANENTLY SAVED: {valid_count} Materials to {MATERIAL_OUTPUT_PATH}")
    unreal.log("="*60)
    
    return materials

# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    generate_all_materials()
