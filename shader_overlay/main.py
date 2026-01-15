import sys
import os
import logging
import subprocess
import json
from PySide6.QtCore import Qt, QUrl, QObject, Slot, Signal
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebChannel import QWebChannel

# Setup Logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))
    res = os.path.join(base_path, relative_path)
    logger.debug(f"Resolved resource path: {res}")
    return res

class CommandBridge(QObject):
    # Signal to relay commands to other windows
    relay_cmd = Signal(str, str) # window_target, command_json

    @Slot(str, str)
    def call(self, target, command_str):
        logger.debug(f"Bridge received: {target} -> {command_str}")
        
        try:
            cmd_data = json.loads(command_str)
            action = cmd_data.get('action')
            
            # 1. SYSTEM ACTIONS (Executed on Host)
            if target == "system":
                self.execute_system_action(action, cmd_data)
            
            # 2. RELAY ACTIONS (Sent to Editor Window for UI/Viewport changes)
            else:
                self.relay_cmd.emit(target, command_str)
                
        except Exception as e:
            logger.error(f"Error processing command: {e}")

    def execute_system_action(self, action, data):
        logger.info(f"Executing System Action: {action}")
        
        if action == "open_vscode":
            subprocess.Popen(["code", "."], cwd=os.getcwd())
        
        elif action == "launch_unreal":
            editor_path = "/Users/Shared/Epic Games/UE_5.7/Engine/Binaries/Mac/UnrealEditor.app/Contents/MacOS/UnrealEditor"
            project_path = "/Users/joeywalter/Documents/Unreal Projects/MyProject/MyProject.uproject"
            subprocess.Popen([editor_path, project_path, "-skipcompile"])
        
        elif action == "build_all":
            # Launch the real packaging script
            subprocess.Popen([sys.executable, "package_unreal.py"], cwd=os.getcwd())
        
        elif action == "git_sync":
            subprocess.Popen(["git", "pull"], cwd=os.getcwd())
            
        elif action == "cook":
            # Simulation of cooking, could link to a real UAT command
            logger.info("Triggering Native Content Cook...")
            self.relay_cmd.emit("editor", json.dumps({"action": "show_status", "msg": "COOKING CONTENT..."}))

        elif action == "open_browser":
            url = data.get("url", "https://github.com")
            subprocess.Popen(["open", url])

class AntigravityEditor(QMainWindow):
    def __init__(self, bridge):
        super().__init__()
        self.bridge = bridge
        self.setWindowTitle("Antigravity Engine Editor")
        
        # Transparent, Frameless, Always on Top
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet("background-color: #0d1117;")
        
        self.setGeometry(100, 100, 1280, 720)
        
        self.web_view = QWebEngineView()
        self.channel = QWebChannel()
        self.channel.registerObject("bridge", self.bridge)
        self.web_view.page().setWebChannel(self.channel)
        
        path = resource_path("nexus_hub.html")
        url = QUrl.fromLocalFile(path)
        self.web_view.setUrl(url)
        self.setCentralWidget(self.web_view)
        
        # Listen for relay commands targeting 'editor'
        self.bridge.relay_cmd.connect(self.handle_relay)

    def handle_relay(self, target, cmd_str):
        if target == "editor":
            logger.debug(f"Injecting JS into editor: handleEngineCommand({cmd_str})")
            # Clear escaping for JS execution
            self.web_view.page().runJavaScript(f"if(typeof handleEngineCommand === 'function') handleEngineCommand({cmd_str});")

class EngineController(QMainWindow):
    def __init__(self, bridge):
        super().__init__()
        self.bridge = bridge
        self.setWindowTitle("Antigravity Engine Controller")
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
        self.setStyleSheet("background-color: #0d1117;")
        
        screen = QApplication.primaryScreen().geometry()
        self.setGeometry(screen.width() - 450, 60, 400, 850)
        
        self.web_view = QWebEngineView()
        self.channel = QWebChannel()
        self.channel.registerObject("bridge", self.bridge)
        self.web_view.page().setWebChannel(self.channel)

        path = resource_path("engine_controller.html")
        self.web_view.setUrl(QUrl.fromLocalFile(path))
        self.setCentralWidget(self.web_view)

if __name__ == "__main__":
    logger.debug("Starting Multi-Window Application Process...")
    os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--enable-gpu-rasterization --ignore-gpu-blocklist"
    
    app = QApplication(sys.argv)
    
    # Global Bridge
    bridge = CommandBridge()
    
    # 1. Main 3D Simulator Editor
    editor = AntigravityEditor(bridge)
    editor.show()
    
    # 2. Native Engine Controller (The real menus)
    controller = EngineController(bridge)
    controller.show()
    
    sys.exit(app.exec())
