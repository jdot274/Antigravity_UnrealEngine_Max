import sys
import json
import os
import numpy as np
from PIL import Image

def generate_hologram_data(image_path, output_path):
    """
    Scans the input image and converts high-luminance pixels into 3D points.
    Returns the path to the generated point cloud JSON.
    """
    print(f"🧬 Neural Depth Engine: Scanning {image_path}...")
    
    if not os.path.exists(image_path):
        print(f"❌ Error: Image not found at {image_path}")
        return None

    try:
        # Load and process image
        img = Image.open(image_path).convert('L') # Grayscale
        # Resize for performance (fingerprints are detailed, but ISMs have limits)
        # 128x128 = 16k points, acceptable for ISM.
        img = img.resize((128, 128)) 
        data = np.array(img)
        
        points = []
        width, height = img.size
        
        # Threshold: Only spawn points for the actual print ridges
        # Map Brightness > 30 -> Point
        
        for y in range(height):
            for x in range(width):
                brightness = data[y][x]
                if brightness > 30: # Threshold
                    # Normalize coordinates centered at 0
                    nx = (x - width/2) * 10
                    ny = (y - height/2) * 10
                    nz = (brightness / 255.0) * 50 # Height map from brightness
                    
                    points.append({
                        "id": len(points),
                        "t": [nx, ny, nz], # Translation
                        "c": [0.0, 1.0, 1.0, brightness/255.0] # Cyan Color (R,G,B,A)
                    })
        
        print(f"✨ Extracted {len(points)} holographic points.")
        
        # Save to JSON
        with open(output_path, 'w') as f:
            json.dump(points, f)
            
        return output_path
        
    except Exception as e:
        print(f"❌ Processing Error: {e}")
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        # Default test
        target_img = "/Users/joeywalter/antigravity-nexus/Content/IMG_9279.png"
    else:
        target_img = sys.argv[1]
        
    out_json = "/Users/joeywalter/antigravity-nexus/Content/biometric_cloud.json"
    generate_hologram_data(target_img, out_json)
