import sys
import json
import os
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QGraphicsDropShadowEffect, QPushButton
from PySide6.QtCore import Qt, QTimer, QPoint, QSize, Property, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QColor, QPalette

class SuggestionBubble(QFrame):
    def __init__(self, title, description, callback_data):
        super().__init__()
        self.setObjectName("Bubble")
        self.setFixedSize(220, 180)
        self.callback_data = callback_data
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)
        
        self.title_label = QLabel(title.upper())
        self.title_label.setWordWrap(True)
        self.title_label.setStyleSheet("color: #00f2ff; font-weight: 900; font-size: 13px; letter-spacing: 1px; font-family: 'Helvetica';")
        
        self.desc_label = QLabel(description)
        self.desc_label.setWordWrap(True)
        self.desc_label.setStyleSheet("color: rgba(255, 255, 255, 0.7); font-size: 11px; font-family: 'Helvetica'; line-height: 14px;")
        
        self.action_btn = QPushButton("SELECT")
        self.action_btn.setStyleSheet("""
            QPushButton {
                background: rgba(0, 242, 255, 0.1);
                border: 1px solid rgba(0, 242, 255, 0.3);
                color: #00f2ff;
                font-weight: 800;
                font-size: 10px;
                border-radius: 4px;
                padding: 5px;
            }
            QPushButton:hover {
                background: rgba(0, 242, 255, 0.3);
            }
        """)
        
        layout.addWidget(self.title_label)
        layout.addWidget(self.desc_label)
        layout.addStretch()
        layout.addWidget(self.action_btn)
        
        self.setStyleSheet("""
            QFrame#Bubble {
                background: rgba(20, 25, 40, 0.95);
                border: 1px solid rgba(0, 242, 255, 0.2);
                border-radius: 20px;
            }
        """)
        
        # Shadow
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setXOffset(0)
        shadow.setYOffset(5)
        shadow.setColor(QColor(0, 0, 0, 150))
        self.setGraphicsEffect(shadow)

class VisualizerModeHUD(QWidget):
    def __init__(self, options_json):
        super().__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignCenter)
        
        # Mode Title
        self.title_frame = QFrame()
        self.title_frame.setFixedHeight(60)
        title_layout = QVBoxLayout(self.title_frame)
        title_layout.setAlignment(Qt.AlignCenter)
        
        mode_label = QLabel("VISUALIZER MODE: ARCHITECT LEVEL")
        mode_label.setStyleSheet("color: #8b5cf6; font-weight: 900; font-size: 18px; letter-spacing: 5px; font-family: 'Helvetica';")
        title_layout.addWidget(mode_label)
        
        self.main_layout.addWidget(self.title_frame)
        
        # Bubbles Container
        self.bubbles_layout = QHBoxLayout()
        self.bubbles_layout.setSpacing(25)
        
        options = json.loads(options_json)
        for opt in options:
            bubble = SuggestionBubble(opt['title'], opt['description'], opt['id'])
            self.bubbles_layout.addWidget(bubble)
            
        self.main_layout.addLayout(self.bubbles_layout)
        
        # Close Button
        self.close_btn = QPushButton("DISMISS")
        self.close_btn.setFixedWidth(120)
        self.close_btn.setStyleSheet("""
            QPushButton {
                background: rgba(255, 85, 85, 0.1);
                border: 1px solid rgba(255, 85, 85, 0.3);
                color: #ff5555;
                font-weight: 900;
                border-radius: 6px;
                padding: 10px;
                margin-top: 30px;
            }
            QPushButton:hover {
                background: rgba(255, 85, 85, 0.3);
            }
        """)
        self.close_btn.clicked.connect(self.close)
        self.main_layout.addWidget(self.close_btn, alignment=Qt.AlignCenter)
        
        self.showMaximized()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Read options from command line arg if provided
    options_json = ""
    if len(sys.argv) > 1:
        options_json = sys.argv[1]
    else:
        # Default fallback
        test_options = [
            {"id": "opt1", "title": "Native Metal HUD", "description": "120 FPS physics overlay using raw Metal pipeline. Zero latency."},
            {"id": "opt2", "title": "UE Commandlet Sub", "description": "Headless Unreal instance driving physics calculations via socket."},
            {"id": "opt3", "title": "Webkit Streamer", "description": "Three.js physics sim streamed from an isolated cloud instance."},
            {"id": "opt4", "title": "Local Venv Simulation", "description": "Python-based physics using PyBullet or Manim in a secondary window."}
        ]
        options_json = json.dumps(test_options)
        
    hud = VisualizerModeHUD(options_json)
    sys.exit(app.exec())
