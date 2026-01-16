import sys
import json
import os
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QGraphicsDropShadowEffect
from PySide6.QtCore import Qt, QTimer, QPoint, QSize

# Explicit absolute path for the data file
STATE_FILE = "/Users/joeywalter/antigravity-nexus/shader_overlay/universe_state.json"

class NodeWidget(QFrame):
    def __init__(self, name, status, notes=""):
        super().__init__()
        self.setObjectName("NodeFrame")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(4)
        
        # Level-based Color Scheme (Accepted/Using=Green, Proposed=Yellow, Research=Grey, Notes/Failed=Red)
        colors = {
            "ACCEPTED": "#00FF88",  # Vibrant Green
            "USING": "#00FF88",
            "PROPOSED": "#FFEE00", # Neon Yellow
            "RESEARCH": "#A0A0A0", # Light Grey
            "NOTES": "#FF5555",    # Soft Red
            "FAILED": "#FF5555"
        }
        color = colors.get(status.upper(), "#FFFFFF")
        
        self.setStyleSheet(f"""
            QFrame#NodeFrame {{
                background: rgba(25, 25, 40, 0.95);
                border-left: 6px solid {color};
                border-radius: 6px;
                margin-bottom: 4px;
            }}
        """)
        
        h_head = QHBoxLayout()
        name_label = QLabel(name.upper())
        # Use a safe font fallback
        name_label.setStyleSheet("color: white; font-size: 12px; font-weight: 900; font-family: 'Helvetica', sans-serif; letter-spacing: 1px;")
        
        status_label = QLabel(status.upper())
        status_label.setStyleSheet(f"color: {color}; font-size: 10px; font-weight: 900; font-family: 'Helvetica'; letter-spacing: 2px;")
        
        h_head.addWidget(name_label)
        h_head.addStretch()
        h_head.addWidget(status_label)
        layout.addLayout(h_head)
        
        if notes:
            note_label = QLabel(notes)
            note_label.setStyleSheet("color: rgba(255, 255, 255, 0.6); font-size: 10px; font-style: normal; font-family: 'Helvetica';")
            note_label.setWordWrap(True)
            layout.addWidget(note_label)

class AntigravityUniverseMonitor(QWidget):
    def __init__(self):
        super().__init__()
        # Mac-Friendly Native HUD Flags
        self.setWindowFlags(
            Qt.WindowStaysOnTopHint | 
            Qt.FramelessWindowHint | 
            Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        # High-Fidelity Header
        self.header = QFrame()
        self.header.setFixedHeight(50)
        self.header.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 rgba(0, 242, 255, 0.3), stop:1 rgba(0, 100, 255, 0.3));
            border-top-left-radius: 15px;
            border-top-right-radius: 15px;
            border-bottom: 1px solid rgba(0, 242, 255, 0.5);
        """)
        h_layout = QHBoxLayout(self.header)
        h_layout.setContentsMargins(20, 0, 20, 0)
        
        title = QLabel("NEXUS UNIVERSE STATUS")
        title.setStyleSheet("color: #00f2ff; font-weight: 900; font-size: 14px; letter-spacing: 4px; font-family: 'Helvetica';")
        h_layout.addWidget(title)
        
        self.main_layout.addWidget(self.header)
        
        # Content Scroll Area
        self.content = QFrame()
        self.content.setStyleSheet("""
            background: rgba(5, 5, 10, 0.98);
            border-bottom-left-radius: 15px;
            border-bottom-right-radius: 15px;
            border: 1px solid rgba(255, 255, 255, 0.05);
        """)
        self.list_layout = QVBoxLayout(self.content)
        self.list_layout.setContentsMargins(15, 20, 15, 20)
        self.list_layout.setSpacing(10)
        self.list_layout.addStretch() 
        
        self.main_layout.addWidget(self.content)
        
        # Shadow for that "Floating" look
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(30)
        shadow.setXOffset(0)
        shadow.setYOffset(15)
        shadow.setColor(Qt.black)
        self.setGraphicsEffect(shadow)
        
        self.setFixedSize(360, 520)
        self.drag_pos = QPoint()

        # Update Timer (check for state changes every second)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.reload_state)
        self.timer.start(1000)
        
        self.reload_state()
        
        # Centered or Top Right position
        screen_geo = QApplication.primaryScreen().availableGeometry()
        self.move(screen_geo.width() - 380, 80)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_pos)
            event.accept()

    def reload_state(self):
        # Clear existing nodes
        for i in reversed(range(self.list_layout.count())):
            item = self.list_layout.itemAt(i)
            if item.widget():
                item.widget().deleteLater()
        
        self.list_layout.addStretch()
        
        if not os.path.exists(STATE_FILE):
            return
            
        try:
            with open(STATE_FILE, "r") as f:
                data = json.load(f)
                
            for node in data.get("nodes", []):
                widget = NodeWidget(node.get("name"), node.get("status"), node.get("notes", ""))
                self.list_layout.insertWidget(0, widget)
                
        except Exception:
            pass

    def closeEvent(self, event):
        event.ignore()
        print("Universe Monitor is eternal.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False) # Keep agent alive
    monitor = AntigravityUniverseMonitor()
    monitor.show()
    app.exec()
