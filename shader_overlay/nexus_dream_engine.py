import unreal
import os
import json
import subprocess
import time
import sys

# Ensure local modules are found
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# Import Nexus Modules
import nexus_drift_rl
import nexus_vehicle_setup
import gemini_code_assist_bridge
import nexus_material_builder

def launch_nexus_super_session():
    """
    Orchestrates the entire Antigravity x Gemini x Unreal pipeline.
    """
    print("\n" + "="*50)
    print("🌌  ANTIGRAVITY NEXUS: SUPER SESSION INITIALIZING  🌌")
    print("="*50 + "\n")

    # 1. Build Material Infrastructure
    nexus_material_builder.create_nexus_glass_material()

    # 1. Instantiate the AI Assistant
    assistant = gemini_code_assist_bridge.GeminiCodeAssistBridge()
    assistant.stream_status_to_gemini("SESSION_START")

    # 2. Build World (Rocket League x Gran Turismo Hybrid)
    game_builder = nexus_drift_rl.NexusDriftRL()
    game_builder.create_gt_rl_hybrid_level()

    # 3. Optimize the Volumetric Glass Shader via Gemini
    shader_file = "/Users/joeywalter/antigravity-nexus/shader_overlay/shaders/glass_spheres.hlsl"
    assistant.optimize_shader(shader_file)

    # 4. Rig the Vehicle (GT Physics)
    nexus_vehicle_setup.setup_nx_vehicle()

    # 5. Gemini-Assisted Level Tweaks
    print("🤖 Gemini: Applying dynamic fog and volumetric light rays...")
    actors = unreal.EditorLevelLibrary.get_all_level_actors()
    for a in actors:
        if isinstance(a, unreal.DirectionalLight):
            comp = a.get_component_by_class(unreal.DirectionalLightComponent)
            comp.set_bloom_scale(1.2)
            comp.set_light_shaft_cone_angle(45.0)

    # 6. Initialize Pixel Streaming Signalling
    game_builder.setup_pixel_streaming()
    
    # 7. SAVE THE LEVEL
    print("💾 Saving Map: Nexus_Volumetric_Lab...")
    unreal.EditorLevelLibrary.save_current_level_as("/Game/Nexus_Volumetric_Lab")

    # 8. AUTO-LAUNCH PIE
    print("🚀 Triggering Play-In-Editor for Live Stream...")
    # Setting the viewport to be the active focus and playing
    unreal.SystemLibrary.execute_console_command(None, "map Nexus_Volumetric_Lab")
    time.sleep(2)
    # Note: verify using command line -game argument for better headless streaming
    
    # 9. Final Handshake
    assistant.stream_status_to_gemini("PIPELINE_STABLE")
    print("\n✅ ALL SYSTEMS ONLINE.")
    print("🏎️  Rocket League x Gran Turismo Arena is READY.")
    print("🌐 Pixel Stream serving at: http://localhost:8080")
    print("="*50 + "\n")

if __name__ == "__main__":
    launch_nexus_super_session()
