import sys
import os
import json
import subprocess
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QFrame, QPushButton, QMenuBar,
                             QMenu, QSizePolicy, QScrollArea)
from PySide6.QtCore import Qt, QTimer, QPoint, QSize
from PySide6.QtGui import QAction, QColor, QPalette, QIcon

class NexusMasterEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NEXUS MASTER EDITOR")
        self.resize(1200, 800)
        
        # Dark Theme Palette
        self.setStyleSheet("""
            QMainWindow { background-color: #0c0d14; }
            QMenuBar { background-color: #1a1b26; color: #a9b1d6; border-bottom: 1px solid #24283b; }
            QMenuBar::item:selected { background-color: #24283b; }
            QMenu { background-color: #1a1b26; color: #a9b1d6; border: 1px solid #24283b; }
            QMenu::item:selected { background-color: #24283b; }
        """)

        # Main Layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(1)

        # 1. Sidebar (Minimap & tech stack)
        self.sidebar = QFrame()
        self.sidebar.setFixedWidth(260)
        self.sidebar.setStyleSheet("background-color: #16161e; border-right: 1px solid #24283b;")
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        
        sm_label = QLabel("PROJECT MINIMAP")
        sm_label.setStyleSheet("color: #7aa2f7; font-weight: 900; font-size: 10px; letter-spacing: 2px; margin-bottom: 10px;")
        self.sidebar_layout.addWidget(sm_label)
        
        # Minimap Placeholder (Visual representation of files/logic)
        self.minimap_frame = QFrame()
        self.minimap_frame.setFixedHeight(200)
        self.minimap_frame.setStyleSheet("background: rgba(0, 242, 255, 0.05); border: 1px dashed rgba(0, 242, 255, 0.2); border-radius: 4px;")
        self.sidebar_layout.addWidget(self.minimap_frame)
        
        self.sidebar_layout.addStretch()
        
        ts_label = QLabel("TECH STACK")
        ts_label.setStyleSheet("color: #bb9af7; font-weight: 900; font-size: 10px; letter-spacing: 2px; margin-top: 20px;")
        self.sidebar_layout.addWidget(ts_label)
        
        stack_items = ["Unreal Engine 5.7", "Metal 3 Native", "Context 7 Protocol", "PySide6 HUD", "LlamaIndex RAG"]
        for item in stack_items:
            sl = QLabel(f"• {item}")
            sl.setStyleSheet("color: #737aa2; font-size: 11px; padding-left: 5px;")
            self.sidebar_layout.addWidget(sl)
            
        self.sidebar_layout.addStretch()
        self.main_layout.addWidget(self.sidebar)

        # 2. Workspace (The flexible area)
        self.workspace = QScrollArea()
        self.workspace.setWidgetResizable(True)
        self.workspace.setStyleSheet("border: none; background-color: #0c0d14;")
        self.workspace_content = QWidget()
        self.workspace_layout = QVBoxLayout(self.workspace_content)
        self.workspace_layout.setContentsMargins(20, 20, 20, 20)
        self.workspace_layout.setSpacing(20)
        
        # Add Workflow Planner placeholder (Large bubble or diagram)
        self.planner_frame = QFrame()
        self.planner_frame.setMinimumHeight(400)
        self.planner_frame.setStyleSheet("""
            QFrame {
                background: rgba(139, 92, 246, 0.05); 
                border: 1px solid rgba(139, 92, 246, 0.3); 
                border-radius: 12px;
            }
            QFrame:hover {
                background: rgba(139, 92, 246, 0.1);
                border: 1px solid rgba(0, 242, 255, 0.5);
            }
        """)
        p_layout = QVBoxLayout(self.planner_frame)
        p_layout.setAlignment(Qt.AlignCenter)
        
        # Big Sync Button
        self.sync_btn = QPushButton("🚀 SYNC UNREAL TWIN")
        self.sync_btn.setFixedSize(300, 80)
        self.sync_btn.setStyleSheet("""
            QPushButton {
                background-color: #8b5cf6;
                color: white;
                font-weight: 900;
                font-size: 18px;
                border-radius: 8px;
                letter-spacing: 2px;
            }
            QPushButton:hover {
                background-color: #7c3aed;
                border: 2px solid #00f2ff;
            }
            QPushButton:pressed {
                background-color: #6d28d9;
            }
        """)
        self.sync_btn.clicked.connect(self.launch_unreal_one_click)
        p_layout.addWidget(self.sync_btn)
        
        p_label = QLabel("Click to manifest the Neural Graphics Lab & Engine Twins")
        p_label.setStyleSheet("color: #737aa2; font-weight: 500; font-size: 12px; margin-top: 10px;")
        p_layout.addWidget(p_label, alignment=Qt.AlignCenter)
        
        self.workspace_layout.addWidget(self.planner_frame)
        
        self.workspace.setWidget(self.workspace_content)
        self.main_layout.addWidget(self.workspace)

        # Create Menu Bar
        self._create_menu_bar()

    def _create_menu_bar(self):
        menubar = self.menuBar()
        
        # File Menu
        file_menu = menubar.addMenu("File")
        save_action = QAction("Save Level Snapshot", self)
        save_action.triggered.connect(lambda: print("Saving Level..."))
        file_menu.addAction(save_action)
        
        # Edit Menu
        edit_menu = menubar.addMenu("Edit")
        
        # Window Menu (Launcher for our components)
        window_menu = menubar.addMenu("Window")
        
        # Launch Status Monitor
        mon_action = QAction("Universe Status Monitor", self)
        mon_action.triggered.connect(self.launch_monitor)
        window_menu.addAction(mon_action)
        
        # Launch Notifications
        notif_action = QAction("Notification Stack", self)
        notif_action.triggered.connect(self.launch_notifications)
        window_menu.addAction(notif_action)

        # Tools Menu
        tools_menu = menubar.addMenu("Tools")
        
        sync_action = QAction("Sync Unreal Twin", self)
        sync_action.triggered.connect(self.launch_unreal_one_click)
        tools_menu.addAction(sync_action)
        
        vis_action = QAction("Visualizer Mode (--visualizer)", self)
        vis_action.triggered.connect(self.launch_visualizer)
        tools_menu.addAction(vis_action)

    def launch_monitor(self):
        cmd = ["/Users/joeywalter/antigravity-nexus/shader_overlay/venv/bin/python3", "/Users/joeywalter/antigravity-nexus/shader_overlay/universe_monitor.py"]
        subprocess.Popen(cmd, start_new_session=True)

    def launch_notifications(self):
        cmd = ["/Users/joeywalter/antigravity-nexus/shader_overlay/venv/bin/python3", "/Users/joeywalter/antigravity-nexus/shader_overlay/nexus_notifier.py"]
        subprocess.Popen(cmd, start_new_session=True)

    def launch_visualizer(self):
        cmd = ["/Users/joeywalter/antigravity-nexus/shader_overlay/venv/bin/python3", "/Users/joeywalter/antigravity-nexus/shader_overlay/visualizer_launcher.py"]
        subprocess.Popen(cmd, start_new_session=True)

    def launch_unreal_one_click(self):
        cmd = ["/Users/joeywalter/antigravity-nexus/shader_overlay/venv/bin/python3", "/Users/joeywalter/antigravity-nexus/shader_overlay/nexus_one_click.py"]
        subprocess.Popen(cmd, start_new_session=True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    editor = NexusMasterEditor()
    editor.show()
    sys.exit(app.exec())
