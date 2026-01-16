import sys
import os
import json
import time
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QFrame, QProgressBar, QGraphicsDropShadowEffect)
from PySide6.QtCore import Qt, QTimer, Property, QRect, QPoint, QSize
from PySide6.QtGui import QColor, QFont, QPainter, QLinearGradient, QBrush, QPen, QRadialGradient

# Shared State Path
STATE_PATH = "/Users/joeywalter/antigravity-nexus/shader_overlay/universe_state.json"

class QuantumProgressBar(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumHeight(12)
        self.progress = 15 # Start at 15% immediately for visibility
        self.glow_offset = 0
        
        # Animation timer for the "flowing" glow effect
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate_glow)
        self.timer.start(30)

    def set_value(self, val):
        self.progress = max(0, min(100, val))
        self.update()

    def animate_glow(self):
        self.glow_offset = (self.glow_offset + 5) % 400
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # 1. Background (Deep Glass)
        bg_rect = self.rect()
        painter.setBrush(QColor(15, 23, 42, 180))
        painter.setPen(QPen(QColor(255, 255, 255, 20), 1))
        painter.drawRoundedRect(bg_rect, 6, 6)
        
        if self.progress <= 0:
            return

        # 2. Progress Fill (3D Gradient)
        fill_width = int((self.progress / 100.0) * self.width())
        fill_rect = QRect(0, 0, fill_width, self.height())
        
        gradient = QLinearGradient(0, 0, fill_width, 0)
        gradient.setColorAt(0, QColor(139, 92, 246)) # Violet
        gradient.setColorAt(0.5, QColor(99, 102, 241)) # Indigo
        gradient.setColorAt(1, QColor(6, 182, 212))   # Cyan
        
        painter.setBrush(QBrush(gradient))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(fill_rect, 6, 6)
        
        # 3. Floating Highlight (3D Effect)
        highlight_rect = QRect(0, 1, fill_width, self.height() // 3)
        h_gradient = QLinearGradient(0, 0, 0, highlight_rect.height())
        h_gradient.setColorAt(0, QColor(255, 255, 255, 40))
        h_gradient.setColorAt(1, QColor(255, 255, 255, 0))
        painter.setBrush(QBrush(h_gradient))
        painter.drawRoundedRect(highlight_rect, 4, 4)
        
        # 4. Scanning Glow Tip
        if self.progress < 100:
            tip_rect = QRect(fill_width - 20, 0, 40, self.height())
            tip_gradient = QRadialGradient(fill_width, self.height()/2, 20)
            tip_gradient.setColorAt(0, QColor(255, 255, 255, 120))
            tip_gradient.setColorAt(1, Qt.transparent)
            painter.setBrush(QBrush(tip_gradient))
            painter.drawRect(tip_rect)

class QuantumHUD(QMainWindow):
    def __init__(self):
        super().__init__()
        # Set window properties: Top persistent bar
        screen = QApplication.primaryScreen().geometry()
        width = 800
        height = 80
        self.setGeometry((screen.width() - width) // 2, 20, width, height)
        
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Main Widget Container
        self.container = QFrame()
        self.container.setObjectName("MainContainer")
        self.container.setStyleSheet("""
            #MainContainer {
                background: rgba(10, 15, 25, 120);
                border-radius: 20px;
                border: 1px solid rgba(255, 255, 255, 10);
            }
        """)
        
        # Inner Layout
        layout = QVBoxLayout(self.container)
        layout.setContentsMargins(30, 15, 30, 15)
        layout.setSpacing(8)
        
        # Header Row
        header_layout = QHBoxLayout()
        
        self.label_task = QLabel("NEURAL ARCHITECTURE SYNCING...")
        self.label_task.setFont(QFont("Outfit", 14, QFont.Bold))
        self.label_task.setStyleSheet("color: white; letter-spacing: 2px;")
        
        self.label_percent = QLabel("0%")
        self.label_percent.setFont(QFont("Outfit", 12, QFont.Bold))
        self.label_percent.setStyleSheet("color: #06b6d4;")
        
        header_layout.addWidget(self.label_task)
        header_layout.addStretch()
        header_layout.addWidget(self.label_percent)
        layout.addLayout(header_layout)
        
        # 3D Progress Bar
        self.bar = QuantumProgressBar()
        layout.addWidget(self.bar)
        
        # Status Subtitle
        self.label_status = QLabel("Initializing manifestation buffers...")
        self.label_status.setFont(QFont("Inter", 9))
        self.label_status.setStyleSheet("color: #94a3b8;")
        layout.addWidget(self.label_status)
        
        self.setCentralWidget(self.container)
        
        # Poll State Timer
        self.poll_timer = QTimer(self)
        self.poll_timer.timeout.connect(self.update_state)
        self.poll_timer.start(100) # 10Hz polling
        
        # Shadow Effect
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(30)
        shadow.setColor(QColor(0, 0, 0, 150))
        shadow.setOffset(0, 10)
        self.container.setGraphicsEffect(shadow)

    def closeEvent(self, event):
        # HUD is eternal
        event.ignore()

    def update_state(self):
        try:
            if os.path.exists(STATE_PATH):
                with open(STATE_PATH, 'r') as f:
                    state = json.load(f)
                
                manifest = state.get("manifestation", {})
                progress = manifest.get("progress", 0)
                status = manifest.get("status", "System Idle")
                mission = manifest.get("active_mission", "Neural Core")
                
                self.bar.set_value(progress)
                self.label_percent.setText(f"{progress}%")
                self.label_status.setText(status.upper())
                self.label_task.setText(f"MANIFESTING: {mission.upper()}")
                
                if progress >= 100:
                    self.label_percent.setStyleSheet("color: #22c55e;") # Green success
                    self.label_status.setText("NEURAL SYNC COMPLETE.")
        except Exception as e:
            pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    hud = QuantumHUD()
    hud.show()
    sys.exit(app.exec())
