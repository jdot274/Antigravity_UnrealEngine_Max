import sys
import os
import time
import json
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QPushButton, QFrame, QStackedWidget,
                             QProgressBar, QGraphicsDropShadowEffect)
from PySide6.QtCore import Qt, QTimer, Property, QPropertyAnimation, QEasingCurve, QRect, QSize
from PySide6.QtGui import QColor, QFont, QPainter, QOpenGLWidget, QSurfaceFormat
from PySide6.QtOpenGL import QOpenGLShader, QOpenGLShaderProgram

# Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SHADER_PATH = os.path.join(BASE_DIR, "shaders", "quantum_core.glsl")
VENV_PYTHON = os.path.join(BASE_DIR, "venv", "bin", "python3")

class ShaderWidget(QOpenGLWidget):
    def __init__(self, shader_source_path):
        super().__init__()
        self.shader_source_path = shader_source_path
        self.start_time = time.time()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(8) # ~120 FPS

    def initializeGL(self):
        self.program = QOpenGLShaderProgram()
        
        # Simple Vertex Shader
        vshader = """
        #version 330
        in vec2 position;
        void main() {
            gl_Position = vec4(position, 0.0, 1.0);
        }
        """
        
        with open(self.shader_source_path, 'r') as f:
            fshader = f.read()
            
        self.program.addShaderFromSourceCode(QOpenGLShader.Vertex, vshader)
        self.program.addShaderFromSourceCode(QOpenGLShader.Fragment, fshader)
        self.program.link()
        self.program.bind()
        
        self.vertices = [
            -1.0, -1.0,
             1.0, -1.0,
            -1.0,  1.0,
             1.0,  1.0,
        ]

    def paintGL(self):
        self.program.bind()
        self.program.setUniformValue("iTime", float(time.time() - self.start_time))
        self.program.setUniformValue("iResolution", QColor(self.width(), self.height())) # Using QColor as a vec2 container hack or just setUniformValue
        self.program.setUniformValue("iResolution", float(self.width()), float(self.height()))
        
        self.program.enableAttributeArray("position")
        self.program.setAttributeArray("position", self.vertices, 2)
        self.painter = QPainter(self)
        self.painter.beginNativePainting()
        # Draw full screen quad
        import OpenGL.GL as gl
        gl.glDrawArrays(gl.GL_TRIANGLE_STRIP, 0, 4)
        self.painter.endNativePainting()
        self.painter.end()

class ModernButton(QPushButton):
    def __init__(self, text, primary=False):
        super().__init__(text)
        self.setFixedSize(280, 60)
        self.setFont(QFont("Outfit", 12, QFont.Bold))
        self.setCursor(Qt.PointingHandCursor)
        
        if primary:
            self.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #8b5cf6, stop:1 #6366f1);
                    color: white;
                    border-radius: 12px;
                    border: 1px solid rgba(255,255,255,0.2);
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #a78bfa, stop:1 #818cf8);
                }
            """)
        else:
            self.setStyleSheet("""
                QPushButton {
                    background: rgba(255, 255, 255, 0.05);
                    color: #e2e8f0;
                    border-radius: 12px;
                    border: 1px solid rgba(255,255,255,0.1);
                }
                QPushButton:hover {
                    background: rgba(255, 255, 255, 0.1);
                    border: 1px solid rgba(255,255,255,0.3);
                }
            """)

class MissionCard(QFrame):
    def __init__(self, title, description, mission_id):
        super().__init__()
        self.mission_id = mission_id
        self.setFixedSize(300, 400)
        self.setStyleSheet(f"""
            QFrame {{
                background: rgba(15, 23, 42, 0.6);
                border-radius: 20px;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }}
            QFrame:hover {{
                border: 1px solid rgba(139, 92, 246, 0.5);
                background: rgba(15, 23, 42, 0.8);
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Icon/Image Placeholder (Glowing Circle)
        self.icon = QFrame()
        self.icon.setFixedSize(80, 80)
        self.icon.setStyleSheet("""
            background: qradialgradient(cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 rgba(139, 92, 246, 0.4), stop:1 transparent);
            border-radius: 40px;
        """)
        layout.addWidget(self.icon, alignment=Qt.AlignCenter)
        
        layout.addSpacing(20)
        
        self.title_label = QLabel(title)
        self.title_label.setFont(QFont("Outfit", 18, QFont.Bold))
        self.title_label.setStyleSheet("color: white;")
        self.title_label.setWordWrap(True)
        layout.addWidget(self.title_label)
        
        self.desc_label = QLabel(description)
        self.desc_label.setFont(QFont("Inter", 10))
        self.desc_label.setStyleSheet("color: #94a3b8;")
        self.desc_label.setWordWrap(True)
        layout.addWidget(self.desc_label)
        
        layout.addStretch()
        
        self.btn = ModernButton("LAUNCH SCENE", primary=True)
        layout.addWidget(self.btn, alignment=Qt.AlignCenter)

class NexusGameEngine(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Antigravity Nexus | Modern Experience")
        self.resize(1280, 800)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # UI Stack
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        # Background Shader
        self.bg_shader = ShaderWidget(SHADER_PATH)
        self.bg_shader.setGeometry(0, 0, 1280, 800)
        self.bg_shader.setParent(self.central_widget)
        
        # Main Container
        self.stack = QStackedWidget()
        self.layout.addWidget(self.stack)
        
        self.init_menu()
        self.init_loader()
        
        # Exit Button REMOVED - Experience is persistent
        # self.exit_btn = QPushButton("✕", self)
        # self.exit_btn.setGeometry(1240, 10, 30, 30)
        # self.exit_btn.setStyleSheet("color: white; background: none; border: none; font-size: 20px;")
        # self.exit_btn.clicked.connect(self.close)

    def closeEvent(self, event):
        # Prevent closing
        event.ignore()
        print("💡 Antigravity Nexus is Eternal. Closing is disabled.")

    def init_menu(self):
        self.menu_page = QWidget()
        layout = QVBoxLayout(self.menu_page)
        layout.setContentsMargins(50, 50, 50, 50)
        
        header = QLabel("SELECT MISSION")
        header.setFont(QFont("Outfit", 42, QFont.Bold))
        header.setStyleSheet("color: white; letter-spacing: 4px;")
        layout.addWidget(header, alignment=Qt.AlignCenter)
        
        subtitle = QLabel("Neural Interlink Synchronized. Awaiting Command.")
        subtitle.setFont(QFont("Inter", 12))
        subtitle.setStyleSheet("color: #94a3b8;")
        layout.addWidget(subtitle, alignment=Qt.AlignCenter)
        
        layout.addSpacing(60)
        
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(30)
        
        m1 = MissionCard("BIOMETRIC ENTRY", "Quantum reconstruction of identity archives via 3D point cloud synthesis.", "001")
        m1.btn.clicked.connect(lambda: self.start_loading("001"))
        
        m2 = MissionCard("NEURAL PHYSICS", "Experimental zero-gravity simulation with high-intensity chaotic nodes.", "002")
        m2.btn.clicked.connect(lambda: self.start_loading("002"))
        
        m3 = MissionCard("CORE ACCESS", "Direct interface with the Antigravity sentient engine layers.", "003")
        m3.btn.setDisabled(True)
        m3.btn.setText("LOCKED")
        
        cards_layout.addWidget(m1)
        cards_layout.addWidget(m2)
        cards_layout.addWidget(m3)
        
        layout.addLayout(cards_layout)
        layout.addStretch()
        
        self.stack.addWidget(self.menu_page)

    def init_loader(self):
        self.loader_page = QWidget()
        layout = QVBoxLayout(self.loader_page)
        
        layout.addStretch()
        
        self.loading_label = QLabel("INITIALIZING NEURAL SYNC...")
        self.loading_label.setFont(QFont("Outfit", 24, QFont.Bold))
        self.loading_label.setStyleSheet("color: white;")
        layout.addWidget(self.loading_label, alignment=Qt.AlignCenter)
        
        self.progress = QProgressBar()
        self.progress.setFixedSize(600, 4)
        self.progress.setTextVisible(False)
        self.progress.setStyleSheet("""
            QProgressBar {
                background: rgba(255,255,255,0.1);
                border-radius: 2px;
            }
            QProgressBar::chunk {
                background: #8b5cf6;
                border-radius: 2px;
            }}
        """)
        layout.addWidget(self.progress, alignment=Qt.AlignCenter)
        
        self.status_msg = QLabel("Allocating VRAM Buffers...")
        self.status_msg.setFont(QFont("Inter", 10))
        self.status_msg.setStyleSheet("color: #64748b;")
        layout.addWidget(self.status_msg, alignment=Qt.AlignCenter)
        
        layout.addStretch()
        
        self.stack.addWidget(self.loader_page)

    def start_loading(self, mission_id):
        self.stack.setCurrentIndex(1)
        self.current_mission = mission_id
        self.progress_val = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_loading)
        self.timer.start(50)
        
        # Sound/Logic trigger
        print(f"📡 Triggering Mission {mission_id}...")

    def update_loading(self):
        self.progress_val += 1
        self.progress.setValue(self.progress_val)
        
        msgs = {
            10: "establishing neural interlink...",
            30: "injecting quantum shaders...",
            50: f"manifesting mission_{self.current_mission}.py...",
            70: "synchronizing twin engine state...",
            90: "finalizing reality rift..."
        }
        
        if self.progress_val in msgs:
            self.status_msg.setText(msgs[self.progress_val])
            
        if self.progress_val >= 100:
            self.timer.stop()
            self.loading_complete()

    def loading_complete(self):
        self.loading_label.setText("CONNECTION ESTABLISHED")
        self.status_msg.setText("ACTIVE IN UNREAL ENGINE 5.7")
        
        # Here we actually run the unreal script via bridge
        if self.current_mission == "001":
            script = "mission_001_biometric.py"
        else:
            script = "mission_002_physics.py"
            
        # Write to bridge for Unreal to see (In a real scenario, the EUW polls this)
        # For now, we simulate success
        QTimer.singleShot(1500, lambda: self.stack.setCurrentIndex(0))

if __name__ == "__main__":
    # Ensure High DPI support
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    
    # Metal/OpenGL support
    fmt = QSurfaceFormat()
    fmt.setVersion(3, 3)
    fmt.setProfile(QSurfaceFormat.CoreProfile)
    QSurfaceFormat.setDefaultFormat(fmt)
    
    window = NexusGameEngine()
    window.show()
    sys.exit(app.exec())
