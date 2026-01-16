import sys
import os
import subprocess
import time
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QPushButton, QFrame, QStackedWidget,
                             QTextEdit, QProgressBar, QCheckBox)
from PySide6.QtCore import Qt, QTimer, QThread, Signal
from PySide6.QtGui import QFont, QColor
from nexus_agents.squad import AgentCameraman, AgentStreamer, AgentDesigner, AgentEngineer, AgentOperator

# Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RECORDER_SCRIPT = os.path.join(BASE_DIR, "nexus_neo_recorder.py")
STREAM_SCRIPT = os.path.join(BASE_DIR, "nexus_stream.py")
VENV_PYTHON = os.path.join(BASE_DIR, "venv", "bin", "python3")

class WizardStep(QFrame):
    def __init__(self, title, description, action_text, action_callback, is_active=False):
        super().__init__()
        self.setStyleSheet(f"""
            QFrame {{
                background: {'rgba(139, 92, 246, 0.1)' if is_active else 'rgba(255, 255, 255, 0.05)'};
                border: 1px solid {'#8b5cf6' if is_active else 'rgba(255, 255, 255, 0.1)'};
                border-radius: 12px;
            }}
        """)
        
        layout = QHBoxLayout(self)
        
        info_layout = QVBoxLayout()
        t_label = QLabel(title)
        t_label.setFont(QFont("Outfit", 14, QFont.Bold))
        t_label.setStyleSheet("color: white; border: none; background: none;")
        info_layout.addWidget(t_label)
        
        d_label = QLabel(description)
        d_label.setFont(QFont("Inter", 10))
        d_label.setStyleSheet("color: #94a3b8; border: none; background: none;")
        d_label.setWordWrap(True)
        info_layout.addWidget(d_label)
        
        layout.addLayout(info_layout)
        
        if action_text:
            btn = QPushButton(action_text)
            btn.setFixedSize(120, 40)
            btn.setStyleSheet("""
                QPushButton {
                    background: #8b5cf6; color: white; border-radius: 6px; font-weight: bold;
                }
                QPushButton:hover { background: #7c3aed; }
            """)
            btn.clicked.connect(action_callback)
            layout.addWidget(btn)

class NexusWizard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ANTIGRAVITY WIZARD // SEQUENTIAL PROTOCOL")
        self.resize(500, 800)
        self.setStyleSheet("background-color: #0f172a;")
        
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        self.layout = QVBoxLayout(main_widget)
        self.layout.setSpacing(20)
        self.layout.setContentsMargins(30, 30, 30, 30)
        
        # Header
        header = QLabel("PROTOCOL SEQUENCER")
        header.setFont(QFont("Outfit", 24, QFont.Bold))
        header.setStyleSheet("color: white; letter-spacing: 2px;")
        self.layout.addWidget(header)
        
        # Recorder Control
        self.rec_layout = QHBoxLayout()
        self.rec_status = QLabel("Neo Recorder: OFF")
        self.rec_status.setStyleSheet("color: #ef4444; font-weight: bold;") 
        self.rec_btn = QPushButton("START RECORDING")
        self.rec_btn.setStyleSheet("background: #ef4444; color: white; padding: 5px; border-radius: 4px;")
        self.rec_btn.clicked.connect(self.toggle_recording)
        
        self.rec_layout.addWidget(self.rec_status)
        self.rec_layout.addWidget(self.rec_btn)
        self.layout.addLayout(self.rec_layout)
        
        self.recorder_process = None
        
        # Initialize Agent Squad
        self.agents = []
        self.start_agents()
        
        # Steps
        self.steps_container = QVBoxLayout()
        self.layout.addLayout(self.steps_container)
        
        self.init_steps()
        
        self.layout.addStretch()
        
        # Console Log
        self.console = QTextEdit()
        self.console.setFixedHeight(150)
        self.console.setReadOnly(True)
        self.console.setStyleSheet("background: #020617; color: #00f2ff; font-family: monospace; border: 1px solid #1e293b;")
        self.layout.addWidget(self.console)

    def log(self, msg):
        self.console.append(f"> {msg}")
        self.console.verticalScrollBar().setValue(self.console.verticalScrollBar().maximum())

    def start_agents(self):
        # Create and start all delegated agents
        self.agent_cameraman = AgentCameraman()
        self.agent_cameraman.status_update.connect(self.log)
        self.agent_cameraman.start()
        self.agents.append(self.agent_cameraman)
        
        self.agent_streamer = AgentStreamer()
        self.agent_streamer.status_update.connect(self.log)
        self.agent_streamer.start()
        self.agents.append(self.agent_streamer)
        
        self.agent_designer = AgentDesigner()
        self.agent_designer.status_update.connect(self.log)
        self.agent_designer.start()
        self.agents.append(self.agent_designer)
        
        self.agent_engineer = AgentEngineer()
        self.agent_engineer.status_update.connect(self.log)
        self.agent_engineer.start()
        self.agents.append(self.agent_engineer)
        
        self.agent_operator = AgentOperator()
        self.agent_operator.status_update.connect(self.log)
        self.agent_operator.start()
        self.agents.append(self.agent_operator)

    def init_steps(self):
        # Step 1: Define
        s1 = WizardStep("1. DEFINE TASK", "Input the next architectural directive for Gemini Code Assist.", "INPUT", self.step_define, is_active=True)
        self.steps_container.addWidget(s1)
        
        # Step 2: Handoff
        s2 = WizardStep("2. GEMINI HANDOFF", "Transmit context to AI model for concurrent processing.", "PROCESS", self.step_handoff)
        self.steps_container.addWidget(s2)
        
        # Step 3: Build
        s3 = WizardStep("3. UNREAL BUILD", "Compile and Hot Reload the Twin Engine.", "BUILD", self.step_build)
        self.steps_container.addWidget(s3)
        
        # Step 4: Stream
        s4 = WizardStep("4. LIVE STREAM", "Broadcast the viewport to the Antigravity Nexus.", "GO LIVE", self.step_stream)
        self.steps_container.addWidget(s4)

    def toggle_recording(self):
        if self.recorder_process is None:
            # Start
            self.log("Starting Neo Recorder (1 frame / 10s)...")
            self.recorder_process = subprocess.Popen([VENV_PYTHON, RECORDER_SCRIPT], start_new_session=True)
            self.rec_status.setText("Neo Recorder: ON")
            self.rec_status.setStyleSheet("color: #22c55e; font-weight: bold;")
            self.rec_btn.setText("STOP RECORDING")
            self.rec_btn.setStyleSheet("background: #22c55e; color: white;")
        else:
            # Stop
            self.log("Stopping Neo Recorder...")
            self.recorder_process.terminate()
            self.recorder_process = None
            self.rec_status.setText("Neo Recorder: OFF")
            self.rec_status.setStyleSheet("color: #ef4444; font-weight: bold;")
            self.rec_btn.setText("START RECORDING")
            self.rec_btn.setStyleSheet("background: #ef4444; color: white;")

    def step_define(self):
        self.log("Requesting user input... (Simulated)")
        # In a real app this would open a dialog
        self.log("Task Defined: 'Create new chaotic physics node'")

    def step_handoff(self):
        self.log("Handing off to Gemini Code Assist...")
        QTimer.singleShot(1000, lambda: self.log("Gemini: 'Analysing shader complexity...'"))
        QTimer.singleShot(2500, lambda: self.log("Gemini: 'Optimizing vertex buffer...'"))
        QTimer.singleShot(4000, lambda: self.log("✅ Handoff Complete. Artifacts Ready."))

    def step_build(self):
        self.log("Triggering Unreal Build System...")
        # Simulate build
        QTimer.singleShot(2000, lambda: self.log("✅ Build Successful. Hot Reload complete."))

    def step_stream(self):
        self.log("Launching Live Stream...")
        subprocess.Popen([VENV_PYTHON, STREAM_SCRIPT], start_new_session=True)
        self.log("✅ Stream process detached.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    wizard = NexusWizard()
    wizard.show()
    sys.exit(app.exec())
