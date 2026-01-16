import unreal
import sys
import os

# Add current dir to path to ensure imports work
current_dir = "/Users/joeywalter/antigravity-nexus/shader_overlay"
if current_dir not in sys.path:
    sys.path.append(current_dir)

# Import the amazing modules
import nexus_world_populator
import nexus_oled_monitor
import nexus_aaa_factory
import nexus_material_builder

def main():
    print("🚀 STARTING AMAZING REFURBISHMENT PROTOCOL 🚀")
    
    # Wrap in a transaction so one Undo can revert (mostly)
    with unreal.ScopedEditorTransaction("Run All Amazing Scripts"):
        try:
            # 1. Materials (Foundation)
            print("\n--- Phase 1: Material Synthesis ---")
            # This creates the glass and neon materials needed by others
            nexus_material_builder.import_tennis_assets()
            nexus_material_builder.create_neon_material("M_NeonGold", (1, 0.8, 0))
            nexus_material_builder.create_neon_material("M_VoidBlack", (0, 0, 0))
            
            # 2. Chaos Population (Scattering objects)
            print("\n--- Phase 2: World Population ---")
            nexus_world_populator.populate_chaos_scene()
            
            # 3. OLED Monitor (The centerpiece)
            print("\n--- Phase 3: OLED Monitor Construction ---")
            nexus_oled_monitor.create_futuristic_oled_monitor()
            
            # 4. AAA Factory (The detailed artifacts)
            print("\n--- Phase 4: AAA Mesh Instantiation ---")
            nexus_aaa_factory.main()
            
            print("\n✅ ALL AMAZING SCRIPTS EXECUTED SUCCESSFULLY!")
            print("   - Check the Output Log for details.")
            print("   - Look at the viewport to see the changes.")
            
        except Exception as e:
            print(f"❌ Error during execution: {e}")
            unreal.log_error(f"Amazing Script Error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    main()
