import unreal
import json
import random

# User Preferences Path
PREF_PATH = "/Users/joeywalter/antigravity-nexus/shader_overlay/preferences.json"

class NexusOracle:
    """
    The 'Asset Oracle' Plugin.
    Guesses what the user wants to build based on 'Tech Awesome' profiles.
    """
    
    @staticmethod
    def consult_oracle():
        """
        Reads user preferences and generates a random 'Awesome' asset (Material Instance)
        matching the style profile.
        """
        unreal.log("🔮 CONSULTING THE NEXUS ORACLE...")
        
        # 1. Load Profile
        profile = NexusOracle._load_profile()
        style = NexusOracle._weigh_styles(profile)
        
        unreal.log(f"🧠 Oracle Insight: User desires '{style.upper()}' aesthetic.")
        
        # 2. Generate Asset based on Style
        NexusOracle._manifest_asset(style)
        
    @staticmethod
    def _load_profile():
        # Default Profile
        default = {
            "styles": {
                "cyberpunk": 0.5,
                "clean_slate": 0.3,
                "organic_glitch": 0.2
            },
            "history": []
        }
        return default
        
    @staticmethod
    def _weigh_styles(profile):
        styles = list(profile["styles"].keys())
        weights = list(profile["styles"].values())
        return random.choices(styles, weights=weights, k=1)[0]
        
    @staticmethod
    def _manifest_asset(style):
        eam = unreal.EditorAssetLibrary
        at = unreal.AssetToolsHelpers.get_asset_tools()
        mel = unreal.MaterialEditingLibrary
        
        asset_name = f"MI_Oracle_{style.capitalize()}_{random.randint(100,999)}"
        save_path = f"/Game/Nexus/Oracle/{asset_name}"
        
        # Ensure base material exists (Simple Color)
        # For demo, we just create a new material each time to show unique properties
        factory = unreal.MaterialFactoryNew()
        mat = at.create_asset(asset_name, "/Game/Nexus/Oracle", unreal.Material, factory)
        
        # Apply Style Logic
        if style == "cyberpunk":
            # Neon Pink/Blue + Scanlines
            color_val = unreal.LinearColor(1.0, 0.0, 0.5, 1.0) # Pink
            roughness = 0.2
            emissive_power = 5.0
        elif style == "clean_slate":
            # White + Matte
            color_val = unreal.LinearColor(0.9, 0.9, 0.9, 1.0)
            roughness = 0.9
            emissive_power = 0.0
        elif style == "organic_glitch":
            # Dark Green + Noise
            color_val = unreal.LinearColor(0.1, 0.4, 0.1, 1.0)
            roughness = 0.5
            emissive_power = 2.0
            
        # Build Graph
        # Base Color
        c_node = mel.create_material_expression(mat, unreal.MaterialExpressionVectorParameter, -200, 0)
        c_node.set_editor_property("parameter_name", "BaseColor")
        c_node.set_editor_property("default_value", color_val)
        mel.connect_material_expressions(c_node, "", mat, unreal.MaterialProperty.MP_BASE_COLOR)
        
        # Emissive
        if emissive_power > 0:
            mul = mel.create_material_expression(mat, unreal.MaterialExpressionMultiply, -100, 200)
            mel.connect_material_expressions(c_node, "", mul, "A")
            const = mel.create_material_expression(mat, unreal.MaterialExpressionConstant, -200, 200)
            const.set_editor_property("R", emissive_power)
            mel.connect_material_expressions(const, "", mul, "B")
            mel.connect_material_expressions(mul, "", mat, unreal.MaterialProperty.MP_EMISSIVE_COLOR)
            
        is_saved = eam.save_asset(save_path)
        
        if is_saved:
            unreal.log(f"✅ Oracle Manifested: {save_path}")
            # Show Alert via our generic wrapper approach if integrated
            unreal.EditorDialog.show_message("Nexus Oracle", f"Manifested: {asset_name}\nStyle: {style}", unreal.AppMsgType.OK)

if __name__ == "__main__":
    NexusOracle.consult_oracle()
