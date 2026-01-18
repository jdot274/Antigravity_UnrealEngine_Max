import json
import random
import math
import os

def generate_track(length=1000):
    """
    Generates a procedural 'safety track' for the Gravity UI.
    Creates a JSON file with road curvature and world object placement.
    Simulates a 'focused' drive.
    """
    
    track_data = {
        "segments": [],
        "objects": []
    }
    
    current_curvature = 0
    target_curvature = 0
    
    # Generate Road Segments
    for i in range(length):
        # Smoothly interpolate curvature
        if i % 50 == 0:
            target_curvature = (random.random() - 0.5) * 0.5 # New random curve target
            
        current_curvature += (target_curvature - current_curvature) * 0.05
        
        segment = {
            "z": i, # dist
            "curve": current_curvature
        }
        track_data["segments"].append(segment)
        
        # Determine if we spawn object
        # "Fake non mesh designs" - procedural blocks
        if random.random() > 0.9:
            side = -1 if random.random() > 0.5 else 1
            # Avoid the center road (safety critical zone)
            x_pos = side * (1.5 + random.random() * 4.0) 
            
            obj = {
                "z": i,
                "x": x_pos,
                "width": 1.0 + random.random() * 2.0,
                "height": 2.0 + random.random() * 5.0,
                "type": "block"
            }
            track_data["objects"].append(obj)

    # Save to JSON
    output_path = os.path.join(os.path.dirname(__file__), 'world_data.json')
    with open(output_path, 'w') as f:
        json.dump(track_data, f)
        
    print(f"Generated world data at {output_path}")

if __name__ == "__main__":
    generate_track()
