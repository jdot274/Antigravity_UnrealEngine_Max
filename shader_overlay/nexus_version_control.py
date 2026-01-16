import os
import shutil
import json
import time
from datetime import datetime

ARCHIVE_DIR = "/Users/joeywalter/antigravity-nexus/manifest_archive"
ASSETS_DIR = "/Users/joeywalter/antigravity-nexus/shader_overlay"
MANIFEST_FILE = os.path.join(ARCHIVE_DIR, "version_manifest.json")

def initialize_archive():
    if not os.path.exists(ARCHIVE_DIR):
        os.makedirs(ARCHIVE_DIR)
    if not os.path.exists(MANIFEST_FILE):
        with open(MANIFEST_FILE, 'w') as f:
            json.dump({"versions": [], "current_version": 0}, f, indent=4)

def version_asset(filename, content=None):
    """
    Saves and versions a file. If content is provided, it writes it.
    Otherwise, it copies the existing file from the ASSETS_DIR.
    """
    initialize_archive()
    
    with open(MANIFEST_FILE, 'r') as f:
        manifest = json.load(f)
    
    version_id = manifest["current_version"] + 1
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create version folder
    version_folder = os.path.join(ARCHIVE_DIR, f"v{version_id:03d}_{timestamp}")
    os.makedirs(version_folder)
    
    target_path = os.path.join(version_folder, filename)
    
    if content:
        with open(target_path, 'w') as f:
            f.write(content)
        # Also update the living asset
        living_path = os.path.join(ASSETS_DIR, filename)
        with open(living_path, 'w') as f:
            f.write(content)
    else:
        source_path = os.path.join(ASSETS_DIR, filename)
        if os.path.exists(source_path):
            shutil.copy2(source_path, target_path)
        else:
            print(f"Error: Source asset {source_path} not found.")
            return None

    # Update Manifest
    entry = {
        "version": version_id,
        "timestamp": timestamp,
        "asset": filename,
        "path": target_path
    }
    manifest["versions"].append(entry)
    manifest["current_version"] = version_id
    
    with open(MANIFEST_FILE, 'w') as f:
        json.dump(manifest, f, indent=4)
    
    print(f"📦 Versioned: {filename} -> v{version_id:03d}")
    return version_id

if __name__ == "__main__":
    # Test versioning
    version_asset("shaders/quantum_core.glsl")
    version_asset("nexus_game_engine.py")
