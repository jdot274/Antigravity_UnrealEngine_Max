import unreal
import os
import sys
import subprocess
import json

# Define the root of our Nexus
PROJECT_ROOT_ABS = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class NexusCLI:
    """
    The Central Command Line Interface for Antigravity Nexus.
    Supports Python, C++ (Build), and Gemini (Simulated) commands.
    Usage from Unreal Output Log: 
       import nexus_tools
       nexus_tools.cli("gemini help me fix this")
    """
    
    @staticmethod
    def run(command_str):
        parts = command_str.split(" ", 1)
        cmd_type = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""
        
        if cmd_type == "py" or cmd_type == "python":
            NexusCLI._run_python(args)
        elif cmd_type == "cpp" or cmd_type == "c++":
            NexusCLI._run_cpp(args)
        elif cmd_type == "gemini" or cmd_type == "ai":
            NexusCLI._run_gemini(args)
        elif cmd_type == "fe" or cmd_type == "file":
            NexusCLI._run_file_explorer(args)
        else:
            unreal.log_warning(f"NexusCLI: Unknown command '{cmd_type}'. Try 'py', 'cpp', 'gemini', or 'fe'.")

    @staticmethod
    def _run_python(code):
        unreal.log(f"🐍 Python Exec: {code}")
        try:
            exec(code)
        except Exception as e:
            unreal.log_error(f"Execution Error: {e}")

    @staticmethod
    def _run_cpp(args):
        unreal.log(f"⚙️ C++ Command: {args}")
        if "recompile" in args or "build" in args:
            unreal.log("Triggering Live Coding Compile...")
            unreal.SystemLibrary.execute_console_command(unreal.EditorLevelLibrary.get_editor_world(), "LiveCoding.Compile")
        else:
            unreal.log_warning("Only 'build' or 'recompile' is currently supported for C++ via NexusCLI.")

    @staticmethod
    def _run_gemini(prompt):
        unreal.log(f"✨ Gemini Inference: {prompt}")
        # In a real integration, this would call the Vertex AI API
        unreal.log("Gemini Reference Architecture Response: [Simulated]")
        unreal.log("   > To implement this feature, create a new C++ AActor subclass.")
        unreal.log("   > Use 'nexus_tools.cli(\"cpp build\")' to compile afterward.")

    @staticmethod
    def _run_file_explorer(path_alias):
        target_path = PROJECT_ROOT_ABS
        if path_alias == "content":
            target_path = os.path.join(PROJECT_ROOT_ABS, "Content")
        elif path_alias == "source":
            target_path = os.path.join(PROJECT_ROOT_ABS, "Source")
        elif path_alias == "plugins":
            target_path = os.path.join(PROJECT_ROOT_ABS, "Plugins")
            
        unreal.log(f"📂 Opening File Explorer at: {target_path}")
        
        if sys.platform == "win32":
            os.startfile(target_path)
        elif sys.platform == "darwin":  # Mac
            subprocess.Popen(["open", target_path])
        else:
            subprocess.Popen(["xdg-open", target_path])

# Shortcuts for the Menu System
def cli(cmd_str):
    NexusCLI.run(cmd_str)

def open_file_explorer_content():
    NexusCLI.run("fe content")

def open_file_explorer_source():
    NexusCLI.run("fe source")

def run_gemini_assist():
    # Since we can't easily pop an input box, we log instructions
    unreal.log_warning("⚠️ To use Gemini CLI: Type `nexus_tools.cli('gemini YOUR PROMPT')` in the Output Log.")

# ----------------------------------------------------------------------------------
# MENU INTEGRATION (Updating the previous Menu Setup to include these new tools)
# ----------------------------------------------------------------------------------


def build_slate_level():
    import level_generator
    level_generator.build_slate_level_with_nanite()

# Automation Wrapper
def show_alert(message, title="Nexus Automation"):
    """Displays an automatic UI alert to the user."""
    # Note: unreal.EditorDialog.show_message is blocking.
    # For non-blocking we would need Slate/PySide, but this ensures 'UI Alert' request is met.
    unreal.EditorDialog.show_message(title, message, unreal.AppMsgType.OK)

# Wrappers with Alerts
def _auto_fe_content():
    show_alert("Opening Content Folder Automatically...")
    open_file_explorer_content()

def _auto_fe_source():
    show_alert("Opening Source Folder Automatically...")
    open_file_explorer_source()

def _auto_build_level():
    show_alert("Constructing AAA Bio-Slate Environment...\n\nPlease wait while Nanite clouds are generated.")
    build_slate_level()
    show_alert("✅ Build Complete.\n\nEnjoy your new environment.", "Nexus Success")


def _auto_gen_solutions():
    show_alert("Accessing Gemini Ultra Models...\nGenerating 20 Advanced Solution Architectures...")
    import gemini_ultra_brain
    gemini_ultra_brain.generate_ultra_solutions()
    show_alert("✅ Analysis Complete.\n20 New Use Cases implanted in 'nexus_ultra_solutions.json'.", "Gemini Ultra")


def _auto_scan_object():
    # Prompt user for path (Simulated via hardcoded selection for now, or use Selected Actors)
    # In a real tool we'd get unreal.EditorLevelLibrary.get_selected_level_actors()[0]
    
    show_alert("Initializing Neural Depth Scanner...\nModel: MiDaS_v3_Hybrid")
    
    selected_actors = unreal.EditorLevelLibrary.get_selected_level_actors()
    if not selected_actors:
        # Default fallback
        target = "/Game/Nexus/Meshes/Cube_Default" 
        show_alert("No actor selected. Scanning simulation target: Cube_Default")
    else:
        target = selected_actors[0].get_actor_label()
    
    import neural_depth_engine
    result = neural_depth_engine.run_scan(target)
    
    show_alert(f"✅ SCAN COMPLETE\n\nTwin ID: {result['id']}\nLidar Density: {result['lidar_density']}", "Neural Scan")

def _auto_predict_track():
    show_alert("Initializing Kalman Filter Tracking...\nPredicting trajectories for AR Candidates.")
    import nexus_predictive_ml
    nexus_predictive_ml.demo_tracking()
    show_alert("✅ Prediction Visualized.\nGhost actors spawned at future coordinates.", "Nexus Prediction")

def _auto_consult_oracle():
    # The Oracle has its own internal alert, but we wrap it for consistency
    import nexus_oracle
    nexus_oracle.NexusOracle.consult_oracle()
    
def _auto_build_spatial_ui():
    show_alert("Constructing Spatial Command Interface...\nSpawning 3D Spline Executables.")
    import nexus_spatial_ui
    nexus_spatial_ui.build_spatial_interface()
    show_alert("✅ Interface Online.\nLook for the floating rings in the center of the world.", "Spatial UI")

def interact_raycast():
    """
    Simulates a 'Click' on a spatial UI element by checking selected actor tags.
    In a real runtime, we'd use LineTrace, but in Editor Python, 'Selected Actor' is the proxy for 'Clicked'.
    """
    actors = unreal.EditorLevelLibrary.get_selected_level_actors()
    if not actors:
        unreal.log_warning("Nexus Interaction: No actor selected.")
        return

    actor = actors[0]
    for tag in actor.tags:
        s_tag = str(tag)
        if s_tag.startswith("NexusCmd:"):
            cmd = s_tag.split(":", 1)[1]
            unreal.log(f"🖱️ SPATIAL CLICK DETECTED: {actor.get_actor_label()} -> {cmd}")
            exec(cmd)
            return
            
    unreal.log("Nexus Interaction: Selected actor is not a Spatial Executable.")

def _auto_spawn_cameras():
    show_alert("Initializng AR Hardware Simulation...\nSpawning iPhone 14 Pro & HoloLens 2 Rigs.")
    import nexus_cameras
    nexus_cameras.spawn_ar_camera_rig()
    show_alert("✅ Rigs Deployed.\nCameras are tagged [NexusAR] for ML injection.", "AR Cameras")

def _auto_import_data():
    show_alert("Running Nexus Importer Suite...\nGenerating Curves, Vector Fields, and Data Tables.")
    import nexus_importer
    nexus_importer.run_importer_suite()
    show_alert("✅ Data Assets Created.\nMapped with NexusType metadata.", "Nexus Importer")
    
def _auto_import_data():
    show_alert("Running Nexus Importer Suite...\nGenerating Curves, Vector Fields, and Data Tables.")
    import nexus_importer
    nexus_importer.run_importer_suite()
    show_alert("✅ Data Assets Created.\nMapped with NexusType metadata.", "Nexus Importer")

# Update Menu to include Level Gen
class NexusMenuSetup:
    def __init__(self):
        self.menus = unreal.ToolMenus.get()
        
    def create_menu(self):
        main_menu = self.menus.find_menu("LevelEditor.MainMenu")
        if not main_menu: return
            
        self.menus.remove_menu("LevelEditor.MainMenu.Nexus")
        nexus_menu = main_menu.add_sub_menu(main_menu.get_name(), "Nexus", "Nexus", "NEXUS")
        
        self._add_entry(nexus_menu, "Open Content Folder", "Browse Content Assets", _auto_fe_content)
        self._add_entry(nexus_menu, "Open Source Folder", "Browse C++ Source", _auto_fe_source)
        self._add_entry(nexus_menu, "Run Gemini Assist", "Ask AI for Help", run_gemini_assist)
        self._add_entry(nexus_menu, "Recompile C++", "Trigger Live Coding", lambda: NexusCLI.run("cpp build"))
        
        self._add_entry(nexus_menu, "Build AAA Slate Level", "Generate Slate Ground & Nanite Cloud", _auto_build_level)
        self._add_entry(nexus_menu, "Generate Ultra Solutions", "20 AI Use Cases (Gemini Ultra)", _auto_gen_solutions)
        self._add_entry(nexus_menu, "Scan Object to Twin", "Create Digital Twin (Neural Depth)", _auto_scan_object)
        
        self._add_entry(nexus_menu, "Predict AR Tracking", "Simulate ML Motion Prediction", _auto_predict_track)
        self._add_entry(nexus_menu, "Consult Asset Oracle", "Generate Assets based on Tech Style", _auto_consult_oracle)
        
        # SPATIAL UI
        self._add_entry(nexus_menu, "Construct Spatial UI", "Spawn 3D Executable Buttons", _auto_build_spatial_ui)
        self._add_entry(nexus_menu, "Interact with Selected", "Trigger Spatial Button (Click Sim)", interact_raycast)
        
        # CAMERAS
        self._add_entry(nexus_menu, "Spawn AR Cameras", "Create Simulated AR CineCameras", _auto_spawn_cameras)
        self._add_entry(nexus_menu, "Import Data Types", "Generate Curves & Vector Fields", _auto_import_data)
        
        self.menus.refresh_all_widgets()
        unreal.log("✅ Nexus Tools & CLI Initialized")

    def _add_entry(self, menu, label, tooltip, callback):
        entry = unreal.ToolMenuEntry(
            name=label,
            type=unreal.MultiBoxType.MENU_ENTRY,
            insert_position=unreal.ToolMenuInsert("", unreal.ToolMenuInsertType.DEFAULT)
        )
        entry.set_label(label)
        entry.set_tool_tip(tooltip)
        
        # Dynamic dispatch wrapper handles both lambdas and named functions securely
        # For our wrapper functions beginning with _, we need to ensure they are accessible
        func_name = callback.__name__
        if func_name == "<lambda>":
             # Fallback for simple lambdas
             cmd = "import nexus_tools; nexus_tools.cli('cpp build')"
        else:
             cmd = f"import nexus_tools; nexus_tools.{func_name}()"

        entry.set_string_command(unreal.ToolMenuStringCommandType.PYTHON, "", string=cmd)
        menu.add_menu_entry("SafeSection", entry)

_setup = NexusMenuSetup()
def run_setup():
    _setup.create_menu()
