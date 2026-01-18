import sys
import subprocess
import os
from PySide6.QtCore import Qt, QSize, QThread, Signal, QPropertyAnimation, QByteArray, QEasingCurve, QUrl, QRect
from PySide6.QtGui import QColor, QPalette, QFont, QLinearGradient, QGradient, QBrush, QPainter, QPen
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QPushButton, QLabel, QFrame, QGraphicsDropShadowEffect,
                               QScrollArea, QSizePolicy, QTextEdit)

# Try imports
try:
    from PySide6.QtWebEngineWidgets import QWebEngineView
    WEB_ENGINE_AVAILABLE = True
except ImportError:
    WEB_ENGINE_AVAILABLE = False

# --- Style Constants (System B: Radial 2d3d / Apple Icon Style) ---
STYLE_BG_COLOR = "#000000" # Pure black
STYLE_TEXT_PRIMARY = "#FFFFFF"
STYLE_TEXT_SECONDARY = "#8E8E93"
STYLE_FONT_FAMILY = ".AppleSystemUIFont"

# "2d3d" Gradient Colors - Distinct, Solid, Vibrant
STYLE_GRADIENTS = {
    "build": ("#FF9500", "#FF5E3A"), # Orange -> Red
    "launch": ("#34C759", "#30B0C7"), # Green -> Teal
    "assets": ("#AF52DE", "#5856D6"), # Purple -> Indigo
    "default": ("#1C1C1E", "#2C2C2E"), # Dark Gray
    "magnetic": ("#FFD60A", "#FF9F0A")  # Gold (Suggested Action)
}

STYLE_SHEET = f"""
QMainWindow {{
    background-color: {STYLE_BG_COLOR};
}}
QLabel {{
    color: {STYLE_TEXT_PRIMARY};
    font-family: '{STYLE_FONT_FAMILY}';
}}
QTextEdit {{
    background-color: #1C1C1E;
    color: #FFFFFF;
    border: 1px solid #333;
    border-radius: 16px;
    padding: 15px;
    font-family: 'Monaco', monospace;
    font-size: 13px;
}}
"""

# --- Worker Thread ---
class CommandWorker(QThread):
    output_signal = Signal(str)
    finished_signal = Signal(int)

    def __init__(self, command, cwd):
        super().__init__()
        self.command = command
        self.cwd = cwd

    def run(self):
        try:
            process = subprocess.Popen(
                self.command,
                cwd=self.cwd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                shell=True
            )
            for line in process.stdout:
                self.output_signal.emit(line)
            process.wait()
            self.finished_signal.emit(process.returncode)
        except Exception as e:
            self.output_signal.emit(f"Error: {str(e)}")
            self.finished_signal.emit(1)

# --- Premium Card (Radial 2d3d) ---
class PremiumCard(QPushButton):
    def __init__(self, title, subtitle, icon, gradient_key="default", parent=None):
        super().__init__(parent)
        self.title = title
        self.subtitle = subtitle
        self.icon_emoji = icon
        self.base_gradient_key = gradient_key
        self.current_gradient_key = gradient_key
        self.is_magnetic = False
        self.is_hovered = False
        
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedHeight(160)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        # Shadow: Solid depth, no bloom
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setOffset(0, 8) 
        shadow.setColor(QColor(0, 0, 0, 150))
        self.setGraphicsEffect(shadow)

    def set_magnetic_state(self, active):
        """Activates 'Magnetic' draw mode to guide user"""
        if self.is_magnetic == active:
            return
        self.is_magnetic = active
        # Pulse animation could be added here if needed, but static for now is clean.
        self.update()

    def enterEvent(self, event):
        self.is_hovered = True
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.is_hovered = False
        self.update()
        super().leaveEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = self.rect()

        # GT / Lyra Style Colors
        # Base is dark, glass-like. Highlights are sharp.
        is_down = self.isDown() or self.isChecked()
        is_hovered = self.is_hovered and not is_down
        
        # 1. Background (Tech Glass)
        back_color = QColor(20, 20, 25, 240)
        if is_hovered:
            back_color = QColor(40, 40, 50, 250)
        elif is_down:
            back_color = QColor(10, 10, 15, 255)

        painter.setBrush(back_color)
        
        # Border
        border_color = QColor(60, 60, 70)
        if is_hovered:
            border_color = QColor(255, 255, 255, 200)
        elif self.is_magnetic:
            border_color = QColor(255, 215, 0) # Gold pulse
        
        pen = QPen(border_color)
        pen.setWidth(1 if not self.is_magnetic else 2)
        painter.setPen(pen)
        
        # Shape: Sharper corners (GT style)
        radius = 4
        painter.drawRoundedRect(rect, radius, radius)

        # 2. Magnetic Glow (Outer)
        if self.is_magnetic:
             glow_pen = QPen(QColor(255, 215, 0, 100))
             glow_pen.setWidth(6)
             painter.setPen(glow_pen)
             painter.setBrush(Qt.NoBrush)
             painter.drawRoundedRect(rect.adjusted(3,3,-3,-3), radius, radius)

        # 3. Content
        # Icon (Left Aligned, smaller)
        font = QFont(STYLE_FONT_FAMILY, 36)
        painter.setFont(font)
        painter.setPen(QColor(240, 240, 240))
        # GT requires precision layout
        icon_rect = QRect(20, 20, 60, 60)
        painter.drawText(icon_rect, Qt.AlignCenter, self.icon_emoji)

        # Title (Uppercase, Tracking)
        font.setPointSize(16)
        font.setBold(True)
        font.setLetterSpacing(QFont.AbsoluteSpacing, 1.5)
        painter.setFont(font)
        painter.setPen(QColor(255, 255, 255))
        
        title_rect = rect.adjusted(20, 0, -20, -50)
        painter.drawText(title_rect, Qt.AlignLeft | Qt.AlignBottom, self.title.upper())

        # Subtitle (Tech grey, smaller)
        font.setPointSize(10)
        font.setBold(False)
        font.setLetterSpacing(QFont.AbsoluteSpacing, 0.5)
        painter.setFont(font)
        painter.setPen(QColor(150, 150, 160))
        
        sub_rect = rect.adjusted(20, 0, -20, -25)
        painter.drawText(sub_rect, Qt.AlignLeft | Qt.AlignBottom, self.subtitle)

        # 4. Accent Bar (Bottom)
        # Each card type gets a colored strip at the bottom
        bar_colors = STYLE_GRADIENTS.get(self.base_gradient_key, STYLE_GRADIENTS["default"])
        bar_color = QColor(bar_colors[0])
        
        painter.setPen(Qt.NoPen)
        painter.setBrush(bar_color)
        # Narrow strip at bottom
        painter.drawRoundedRect(rect.x() + 4, rect.bottom() - 6, rect.width() - 8, 2, 1, 1)

    def set_magnetic_focus(self, target_btn):
        # ... existing implementation ...
        pass

# ... inside NexusDashboard methods ...

    def run_view3d(self):
        if not self.web_view: return
        
        # Toggle Logic
        if self.web_view.isVisible():
            self.web_view.setVisible(False)
            self.terminal.setVisible(True)
            self.status.setText("System B Design Active • Ready")
            self.log("Switched to Terminal View.\n")
        else:
            self.terminal.setVisible(False)
            self.web_view.setVisible(True)
            
            html_path = os.path.abspath(os.path.join(self.root_dir, "tools/dashboard/nexus-web-view/dist/index.html"))
            if self.web_view.url().toString() != QUrl.fromLocalFile(html_path).toString():
                 self.web_view.load(QUrl.fromLocalFile(html_path))
            
            self.log(f"Loading 3D View: {html_path}\n")
            self.status.setText("Mode: Spline Interactive View")

# --- Main Dashboard ---
class NexusDashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Antigravity Nexus Control")
        self.resize(1100, 750)
# ... (Imports)
    # ... inside NexusDashboard init ...
        # Frameless Window - The "Game Launcher" Look
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Main Container with Border (for visibility against dark desktop)
        container = QFrame()
        container.setObjectName("MainContainer")
        container.setStyleSheet(f"""
            #MainContainer {{
                background-color: {STYLE_BG_COLOR};
                border: 1px solid #333;
                border-radius: 20px;
            }}
        """)
        self.setCentralWidget(container)
        
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Custom Title Bar
        title_bar = QWidget()
        title_bar.setFixedHeight(60)
        title_layout = QHBoxLayout(title_bar)
        title_layout.setContentsMargins(30, 0, 30, 0)
        
        # Window Title
        header = QLabel("ANTIGRAVITY // NEXUS")
        header.setFont(QFont(STYLE_FONT_FAMILY, 14, QFont.Bold))
        header.setStyleSheet("letter-spacing: 2px; color: #888;")
        title_layout.addWidget(header)
        title_layout.addStretch()
        
        # Window Controls
        btn_close = QPushButton("×")
        btn_close.setFixedSize(40, 40)
        btn_close.clicked.connect(self.close)
        btn_close.setStyleSheet("""
            QPushButton {
                color: #666; font-size: 24px; border: none; background: transparent;
            }
            QPushButton:hover { color: #FFF; }
        """)
        title_layout.addWidget(btn_close)
        
        layout.addWidget(title_bar)
        
        # Content Area
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(40, 10, 40, 40)
        content_layout.setSpacing(30)
        
        # Grid
        grid = QHBoxLayout()
        grid.setSpacing(25)
        # ... (Add buttons to grid)
        # Note: We need to re-add buttons here as we changed layout structure
        
        # 1. UPDATE
        self.btn_build = PremiumCard("Update", "Apply latest changes", "🛠️", "build")
        self.btn_build.clicked.connect(self.run_build)
        grid.addWidget(self.btn_build)

        # 2. PLAY
        self.btn_launch = PremiumCard("Play", "Start experience", "🚀", "launch")
        self.btn_launch.clicked.connect(self.run_launch)
        grid.addWidget(self.btn_launch)

        # 3. EXPAND
        self.btn_assets = PremiumCard("Expand", "Add new content", "⚡", "assets")
        self.btn_assets.clicked.connect(self.run_assets)
        grid.addWidget(self.btn_assets)

        # 4. VIEW 3D
        self.btn_view3d = PremiumCard("View 3D", "Spline Interactive", "🧊", "default")
        self.btn_view3d.clicked.connect(self.run_view3d)
        if not WEB_ENGINE_AVAILABLE:
            self.btn_view3d.setEnabled(False)
        grid.addWidget(self.btn_view3d)
        
        content_layout.addLayout(grid)
        
        # Terminal / Web View Container
        stack = QWidget()
        stack.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        stack_layout = QVBoxLayout(stack)
        stack_layout.setContentsMargins(0,0,0,0)
        
        self.terminal = QTextEdit()
        self.terminal.setReadOnly(True)
        self.terminal.setPlaceholderText("SYSTEM READY...")
        # Terminal Styling - "Hacker/Game Console"
        self.terminal.setStyleSheet("""
            QTextEdit {
                background-color: #0A0A0C;
                color: #00FF00;
                border: 1px solid #222;
                border-radius: 12px;
                padding: 20px;
                font-family: 'JetBrains Mono', 'Monaco', monospace;
                font-size: 12px;
                selection-background-color: #00FF00;
                selection-color: #000;
            }
        """)
        stack_layout.addWidget(self.terminal)
        
        self.web_view = None
        if WEB_ENGINE_AVAILABLE:
             self.web_view = QWebEngineView()
             self.web_view.setVisible(False)
             # Round corners for web view? Hard with QWebEngineView, but we can try masking or just placing it nicely.
             stack_layout.addWidget(self.web_view)
        
        content_layout.addWidget(stack)
        
        # Footer / Status
        self.status = QLabel("SYSTEM B // ONLINE")
        self.status.setStyleSheet("color: #444; font-size: 10px; letter-spacing: 1px; font-weight: bold;")
        content_layout.addWidget(self.status, alignment=Qt.AlignRight)
        
        layout.addLayout(content_layout)

        self.root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.set_magnetic_focus(self.btn_build)
        
        # Drag Logic Variables
        self.old_pos = None

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.old_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if self.old_pos:
            delta = event.globalPosition().toPoint() - self.old_pos
            self.move(self.pos() + delta)
            self.old_pos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        self.old_pos = None
        
    # ... (Keep existing methods: log, run_command, paintEvent, etc.)

    def log(self, text):
        self.terminal.moveCursor(self.terminal.textCursor().MoveOperation.End)
        self.terminal.insertPlainText(text)
        self.terminal.ensureCursorVisible()

    def set_magnetic_focus(self, target_btn):
        """Moves the 'magnetic' attention to the specified button"""
        self.btn_build.set_magnetic_state(False)
        self.btn_launch.set_magnetic_state(False)
        self.btn_assets.set_magnetic_state(False)
        self.btn_view3d.set_magnetic_state(False)
        
        if target_btn:
            target_btn.set_magnetic_state(True)
            self.status.setText(f"Magnetic Guide: Suggested Action -> {target_btn.title}")

    def run_view3d(self):
        if not self.web_view: return
        
        self.terminal.setVisible(False)
        self.web_view.setVisible(True)
        
        html_path = os.path.abspath(os.path.join(self.root_dir, "tools/dashboard/nexus-web-view/dist/index.html"))
        self.web_view.load(QUrl.fromLocalFile(html_path))
        
        self.log(f"Loading 3D View: {html_path}\n")
        self.status.setText("Mode: Spline Interactive View")

    def run_command(self, cmd, next_target=None):
        if self.web_view:
             self.web_view.setVisible(False)
        self.terminal.setVisible(True)

        self.terminal.clear()
        self.log(f"> Executing: {cmd}\n{'-'*40}\n")
        self.next_magnetic_target = next_target
        
        self.worker = CommandWorker(cmd, self.root_dir)
        self.worker.output_signal.connect(self.log)
        self.worker.finished_signal.connect(self.on_process_finished)
        self.worker.start()
        
        # Lock UI
        self.btn_build.setEnabled(False)
        self.btn_launch.setEnabled(False)
        self.btn_assets.setEnabled(False)

    def on_process_finished(self, code):
        self.log(f"\n[Exit Code {code}]\n")
        self.btn_build.setEnabled(True)
        self.btn_launch.setEnabled(True)
        self.btn_assets.setEnabled(True)

        if code == 0 and self.next_magnetic_target:
            # Success! Magnetically snap to next step
            self.set_magnetic_focus(self.next_magnetic_target)
            self.log(f"\n✨ SUCCESS. Proceed to: {self.next_magnetic_target.title}\n")
        else:
            self.log("\n❌ Process failed or no next step linked.")

    def run_build(self):
        # After build -> Suggest Launch
        self.run_command("python3 nexus_compiler.py", next_target=self.btn_launch)

    def run_launch(self):
        # End of linear chain
        self.run_command("./AntigravityNexus.command", next_target=None)

    def run_assets(self):
        self.run_command("python3 Scripts/nexus_builder.py", next_target=None)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NexusDashboard()
    window.show()
    sys.exit(app.exec())
