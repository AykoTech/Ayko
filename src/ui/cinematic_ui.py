#!/usr/bin/env python3
"""Cinematic UI - Marvel-style interface for JARVIS."""

import logging
from typing import Dict, Optional
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTextEdit, QSlider, QFrame
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QFont

# Import after sphere_manager and other components are created
try:
    from .sphere_manager import SphereManager
    from .hud_controller import HUDController
    from .audio_visualizer import AudioVisualizer
except ImportError:
    SphereManager = None
    HUDController = None
    AudioVisualizer = None

logger = logging.getLogger("CinematicUI")

# Marvel Cinematic Theme Colors
MARVEL_THEME = {
    "arc_blue": "#00BFFF", 
    "arc_blue_glow": "#0066CC",
    "iron_gold": "#FFD700",
    "iron_orange": "#FF8C00", 
    "hud_black": "#0A0E27",
    "hud_dark": "#0F1428",
    "hud_panel": "#1A1F3A",
    "error_red": "#FF3333",
    "success_green": "#00FF41",
    "text_primary": "#E0E0E0",
    "text_secondary": "#A0A0A0",
}


class CinematicUI(QWidget):
    """Main cinematic UI container with Marvel-style design."""
    
    # Signals for core integration
    command_requested = pyqtSignal(str)
    microphone_toggled = pyqtSignal(bool)
    settings_requested = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.current_state = "idle"
        self.audio_data = []
        
        self._init_ui()
        self._apply_marvel_theme()
        
        logger.info("✓ CinematicUI initialized")
    
    def _init_ui(self):
        """Initialize cinematic UI components."""
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # LEFT: 3D Sphere + HUD (70%)
        left_container = QWidget()
        left_layout = QVBoxLayout(left_container)
        left_layout.setContentsMargins(0, 0, 0, 0)
        
        # 3D Sphere (with fallback if not available)
        if SphereManager:
            self.sphere_manager = SphereManager()
            left_layout.addWidget(self.sphere_manager.get_sphere_widget(), 3)
        else:
            # Fallback placeholder
            sphere_placeholder = QLabel("3D SPHERE LOADING...")
            sphere_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
            sphere_placeholder.setStyleSheet("color: #00BFFF; font-size: 24px; font-weight: bold;")
            left_layout.addWidget(sphere_placeholder, 3)
            self.sphere_manager = None
        
        # HUD Overlay (with fallback if not available)
        if HUDController:
            self.hud_controller = HUDController()
            left_layout.addWidget(self.hud_controller, 1)
        else:
            # Fallback placeholder
            hud_placeholder = QLabel("HUD SYSTEM LOADING...")
            hud_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
            hud_placeholder.setStyleSheet("color: #FFD700; font-size: 14px;")
            left_layout.addWidget(hud_placeholder, 1)
            self.hud_controller = None
        
        main_layout.addWidget(left_container, 7)
        
        # RIGHT: Control Panel (30%)
        right_panel = self._create_control_panel()
        main_layout.addWidget(right_panel, 3)
        
        self.setLayout(main_layout)
    
    def _create_control_panel(self) -> QWidget:
        """Create Marvel-style control panel."""
        panel = QWidget()
        panel.setStyleSheet(f"""
            QWidget {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {MARVEL_THEME["hud_dark"]}, 
                    stop:1 {MARVEL_THEME["hud_black"]});
                border-left: 3px solid {MARVEL_THEME["arc_blue"]};
            }}
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Cinematic Title
        title = QLabel("JARVIS")
        title.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        title.setStyleSheet(f"""
            color: {MARVEL_THEME["arc_blue"]};
            text-shadow: 0 0 20px {MARVEL_THEME["arc_blue_glow"]};
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        subtitle = QLabel("AI SYSTEM v0.0.01")
        subtitle.setFont(QFont("Courier New", 10))
        subtitle.setStyleSheet(f"color: {MARVEL_THEME["iron_gold"]};")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle)
        
        # Status Display
        self.status_display = QLabel("SYSTEM ONLINE")
        self.status_display.setFont(QFont("Courier New", 12, QFont.Weight.Bold))
        self.status_display.setStyleSheet(f"""
            color: {MARVEL_THEME["success_green"]};
            background: rgba(0, 255, 65, 0.1);
            border: 2px solid {MARVEL_THEME["success_green"]};
            padding: 10px;
            border-radius: 5px;
        """)
        self.status_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_display)
        
        # Audio Visualizer (with fallback)
        if AudioVisualizer:
            self.audio_visualizer = AudioVisualizer()
            layout.addWidget(self.audio_visualizer, 2)
        else:
            # Fallback placeholder
            audio_placeholder = QLabel("AUDIO VISUALIZER")
            audio_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
            audio_placeholder.setStyleSheet("color: #00BFFF; font-size: 12px;")
            layout.addWidget(audio_placeholder, 2)
            self.audio_visualizer = None
        
        # Microphone Button (Cinematic Style)
        self.mic_button = QPushButton("◉ ACTIVATE VOICE")
        self.mic_button.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.mic_button.setStyleSheet(self._get_marvel_button_style())
        self.mic_button.clicked.connect(self._toggle_microphone)
        layout.addWidget(self.mic_button)
        
        # Command Log (Cinematic Terminal)
        log_label = QLabel("COMMAND LOG")
        log_label.setFont(QFont("Courier New", 10, QFont.Weight.Bold))
        log_label.setStyleSheet(f"color: {MARVEL_THEME["arc_blue"]};")
        layout.addWidget(log_label)
        
        self.command_log = QTextEdit()
        self.command_log.setReadOnly(True)
        self.command_log.setFont(QFont("Courier New", 9))
        self.command_log.setStyleSheet(f"""
            QTextEdit {{
                background: rgba(10, 14, 39, 0.8);
                color: {MARVEL_THEME["success_green"]};
                border: 1px solid {MARVEL_THEME["arc_blue"]};
                border-radius: 5px;
                padding: 8px;
            }}
        """)
        layout.addWidget(self.command_log, 2)
        
        # Settings Button
        settings_btn = QPushButton("⚙ SYSTEM CONFIG")
        settings_btn.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        settings_btn.setStyleSheet(self._get_marvel_button_style())
        settings_btn.clicked.connect(self.settings_requested.emit)
        layout.addWidget(settings_btn)
        
        layout.addStretch()
        
        panel.setLayout(layout)
        return panel
    
    def _get_marvel_button_style(self) -> str:
        """Get Marvel-style button CSS."""
        return f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {MARVEL_THEME["arc_blue"]}, 
                    stop:1 {MARVEL_THEME["arc_blue_glow"]});
                color: white;
                border: 2px solid {MARVEL_THEME["arc_blue"]};
                border-radius: 8px;
                padding: 12px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {MARVEL_THEME["iron_gold"]}, 
                    stop:1 {MARVEL_THEME["iron_orange"]});
                border: 2px solid {MARVEL_THEME["iron_gold"]};
            }}
            QPushButton:pressed {{
                background: {MARVEL_THEME["hud_black"]};
                border: 2px solid {MARVEL_THEME["iron_gold"]};
            }}
        """
    
    def _apply_marvel_theme(self):
        """Apply Marvel cinematic theme to entire window."""
        self.setStyleSheet(f"""
            CinematicUI {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {MARVEL_THEME["hud_black"]}, 
                    stop:1 {MARVEL_THEME["hud_dark"]});
            }}
        """)
    
    def _toggle_microphone(self):
        """Toggle microphone with visual feedback."""
        is_active = self.mic_button.text() == "◉ ACTIVATE VOICE"
        
        if is_active:
            self.mic_button.setText("⏹ DEACTIVATE")
            self.status_display.setText("VOICE ACTIVE")
            self.status_display.setStyleSheet(f"""
                color: {MARVEL_THEME["arc_blue"]};
                background: rgba(0, 191, 255, 0.2);
                border: 2px solid {MARVEL_THEME["arc_blue"]};
                padding: 10px;
                border-radius: 5px;
            """)
            if self.sphere_manager:
                self.sphere_manager.set_state("listening")
            if self.hud_controller:
                self.hud_controller.set_mode("listening")
            self.microphone_toggled.emit(True)
        else:
            self.mic_button.setText("◉ ACTIVATE VOICE")
            self.status_display.setText("SYSTEM ONLINE")
            self.status_display.setStyleSheet(f"""
                color: {MARVEL_THEME["success_green"]};
                background: rgba(0, 255, 65, 0.1);
                border: 2px solid {MARVEL_THEME["success_green"]};
                padding: 10px;
                border-radius: 5px;
            """)
            if self.sphere_manager:
                self.sphere_manager.set_state("idle")
            if self.hud_controller:
                self.hud_controller.set_mode("idle")
            self.microphone_toggled.emit(False)
    
    def set_state(self, state: str):
        """Set UI state with appropriate visuals."""
        self.current_state = state
        
        state_config = {
            "idle": {
                "status": "SYSTEM ONLINE",
                "color": MARVEL_THEME["success_green"],
                "sphere_state": "idle"
            },
            "listening": {
                "status": "VOICE ACTIVE", 
                "color": MARVEL_THEME["arc_blue"],
                "sphere_state": "listening"
            },
            "processing": {
                "status": "PROCESSING COMMAND",
                "color": MARVEL_THEME["iron_gold"],
                "sphere_state": "processing"
            },
            "speaking": {
                "status": "SPEAKING",
                "color": MARVEL_THEME["success_green"],
                "sphere_state": "speaking"
            },
            "error": {
                "status": "SYSTEM ERROR",
                "color": MARVEL_THEME["error_red"],
                "sphere_state": "error"
            }
        }
        
        config = state_config.get(state, state_config["idle"])
        
        self.status_display.setText(config["status"])
        self.status_display.setStyleSheet(f"""
            color: {config["color"]};
            background: rgba({self._hex_to_rgb(config["color"])}, 0.2);
            border: 2px solid {config["color"]};
            padding: 10px;
            border-radius: 5px;
        """)
        
        if self.sphere_manager:
            self.sphere_manager.set_state(config["sphere_state"])
        if self.hud_controller:
            self.hud_controller.set_mode(state)
    
    def _hex_to_rgb(self, hex_color: str) -> str:
        """Convert hex color to RGB string."""
        hex_color = hex_color.lstrip('#')
        return ",".join(str(int(hex_color[i:i+2], 16)) for i in (0, 2, 4))
    
    def add_log_entry(self, text: str):
        """Add entry to command log with cinematic formatting."""
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        formatted = f"[{timestamp}] > {text}"
        
        if "ERROR" in text.upper():
            color = MARVEL_THEME["error_red"]
        elif "SUCCESS" in text.upper() or "✓" in text:
            color = MARVEL_THEME["success_green"]
        else:
            color = MARVEL_THEME["text_primary"]
        
        self.command_log.append(f'<span style="color: {color}">{formatted}</span>')
    
    def update_audio_visualization(self, audio_data):
        """Update audio visualization with real-time data."""
        if self.audio_visualizer:
            self.audio_visualizer.update_waveform(audio_data)


def launch_cinematic_ui():
    """Launch JARVIS cinematic interface."""
    import sys
    try:
        from PyQt6.QtWidgets import QApplication
    except ImportError:
        print("PyQt6 not found. Run: pip install PyQt6 PyQt6-WebEngine")
        sys.exit(1)

    app = QApplication(sys.argv)
    app.setApplicationName("JARVIS")
    app.setApplicationVersion("0.0.01")

    window = CinematicUI()
    window.setWindowTitle("JARVIS v0.0.01 - Cinematic Marvel Edition")
    window.setGeometry(100, 100, 1400, 850)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    launch_cinematic_ui()