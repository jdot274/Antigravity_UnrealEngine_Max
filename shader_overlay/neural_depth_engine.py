import json
import math
import random

def generate_depth_cloud(image_path, resolution=64):
    """
    Simulates depth mapping by generating a 3D point cloud from a 2D resolution.
    In a full implementation, this would use a model like MiDaS or ZoeDepth.
    """
    points = []
    for y in range(resolution):
        for x in range(resolution):
            # Calculate normalized coords
            nx = x / resolution
            ny = y / resolution
            
            # Simulate a "Face-like" depth (spherical or topographic)
            # Center of the grid is closest (higher Z)
            dist_from_center = math.sqrt((nx-0.5)**2 + (ny-0.5)**2)
            z = math.cos(dist_from_center * math.pi) * 50.0 # Depth amplitude
            
            # Add small 'detail' noise
            z += random.uniform(-1, 1)
            
            points.append({
                "x": (nx - 0.5) * 200, # Spread
                "y": (ny - 0.5) * 200,
                "z": z,
                "r": 0.0, "g": 0.8, "b": 1.0, "a": 1.0 # Manifest Blue
            })
            
    return points

def export_cloud_for_niagara(points, output_path):
    with open(output_path, "w") as f:
        json.dump(points, f)
    print(f"Generated {len(points)} points for Niagara Cloud at {output_path}")

if __name__ == "__main__":
    import sys
    img = sys.argv[1] if len(sys.argv) > 1 else "default_face.jpg"
    out = "/Users/joeywalter/antigravity-nexus/shader_overlay/depth_cloud.json"
    cloud = generate_depth_cloud(img)
    export_cloud_for_niagara(cloud, out)
