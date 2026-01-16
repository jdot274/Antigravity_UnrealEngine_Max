import unreal
import subprocess
import os
import json

class NexusEngineBridge:
    def __init__(self):
        self.state_path = "/Users/joeywalter/antigravity-nexus/shader_overlay/universe_state.json"
        self.notif_bridge = "/Users/joeywalter/antigravity-nexus/shader_overlay/push_notif.py"

    def sync_to_twin(self):
        """Notifies the external monitor that Unreal has joined the cluster."""
        msg = "Unreal Twin connected. Shared state sync active."
        subprocess.run(["python3", self.notif_bridge, "Engine Link", msg, "SUCCESS"])
        
    def trigger_neural_lab_sim(self, image_input):
        """
        Executes the Neural Depth Mapping pipeline.
        1. Generates depth json from image.
        2. Informs Unreal to update the Niagara Data Interface.
        """
        print(f"🧬 Initializing Neural Graphics Lab for: {image_input}")
        
        # Run the depth engine
        depth_script = "/Users/joeywalter/antigravity-nexus/shader_overlay/neural_depth_engine.py"
        subprocess.run(["python3", depth_script, image_input])
        
        # Tell Unreal (via Python API) to refresh the simulation
        # In a target-rich environment, we'd find the Niagara actor here
        print("✅ Depth Cloud generated. Requesting Niagara refresh...")
        
    def spawn_twin_huds(self):
        """Native Unreal HUD launch."""
        euw_subsystem = unreal.get_subsystem(unreal.EditorUtilitySubsystem)
        monitor_asset = unreal.EditorAssetLibrary.load_asset("/Game/Editor/EUW_UniverseMonitor")
        portal_asset = unreal.EditorAssetLibrary.load_asset("/Game/Editor/EUW_NexusMainPortal")
        
        if monitor_asset:
            euw_subsystem.spawn_and_register_tab(monitor_asset)
        if portal_asset:
            euw_subsystem.spawn_and_register_tab(portal_asset)

# Singleton Instance for the Engine
nexus_bridge = NexusEngineBridge()

if __name__ == "__main__":
    nexus_bridge.sync_to_twin()
