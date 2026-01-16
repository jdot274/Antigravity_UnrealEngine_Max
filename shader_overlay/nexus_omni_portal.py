import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import Qt, QUrl

class NexusOmniPortal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ANTIGRAVITY OMNI PORTAL")
        
        # Transparent, frameless, stay-on-top
        self.setWindowFlags(
            Qt.FramelessWindowHint | 
            Qt.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Full screen reveal
        screen = QApplication.primaryScreen().geometry()
        self.setGeometry(screen)
        
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0,0,0,0)
        
        self.browser = QWebEngineView()
        self.browser.page().setBackgroundColor(Qt.transparent)
        
        # Load the central hub
        hub_path = "/Users/joeywalter/antigravity-nexus/shader_overlay/nexus_hub.html"
        self.browser.setUrl(QUrl.fromLocalFile(hub_path))
        
        layout.addWidget(self.browser)
        self.setCentralWidget(container)

    def closeEvent(self, event):
        event.ignore()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    portal = NexusOmniPortal()
    portal.show()
    sys.exit(app.exec())
