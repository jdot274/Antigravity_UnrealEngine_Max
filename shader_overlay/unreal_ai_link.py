import unreal
import requests
import json

# CONFIG
BRIDGE_URL = "http://localhost:3002/chat"

class UnrealNexusAI:
    def __init__(self):
        unreal.log("🛡️ Antigravity_UnrealEngine: AI Live Execution Link Active")
        
    def talk(self, message):
        """Send message and EXECUTE code returned by Gemini"""
        try:
            # We explicitly tell Gemini it has access to the 'unreal' python API
            payload = {
                "message": f"SYSTEM INSTRUCTION: You are an Unreal Engine 5.7 Python Expert. Return ONLY valid python code that uses the 'unreal' module to achieve the goal. No explanation.\n\nUSER REQUEST: {message}",
                "context": {
                    "source": "unreal_editor_live",
                    "mode": "execution"
                }
            }
            
            response = requests.post(BRIDGE_URL, json=payload)
            if response.status_code == 200:
                ai_code = response.json().get('response', '')
                
                # Strip markdown code blocks if present
                clean_code = ai_code.replace("```python", "").replace("```", "").strip()
                
                unreal.log(f"🚀 EXECUTING NEXUS CODE:\n{clean_code}")
                
                # THE LIVE EXECUTION STEP
                try:
                    exec(clean_code)
                    unreal.log("✅ EXECUTION SUCCESSFUL")
                except Exception as e:
                    unreal.log_error(f"❌ Execution Failed: {str(e)}")
                    
            else:
                unreal.log_error(f"❌ Bridge Error: {response.status_code}")
        except Exception as e:
            unreal.log_error(f"❌ Failed to reach Nexus Bridge: {str(e)}")

    def implement_cpp(self, message):
        """Handle C++ Generation, File Writing, and Live Coding Trigger"""
        unreal.log("🛡️ Antigravity Nexus: Initiating C++ Tactical Build...")
        
        try:
            payload = {
                "message": f"SYSTEM INSTRUCTION: You are a Senior Unreal C++ Architect. Return a JSON object with 'header_code', 'source_code', and 'filename' (e.g. MyActor). No explanation.\n\nUSER REQUEST: {message}",
                "context": {
                    "source": "unreal_editor_cpp",
                    "mode": "cpp_generation"
                }
            }
            
            response = requests.post(BRIDGE_URL, json=payload)
            if response.status_code == 200:
                data = json.loads(response.json().get('response', '{}'))
                
                h_code = data.get('header_code')
                cpp_code = data.get('source_code')
                filename = data.get('filename')
                
                # Use Unreal Python to find the source directory
                proj_dir = unreal.Paths.project_dir()
                source_dir = unreal.Paths.combine(unreal.Paths.convert_relative_path_to_full(proj_dir), "Source/MyProject")
                
                if not unreal.Paths.directory_exists(source_dir):
                    unreal.log_error(f"❌ Source directory not found: {source_dir}")
                    return

                # Write files
                h_path = unreal.Paths.combine(source_dir, f"{filename}.h")
                cpp_path = unreal.Paths.combine(source_dir, f"{filename}.cpp")
                
                with open(h_path, 'w') as f: f.write(h_code)
                with open(cpp_path, 'w') as f: f.write(cpp_code)
                
                unreal.log(f"✅ C++ Files Written: {filename}.h/cpp")
                
                # Trigger Live Coding Recompile
                unreal.log("⚙️ Triggering Live Coding Recompile...")
                unreal.EditorTests.recompile_game_code() # Or use subprocess to trigger shortcut
                
            else:
                unreal.log_error(f"❌ Bridge Error: {response.status_code}")
        except Exception as e:
            unreal.log_error(f"❌ C++ Build Failed: {str(e)}")

# Global instance for the session
if 'nexus_ai' not in globals():
    nexus_ai = UnrealNexusAI()

def implement(msg):
    """Call this from Unreal Python Console: implement('spawn 10 red spheres')"""
    nexus_ai.talk(msg)

def implement_cpp(msg):
    """Call this from Unreal Python Console: implement_cpp('create a new C++ component that follows the player')"""
    nexus_ai.implement_cpp(msg)

unreal.log("--- NEXUS LIVE IMPLEMENTATION READY ---")
unreal.log("Use: implement('request') to generate and run code instantly.")
