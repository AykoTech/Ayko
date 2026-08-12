
import sys
import logging
from datetime import datetime
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTextEdit, QSlider, QComboBox, QCheckBox, QSpinBox
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QSize
from PyQt6.QtGui import QFont, QColor, QPixmap
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl
from pathlib import Path

logger = logging.getLogger("MainWindow")

class MainWindow(QWidget):
    """Main JARVIS UI with 3D sphere"""
    
    def __init__(self, parent=None):
        super().__init__()
        self.parent_app = parent
        self.init_ui()
        self.setup_styles()
    
    def init_ui(self):
        """Initialize UI components"""
        
        main_layout = QHBoxLayout()
        
        # LEFT: 3D Sphere (70%)
        left_layout = QVBoxLayout()
        self.sphere_view = QWebEngineView()
        sphere_path = Path("assets/sphere.html").resolve()
        if sphere_path.exists():
            self.sphere_view.load(QUrl.fromLocalFile(str(sphere_path)))
        left_layout.addWidget(self.sphere_view)
        
        # Center info panel
        info_layout = QVBoxLayout()
        self.status_label = QLabel("🟢 Ready")
        self.status_label.setStyleSheet("color: #00ff41; font-size: 16px; font-weight: bold;")
        self.command_label = QLabel("Waiting for command...")
        self.command_label.setStyleSheet("color: #00aa20; font-size: 12px;")
        
        info_layout.addWidget(self.status_label)
        info_layout.addWidget(self.command_label)
        left_layout.addLayout(info_layout)
        
        # RIGHT: Control Panel (30%)
        right_layout = QVBoxLayout()
        right_layout.setSpacing(10)
        
        # Title
        title = QLabel("JARVIS v0.0.01")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title.setStyleSheet("color: #00ff41;")
        right_layout.addWidget(title)
        
        # Microphone button
        self.mic_button = QPushButton("🎤 Start Listening")
        self.mic_button.setStyleSheet(self._get_button_style())
        self.mic_button.clicked.connect(self.toggle_microphone)
        right_layout.addWidget(self.mic_button)
        
        # Command log
        log_label = QLabel("Command Log:")
        log_label.setStyleSheet("color: #00ff41; font-weight: bold;")
        right_layout.addWidget(log_label)
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setStyleSheet(self._get_log_style())
        self.log_text.setMaximumHeight(150)
        right_layout.addWidget(self.log_text)
        
        # Volume control
        right_layout.addWidget(QLabel("Volume:"))
        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setMinimum(0)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setValue(70)
        right_layout.addWidget(self.volume_slider)
        
        # Settings button
        settings_btn = QPushButton("⚙️ Settings")
        settings_btn.setStyleSheet(self._get_button_style())
        settings_btn.clicked.connect(self.open_settings)
        right_layout.addWidget(settings_btn)
        
        # Help button
        help_btn = QPushButton("❓ Commands")
        help_btn.setStyleSheet(self._get_button_style())
        help_btn.clicked.connect(self.show_commands)
        right_layout.addWidget(help_btn)
        
        right_layout.addStretch()
        
        # Combine layouts
        main_layout.addLayout(left_layout, 7)
        main_layout.addLayout(right_layout, 3)
        
        self.setLayout(main_layout)
        
        logger.info("UI initialized")
    
    def toggle_microphone(self):
        """Toggle microphone listening"""
        if self.parent_app.audio_manager.is_listening:
            self.parent_app.audio_manager.stop()
            self.mic_button.setText("🎤 Start Listening")
            self.update_status("Stopped", "red")
        else:
            self.parent_app.audio_manager.start()
            self.mic_button.setText("⏹️ Stop Listening")
            self.update_status("Listening...", "green")
    
    def on_listening_started(self):
        """Called when wake-word detected"""
        self.update_status("Recording...", "yellow")
        self.add_log_entry("🎤 Listening for command...")
    
    def on_command_executed(self, cmd_text: str, intent: str, result: dict):
        """Called when command executed"""
        status = result.get("status", "unknown")
        self.update_status(f"Executed: {intent}", "green")
        self.add_log_entry(f"✓ {intent}: {cmd_text[:50]}")
    
    def on_command_done(self, text: str, intent: str):
        """Called when command completes"""
        self.add_log_entry(f"✓ {intent}")
        self.update_status("Ready", "green")
    
    def on_error(self, error_msg: str):
        """Called on error"""
        self.update_status(f"Error: {error_msg[:30]}", "red")
        self.add_log_entry(f"✗ Error: {error_msg}")
    
    def update_status(self, text: str, color: str = "green"):
        """Update status indicator"""
        color_map = {"green": "#00ff41", "red": "#ff0000", "yellow": "#ffff00"}
        self.status_label.setText(f"🔵 {text}")
        self.status_label.setStyleSheet(f"color: {color_map.get(color, '#00ff41')}; font-size: 16px; font-weight: bold;")
    
    def add_log_entry(self, text: str):
        """Add entry to command log"""
        time = datetime.now().strftime("%H:%M:%S")
        self.log_text.append(f"[{time}] {text}")
        # Auto-scroll
        self.log_text.verticalScrollBar().setValue(
            self.log_text.verticalScrollBar().maximum()
        )
    
    def open_settings(self):
        """Open settings panel"""
        self.add_log_entry("⚙️ Opening settings...")
        # TODO: Implement settings panel
    
    def show_commands(self):
        """Show available commands"""
        self.add_log_entry("📋 Commands: Check COMMANDS.md")
    
    def _get_button_style(self) -> str:
        return """
            QPushButton {
                background-color: #1a1a2e;
                color: #00ff41;
                border: 2px solid #00ff41;
                border-radius: 5px;
                padding: 8px;
                font-weight: bold;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #0f3a0f;
                border: 2px solid #00ff41;
            }
            QPushButton:pressed {
                background-color: #00ff41;
                color: #000000;
            }
        """
    
    def _get_log_style(self) -> str:
        return """
            QTextEdit {
                background-color: #0a0e27;
                color: #00ff41;
                border: 1px solid #00ff41;
                border-radius: 3px;
                font-family: Courier;
                font-size: 10px;
            }
        """
