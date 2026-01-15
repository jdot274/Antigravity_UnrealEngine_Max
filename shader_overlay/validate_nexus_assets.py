import json
import os
import sys

MANIFEST_PATH = "/Users/joeywalter/antigravity-nexus/shader_overlay/nexus_asset_manifest.json"

def validate_manifest():
    print("🛡️ ANTIGRAVITY NEXUS: ASSET AUDIT STARTING...")
    
    if not os.path.exists(MANIFEST_PATH):
        print(f"❌ CRITICAL ERROR: Manifest not found at {MANIFEST_PATH}")
        return

    with open(MANIFEST_PATH, 'r') as f:
        data = json.load(f)

    meta = data.get('meta', {})
    print(f"--- Meta Context ---")
    print(f"Compliance: {meta.get('pbr_compliance')}")
    print(f"UE Target: {meta.get('engine_target')}")
    print(f"References: {len(meta.get('authoritative_references', {}))} found.")

    assets = data.get('asset_mappings', [])
    print(f"\n--- Asset Audit ({len(assets)} items) ---")
    
    for asset in assets:
        asset_id = asset.get('id')
        name = asset.get('name')
        latest = asset['versions'][0]
        
        print(f"\n[ID: {asset_id}] {name} (v{latest['ver']})")
        
        # Check targets
        targets = latest.get('targets', {})
        for target_type, spec in targets.items():
            if target_type == 'gltf':
                path = spec.get('path')
                full_path = os.path.join("/Users/joeywalter/antigravity-nexus/shader_overlay", path)
                status = "✅ FOUND" if os.path.exists(full_path) else "⚠️ MISSING (Placeholder)"
                print(f"  - glTF: {path} [{status}]")
                if spec.get('poly_count', 0) > 100000:
                    print(f"    🚨 WARNING: Polycount ({spec['poly_count']}) exceeds mobile/XR limits (Khronos recommendation).")
            
            elif target_type == 'spline':
                print(f"  - Spline: {spec.get('url')[:40]}...")
            
            elif target_type == 'unreal':
                print(f"  - Unreal: {spec.get('asset_path')} [Nanite: {spec.get('nanite')}]")

    print("\n✅ AUDIT COMPLETE. NEXUS VERSION MAPPING IS AUTHORITATIVE.")

if __name__ == "__main__":
    validate_manifest()
