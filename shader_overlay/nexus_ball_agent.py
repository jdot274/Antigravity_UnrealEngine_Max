import json
import random
import math

class NexusBallAgent:
    def __init__(self):
        self.name = "🎾 Nexus Voxtennis Agent"
        self.material_config = {
            "Type": "Advanced Glass",
            "IOR_Red": 1.54,
            "IOR_Green": 1.50,
            "IOR_Blue": 1.46,
            "Roughness": 0.05,
            "Transmission": 0.98,
            "Emissive": [0.1, 1.0, 0.5] # Tennis Green
        }
        self.voxel_grid = []
        self.generate_voxels()

    def generate_voxels(self):
        """Generates the 16,000 dot 3D array representing the ball's volume."""
        print("🎾 Generating Voxel Tensor for Ball Volume...")
        points = []
        # Create a density cloud in a sphere shape
        radius = 50.0
        count = 16000
        
        for i in range(count):
            # Uniform sphere distribution approximation
            phi = random.uniform(0, 2 * math.pi)
            costheta = random.uniform(-1, 1)
            u = random.random()
            
            theta = math.acos(costheta)
            r = radius * (u ** (1/3))
            
            x = r * math.sin(theta) * math.cos(phi)
            y = r * math.sin(theta) * math.sin(phi)
            z = r * math.cos(theta)
            
            # Add some "fuzz" procedural noise
            x += random.uniform(-2, 2)
            y += random.uniform(-2, 2)
            z += random.uniform(-2, 2)
            
            points.append((round(x, 2), round(y, 2), round(z, 2)))
            
        self.voxel_grid = points
        print(f"✅ Generated {len(points)} voxels.")

    def respond_to_prompt(self, user_prompt):
        """
        The Core Agent Loop.
        Returns the data structure requested by the user.
        """
        response = {
            "Agent": self.name,
            "Prompt_Received": user_prompt,
            "Material_Effects": self.material_config,
            "Voxel_Data_Sample": self.voxel_grid[:10], # Show first 10 for sanity
            "Total_Voxels": len(self.voxel_grid),
            "Render_Directive": "EXECUTE_RAYMARCH_PASS"
        }
        return json.dumps(response, indent=2)

if __name__ == "__main__":
    agent = NexusBallAgent()
    print(agent.respond_to_prompt("Initialize"))
