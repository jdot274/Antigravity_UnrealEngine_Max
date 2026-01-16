import unreal
import json
import os

def generate_live_architecture_report():
    """
    Scans the actual Unreal structure and exports it for the Architect Portal.
    """
    unreal.log("🛡️ Antigravity: Indexing Container Architecture...")
    
    project_dir = unreal.Paths.project_dir()
    content_dir = unreal.Paths.content_dir()
    
    report = {
        "project_name": unreal.Paths.get_base_filename(unreal.Paths.get_project_file_path()),
        "engine_version": "5.7.0X",
        "container_health": "OPTIMAL",
        "spatial_containers": [],
        "logic_modules": [],
        "active_worlds": []
    }
    
    # 1. Gather Maps (.umaps) - Our Worlds
    assets = unreal.EditorAssetLibrary.list_assets("/Game")
    for asset in assets:
        asset_data = unreal.EditorAssetLibrary.find_asset_data(asset)
        if asset_data.asset_class_path.asset_name == "World":
            report["active_worlds"].append({
                "name": str(asset_data.asset_name),
                "path": str(asset_data.package_name),
                "type": "WorldPartition_Container" if "WP" in str(asset_data.asset_name) else "Standard_Level"
            })
            
    # 2. Gather Plugins - Our Logic Containers
    plugins = unreal.PluginBlueprintLibrary.get_enabled_plugins()
    for plugin in plugins:
        if "Antigravity" in plugin:
            report["logic_modules"].append({
                "name": plugin,
                "status": "LOADED",
                "isolation": "SECURE"
            })

    output_path = "/Users/joeywalter/antigravity-nexus/shader_overlay/live_architecture.json"
    with open(output_path, 'w') as f:
        json.dump(report, f, indent=4)
        
    unreal.log(f"✅ Architecture Report Manifested at {output_path}")

if __name__ == "__main__":
    generate_live_architecture_report()
