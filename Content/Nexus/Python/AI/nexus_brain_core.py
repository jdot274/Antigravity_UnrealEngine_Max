import os
import json
import unreal

# Try to import local env libs
try:
    import google.generativeai as genai
    from dotenv import load_dotenv
    HAS_LIBS = True
except ImportError:
    HAS_LIBS = False
    unreal.log_warning("⚠️ NexusBrain: Missing google-generativeai or dotenv. Running in MOCK mode.")

class NexusBrain:
    def __init__(self):
        self.api_key = None
        self.model = None
        
        if HAS_LIBS:
            # Load .env manually if python-dotenv fails or just read file
            env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))), ".env")
            if os.path.exists(env_path):
                with open(env_path, "r") as f:
                    for line in f:
                        if line.startswith("GEMINI_API_KEY="):
                            self.api_key = line.strip().split("=")[1]
                            break
            
            if self.api_key:
                genai.configure(api_key=self.api_key)
                # 2026 ARCHITECTURE UPGRADE: Gemini 3.0 Series
                # Defaulting to 3.0 Pro for balance of speed/reasoning
                try:
                    # 2026 Full Spectrum-Suite
                    self.fast_model = genai.GenerativeModel('gemini-3.0-flash')      # Speed (Translation)
                    self.smart_model = genai.GenerativeModel('gemini-3.0-pro')       # General Intelligence (Director)
                    self.deep_model = genai.GenerativeModel('gemini-3.0-deep-think') # Complex Planning (Architecture)
                    
                    unreal.log("🧠 NexusBrain: ONLINE (Gemini 3.0 Flash/Pro/Deep-Think Connected)")
                    
                    # --- HYBRID LINK ---
                    # Initialize the C++ Persistent Core
                    try:
                        status = unreal.NexusBridge.execute_runtime_cpp("INIT_SYSTEM", "BrainLink")
                        unreal.log(f"🔗 C++ Core Linked: {status}")
                    except AttributeError:
                        unreal.log_warning("⚠️ NexusBridge C++ Class not found. Did you recompile?")
                        
                except:
                    # Fallback
                    self.smart_model = genai.GenerativeModel('gemini-1.5-pro')
                    self.fast_model = self.smart_model
                    self.deep_model = self.smart_model
                    unreal.log_warning("⚠️ NexusBrain: Gemini 3.0 unreachable, falling back to 1.5 Pro Ultra")
            else:
                unreal.log_error("❌ NexusBrain: No API KEY found in .env")

    def think(self, user_prompt):
        """
        Cognitive processing. Returns structured JSON directive.
        """
        if not self.smart_model:
            return self._mock_brain(user_prompt)

        # Route complex planning to Deep Think
        active_model = self.smart_model
        if "plan" in user_prompt.lower() or "design" in user_prompt.lower() or "complex" in user_prompt.lower():
            active_model = self.deep_model
            unreal.log("🤔 Deep Thinking Activated...")

        # System Prompt for JSON output
        sys_prompt = """
        You are the AI Director of a Virtual Engine. 
        Analyze the user's Natural Language request and output a strictly formatted JSON object.
        Possible Actions: "CREATE", "MODIFY", "TRANSLATE", "PHYSICS".
        
        Example Output:
        {
            "action": "CREATE",
            "objects": [
                {"type": "sphere", "color": [1.0, 0.0, 0.0], "location": [0,0,100], "name": "RedBall"}
            ],
            "physics": true
        }
        
        If the user asks to translate, return: {"action": "TRANSLATE", "text": "...", "target": "..." }
        """
        
        try:
            response = self.model.generate_content(f"{sys_prompt}\nUSER: {user_prompt}")
            # Clean md blocks if present
            txt = response.text.replace("```json", "").replace("```", "")
            return json.loads(txt)
        except Exception as e:
            unreal.log_error(f"Brain Freeze: {e}")
            return self._mock_brain(user_prompt)

    def translate(self, text, target_language="English"):
        """
        Universal Translator Module (Uses 3.0 Flash for sub-100ms latency)
        """
        if not self.fast_model:
            return f"[MOCK TRANSLATION] {text} -> {target_language}"
            
        try:
            prompt = f"Translate the following text to {target_language}. Return ONLY the translated text.\n\nText: {text}"
            res = self.fast_model.generate_content(prompt)
            return res.text.strip()
        except Exception as e:
            return f"Translation Error: {e}"

    def _mock_brain(self, prompt):
        """
        Fallback logic purely based on keywords if API is down.
        """
        unreal.log_warning("⚠️ Using Mock Brain Logic")
        p = prompt.lower()
        if "sphere" in p:
            return {
                "action": "CREATE", 
                "objects": [{"type": "sphere", "color": [1,1,1], "location": [0,0,200]}],
                "physics": "fall" in p
            }
        return {"action": "UNKNOWN", "original": prompt}

# Global Instance
BRAIN = NexusBrain()
