import sys
import subprocess
import os
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, 
                             QPushButton, QWidget, QLabel, QHBoxLayout)

class UnrealLauncherOverlay(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Unreal Tactical Instance")
        
        # Frameless, Always on Top, Full Screen Rounded Overlay
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | 
            Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Get screen size and set large rounded window
        screen = QApplication.primaryScreen().geometry()
        margin = 80
        self.setGeometry(margin, margin, screen.width() - margin*2, screen.height() - margin*2)
        
        # Central Widget with rounded styling
        self.central = QWidget()
        self.central.setStyleSheet("""
            QWidget {
                background: rgba(10, 15, 25, 0.95);
                border-radius: 30px;
                border: 1px solid rgba(59, 130, 246, 0.4);
            }
        """)
        self.setCentralWidget(self.central)
        
        self.layout = QVBoxLayout(self.central)
        self.layout.setContentsMargins(60, 60, 60, 60)
        self.layout.setSpacing(20)
        
        # Header
        title = QLabel("TACTICAL INSTANCE")
        title.setStyleSheet("font-size: 28px; font-weight: 900; color: #3b82f6; letter-spacing: 4px; border: none; background: transparent;")
        self.layout.addWidget(title)
        
        subtitle = QLabel("SELECT UNREAL ENGINE 5.7 PROJECT")
        subtitle.setStyleSheet("font-size: 12px; color: rgba(255,255,255,0.4); letter-spacing: 2px; border: none; background: transparent;")
        self.layout.addWidget(subtitle)
        
        self.layout.addSpacing(40)
        
        # Projects
        self.projects = [
            ("ProjectAnywhereXR", "/Users/joeywalter/Documents/Unreal Projects/ProjectAnywhereXR/ProjectAnywhereXR.uproject", "XR/VR Interactive Demo"),
            ("PixelStreamingDemo", "/Users/joeywalter/Documents/Unreal Projects/PixelStreamingDemo/PixelStreamingDemo.uproject", "Pixel Streaming Server"),
            ("UIMaterialLab", "/Users/joeywalter/Documents/Unreal Projects/UIMaterialLab/UIMaterialLab.uproject", "Material & UI Testing"),
            ("MyProject", "/Users/joeywalter/Documents/Unreal Projects/MyProject/MyProject.uproject", "Default Project Template")
        ]
        
        for name, path, desc in self.projects:
            btn = QPushButton()
            btn.setFixedHeight(90)
            btn.setStyleSheet("""
                QPushButton {
                    background: rgba(255,255,255,0.03);
                    border: 1px solid rgba(255,255,255,0.08);
                    border-radius: 16px;
                    text-align: left;
                    padding-left: 30px;
                }
                QPushButton:hover {
                    background: rgba(59, 130, 246, 0.2);
                    border-color: #3b82f6;
                }
            """)
            
            btn_layout = QVBoxLayout(btn)
            btn_layout.setContentsMargins(30, 15, 30, 15)
            
            name_label = QLabel(name)
            name_label.setStyleSheet("font-size: 18px; font-weight: bold; color: white; border: none; background: transparent;")
            btn_layout.addWidget(name_label)
            
            desc_label = QLabel(desc)
            desc_label.setStyleSheet("font-size: 11px; color: rgba(255,255,255,0.5); border: none; background: transparent;")
            btn_layout.addWidget(desc_label)
            
            btn.clicked.connect(lambda checked, p=path: self.launch(p))
            self.layout.addWidget(btn)
        
        self.layout.addStretch()
        
        # Close button
        close_btn = QPushButton("ESC TO CLOSE")
        close_btn.setStyleSheet("background: transparent; color: rgba(255,255,255,0.3); border: none; font-size: 10px;")
        close_btn.clicked.connect(self.close)
        self.layout.addWidget(close_btn, alignment=Qt.AlignCenter)
        
        # Drag support
        self.old_pos = None

    def launch(self, project_path):
        editor = "/Users/Shared/Epic Games/UE_5.7/Engine/Binaries/Mac/UnrealEditor.app/Contents/MacOS/UnrealEditor"
        cmd = [editor, project_path, "-skipcompile"]
        try:
            subprocess.Popen(cmd)
            self.close()
        except Exception as e:
            print(f"Failed: {e}")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.close()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.old_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if self.old_pos:
            delta = event.globalPosition().toPoint() - self.old_pos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        self.old_pos = None

if __name__ == "__main__":
    os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--transparent-background"
    app = QApplication(sys.argv)
    window = UnrealLauncherOverlay()
    window.show()
    sys.exit(app.exec())
