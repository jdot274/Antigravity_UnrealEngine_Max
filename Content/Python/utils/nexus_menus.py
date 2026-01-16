import unreal
import os
import json
import subprocess

# Define paths relative to the project
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
STATE_FILE = os.path.join(PROJECT_ROOT, "shader_overlay", "universe_state.json")

def sync_twin():
    """Logic for Syncing Unreal Twin"""
    unreal.log("🚀 Syncing Unreal Twin...")
    # Execute the One Click logic directly or subprocess?
    # Direct is better if possible, but for safety lets keep subprocess for the heavyweight stuff
    # Or just print instructions.
    unreal.EditorLevelLibrary.save_current_level()
    unreal.log("✅ Level Saved. Spawning Twin Process...")
    # Here we would call the complex logic
    
def toggle_stream_mode():
    unreal.log("📡 Toggling Stream Mode...")
    
def show_status():
    """Reads the universe state and logs it to the Output Log"""
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            data = json.load(f)
        
        unreal.log_warning("=== NEXUS UNIVERSE STATUS ===")
        for node in data.get("nodes", []):
            status = node.get("status", "UNKNOWN")
            name = node.get("name", "Unknown")
            unreal.log(f"[{status}] {name}")
        unreal.log_warning("===========================")
    else:
        unreal.log_error("Universe State file not found.")

class NexusMenuSetup:
    def __init__(self):
        self.menu_name = "LevelEditor.MainMenu.Nexus"
        self.menus = unreal.ToolMenus.get()
        
    def create_menu(self):
        # Find the Main Menu
        main_menu = self.menus.find_menu("LevelEditor.MainMenu")
        if not main_menu:
            return
            
        # Add 'Nexus' Submenu
        nexus_menu = main_menu.add_sub_menu(main_menu.get_name(), "Nexus", "Nexus", "NEXUS")
        
        # Add Actions
        self._add_entry(nexus_menu, "Sync Twin", "Sync Unreal Twin Logic", sync_twin)
        self._add_entry(nexus_menu, "Stream Mode", "Activate Pixel Streaming", toggle_stream_mode)
        self._add_entry(nexus_menu, "Status Monitor", "Dump Status to Log", show_status)
        
        self.menus.refresh_all_widgets()
        unreal.log("✅ Nexus Menu Initialized in Unreal Editor")

    def _add_entry(self, menu, label, tooltip, callback):
        entry = unreal.ToolMenuEntry(
            name=label,
            type=unreal.MultiBoxType.MENU_ENTRY,
            insert_position=unreal.ToolMenuInsert("", unreal.ToolMenuInsertType.DEFAULT)
        )
        entry.set_label(label)
        entry.set_tool_tip(tooltip)
        
        # In Python, we can't easily bind delegates for tool menus without a specific wrapper object
        # or using the 'string command' execution.
        # So we use set_string_command.
        
        # Hack: We need the function name to be importable or globally available.
        # A safer way for this specific context is using `unreal.SystemLibrary.execute_console_command`
        # But calling python directly from tool menu string command is: "py KeepingItReal()"
        
        # Let's assume we import this module in init_unreal.py as 'nexus_menus'
        cmd = f"import nexus_menus; nexus_menus.{callback.__name__}()"
        entry.set_string_command(
            unreal.ToolMenuStringCommandType.PYTHON,
            "",
            string=cmd
        )
        menu.add_menu_entry("SafeSection", entry)

# Global instance for the module
_setup = NexusMenuSetup()

# Accessible functions for the menu commands
def run_setup():
    _setup.create_menu()
