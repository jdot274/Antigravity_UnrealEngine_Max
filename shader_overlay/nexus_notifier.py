import sys
import os
import json
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QFrame, QGraphicsDropShadowEffect)
from PySide6.QtCore import Qt, QTimer, QPoint, Property, QPropertyAnimation, QEasingCurve, QRect

class NotificationCard(QFrame):
    def __init__(self, title, message, type="INFO"):
        super().__init__()
        self.setFixedSize(300, 80)
        self.setObjectName("Notification")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 10, 15, 10)
        layout.setSpacing(2)
        
        color = "#00f2ff" # Cyan
        if type == "SUCCESS": color = "#00ff88"
        elif type == "WARNING": color = "#ffee00"
        elif type == "ERROR": color = "#ff5555"
        elif type == "TOOL": color = "#8b5cf6"
        
        self.setStyleSheet(f"""
            QFrame#Notification {{
                background: rgba(20, 20, 35, 0.95);
                border-left: 4px solid {color};
                border-radius: 8px;
            }}
        """)
        
        h_head = QHBoxLayout()
        t_label = QLabel(title.upper())
        t_label.setStyleSheet(f"color: {color}; font-weight: 900; font-size: 10px; letter-spacing: 1px; font-family: 'Helvetica';")
        h_head.addWidget(t_label)
        h_head.addStretch()
        layout.addLayout(h_head)
        
        m_label = QLabel(message)
        m_label.setWordWrap(True)
        m_label.setStyleSheet("color: white; font-size: 11px; font-family: 'Helvetica';")
        layout.addWidget(m_label)

        # Shadow
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(10)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(Qt.black)
        self.setGraphicsEffect(shadow)

class NexusNotifier(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool | Qt.WindowTransparentForInput)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(10)
        self.layout.setAlignment(Qt.AlignBottom | Qt.AlignRight)
        
        self.cards = []
        
        # Position at bottom right
        screen = QApplication.primaryScreen().availableGeometry()
        self.setGeometry(screen.width() - 320, 0, 310, screen.height())

    def notify(self, title, message, type="INFO"):
        card = NotificationCard(title, message, type)
        self.layout.insertWidget(0, card)
        self.cards.append(card)
        
        # Auto fade/remove
        QTimer.singleShot(5000, lambda: self.remove_card(card))

    def remove_card(self, card):
        if card in self.cards:
            self.layout.removeWidget(card)
            card.deleteLater()
            self.cards.remove(card)

# Global Instance logic for inter-process comms
NOTIFIER_PIPE = "/Users/joeywalter/antigravity-nexus/shader_overlay/notifier_queue.json"

class NexusWatcher(QWidget):
    def __init__(self, notifier):
        super().__init__()
        self.notifier = notifier
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_queue)
        self.timer.start(500)
        
    def check_queue(self):
        if os.path.exists(NOTIFIER_PIPE):
            try:
                with open(NOTIFIER_PIPE, "r") as f:
                    notifications = json.load(f)
                
                # Clear the pipe
                with open(NOTIFIER_PIPE, "w") as f:
                    json.dump([], f)
                    
                for n in notifications:
                    self.notifier.notify(n['title'], n['message'], n.get('type', 'INFO'))
            except Exception:
                pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    notifier = NexusNotifier()
    notifier.show()
    
    # Initialize Watcher to listen for external tool calls
    watcher = NexusWatcher(notifier)
    
    # Test notification
    notifier.notify("SYSTEM INITIALIZED", "Nexus Notifier is now persistent across the stack.", "SUCCESS")
    
    sys.exit(app.exec())
