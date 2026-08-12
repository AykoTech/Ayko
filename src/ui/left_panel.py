#!/usr/bin/env python3
"""Left Panel - Navigation and controls for professional interface."""

import logging
from typing import List
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTextEdit, QGroupBox, QScrollArea
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QFont

logger = logging.getLogger("LeftPanel")

PROFESSIONAL_THEME = {
    "header_bg": "#1a1f3a",
    "panel_bg": "#0f1428",
    "panel_border": "#2a3a5a",
    "text_primary": "#e0e0e0",
    "text_secondary": "#9090a0",
    "accent_blue": "#4a7cba",
    "accent_green": "#4a7a4a",
    "accent_red": "#7a4a4a",
}


class LeftPanel(QWidget):
    """Professional left panel with navigation and controls."""
    
    command_requested = pyqtSignal(str)
    microphone_toggled = pyqtSignal(bool)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.current_state = "operational"
        self.microphone_active = False
        
        self._init_ui()
        self._apply_professional_theme()
        
        logger.info("✓ LeftPanel initialized")
    
    def _init_ui(self):
        """Initialize left panel layout."""
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)
        
        # Navigation Section
        nav_section = self._create_navigation_section()
        layout.addWidget(nav_section)
        
        # Voice Controls Section
        voice_section = self._create_voice_controls_section()
        layout.addWidget(voice_section)
        
        # Quick Actions Section
        actions_section = self._create_quick_actions_section()
        layout.addWidget(actions_section)
        
        # Command Log Section
        log_section = self._create_command_log_section()
        layout.addWidget(log_section, 1)
        
        # System Status Section
        status_section = self._create_system_status_section()
        layout.addWidget(status_section)
        
        self.setLayout(layout)
    
    def _create_navigation_section(self) -> QWidget:
        """Create navigation section."""
        section = QGroupBox("NAVIGATION")
        section.setStyleSheet(self._get_section_style())
        
        layout = QVBoxLayout()
        layout.setSpacing(8)
        
        nav_buttons = [
            ("🏠 DASHBOARD", "dashboard"),
            ("🎤 VOICE", "voice"),
            ("📊 METRICS", "metrics"),
            ("⚙️ SETTINGS", "settings"),
            ("📋 LOGS", "logs"),
        ]
        
        for label, action in nav_buttons:
            btn = QPushButton(label)
            btn.setStyleSheet(self._get_nav_button_style())
            btn.clicked.connect(lambda checked, a=action: self._handle_nav_action(a))
            layout.addWidget(btn)
        
        section.setLayout(layout)
        return section
    
    def _create_voice_controls_section(self) -> QWidget:
        """Create voice controls section."""
        section = QGroupBox("VOICE CONTROLS")
        section.setStyleSheet(self._get_section_style())
        
        layout = QVBoxLayout()
        layout.setSpacing(10)
        
        # Microphone Status
        status_layout = QHBoxLayout()
        self.mic_status_indicator = QLabel("●")
        self.mic_status_indicator.setStyleSheet(f"color: {PROFESSIONAL_THEME['text_secondary']};")
        status_layout.addWidget(self.mic_status_indicator)
        
        self.mic_status_text = QLabel("MICROPHONE: OFFLINE")
        self.mic_status_text.setFont(QFont("Courier New", 10))
        self.mic_status_text.setStyleSheet(f"color: {PROFESSIONAL_THEME['text_secondary']};")
        status_layout.addWidget(self.mic_status_text)
        
        status_layout.addStretch()
        layout.addLayout(status_layout)
        
        # Microphone Toggle
        self.mic_button = QPushButton("ACTIVATE MICROPHONE")
        self.mic_button.setStyleSheet(self._get_action_button_style())
        self.mic_button.clicked.connect(self._toggle_microphone)
        layout.addWidget(self.mic_button)
        
        # Wake Word Settings
        wake_word_label = QLabel("WAKE WORD:")
        wake_word_label.setStyleSheet(f"color: {PROFESSIONAL_THEME['text_secondary']};")
        layout.addWidget(wake_word_label)
        
        self.wake_word_display = QLabel("JARVIS")
        self.wake_word_display.setFont(QFont("Courier New", 12, QFont.Weight.Bold))
        self.wake_word_display.setStyleSheet(f"color: {PROFESSIONAL_THEME['accent_blue']};")
        self.wake_word_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.wake_word_display)
        
        section.setLayout(layout)
        return section
    
    def _create_quick_actions_section(self) -> QWidget:
        """Create quick actions section."""
        section = QGroupBox("QUICK ACTIONS")
        section.setStyleSheet(self._get_section_style())
        
        layout = QVBoxLayout()
        layout.setSpacing(8)
        
        actions = [
            ("🌐 OPEN BROWSER", "browser"),
            ("🔍 WEB SEARCH", "search"),
            ("📁 FILE MANAGER", "files"),
            ("💻 SYSTEM INFO", "sysinfo"),
        ]
        
        for label, action in actions:
            btn = QPushButton(label)
            btn.setStyleSheet(self._get_action_button_style())
            btn.clicked.connect(lambda checked, a=action: self._handle_quick_action(a))
            layout.addWidget(btn)
        
        section.setLayout(layout)
        return section
    
    def _create_command_log_section(self) -> QWidget:
        """Create command log section."""
        section = QGroupBox("COMMAND LOG")
        section.setStyleSheet(self._get_section_style())
        
        layout = QVBoxLayout()
        layout.setSpacing(5)
        
        self.command_log = QTextEdit()
        self.command_log.setReadOnly(True)
        self.command_log.setFont(QFont("Courier New", 9))
        self.command_log.setStyleSheet(f"""
            QTextEdit {{
                background: {PROFESSIONAL_THEME["panel_bg"]};
                color: {PROFESSIONAL_THEME["text_primary"]};
                border: 1px solid {PROFESSIONAL_THEME["panel_border"]};
                border-radius: 3px;
                padding: 5px;
            }}
        """)
        layout.addWidget(self.command_log)
        
        clear_btn = QPushButton("CLEAR LOG")
        clear_btn.setStyleSheet(self._get_small_button_style())
        clear_btn.clicked.connect(self.command_log.clear)
        layout.addWidget(clear_btn)
        
        section.setLayout(layout)
        return section
    
    def _create_system_status_section(self) -> QWidget:
        """Create system status section."""
        section = QGroupBox("SYSTEM STATUS")
        section.setStyleSheet(self._get_section_style())
        
        layout = QVBoxLayout()
        layout.setSpacing(5)
        
        self.system_status_text = QLabel("SYSTEM: OPERATIONAL")
        self.system_status_text.setFont(QFont("Courier New", 10, QFont.Weight.Bold))
        self.system_status_text.setStyleSheet(f"color: {PROFESSIONAL_THEME['status_operational']};")
        layout.addWidget(self.system_status_text)
        
        self.components_status = QLabel("ALL COMPONENTS: ACTIVE")
        self.components_status.setFont(QFont("Courier New", 9))
        self.components_status.setStyleSheet(f"color: {PROFESSIONAL_THEME['accent_green']};")
        layout.addWidget(self.components_status)
        
        section.setLayout(layout)
        return section
    
    def _get_section_style(self) -> str:
        """Get professional section style."""
        return f"""
            QGroupBox {{
                font-family: 'Arial';
                font-size: 10px;
                font-weight: bold;
                color: {PROFESSIONAL_THEME["accent_blue"]};
                border: 1px solid {PROFESSIONAL_THEME["panel_border"]};
                border-radius: 3px;
                margin-top: 10px;
                padding: 8px;
                background: {PROFESSIONAL_THEME["header_bg"]};
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 5px;
            }}
        """
    
    def _get_nav_button_style(self) -> str:
        """Get navigation button style."""
        return f"""
            QPushButton {{
                background: {PROFESSIONAL_THEME["panel_bg"]};
                color: {PROFESSIONAL_THEME["text_primary"]};
                border: 1px solid {PROFESSIONAL_THEME["panel_border"]};
                border-radius: 3px;
                padding: 8px;
                text-align: left;
                font-size: 10px;
            }}
            QPushButton:hover {{
                background: {PROFESSIONAL_THEME["accent_blue"]};
                color: white;
                border: 1px solid {PROFESSIONAL_THEME["accent_blue"]};
            }}
            QPushButton:pressed {{
                background: {PROFESSIONAL_THEME["header_bg"]};
            }}
        """
    
    def _get_action_button_style(self) -> str:
        """Get action button style."""
        return f"""
            QPushButton {{
                background: {PROFESSIONAL_THEME["panel_bg"]};
                color: {PROFESSIONAL_THEME["accent_blue"]};
                border: 1px solid {PROFESSIONAL_THEME["accent_blue"]};
                border-radius: 3px;
                padding: 10px;
                font-weight: bold;
                font-size: 10px;
            }}
            QPushButton:hover {{
                background: {PROFESSIONAL_THEME["accent_blue"]};
                color: white;
            }}
            QPushButton:pressed {{
                background: {PROFESSIONAL_THEME["header_bg"]};
            }}
        """
    
    def _get_small_button_style(self) -> str:
        """Get small button style."""
        return f"""
            QPushButton {{
                background: {PROFESSIONAL_THEME["panel_bg"]};
                color: {PROFESSIONAL_THEME["text_secondary"]};
                border: 1px solid {PROFESSIONAL_THEME["panel_border"]};
                border-radius: 2px;
                padding: 5px;
                font-size: 9px;
            }}
            QPushButton:hover {{
                background: {PROFESSIONAL_THEME["accent_blue"]};
                color: white;
            }}
        """
    
    def _apply_professional_theme(self):
        """Apply professional theme to panel."""
        self.setStyleSheet(f"""
            LeftPanel {{
                background: {PROFESSIONAL_THEME["panel_bg"]};
                border-right: 1px solid {PROFESSIONAL_THEME["panel_border"]};
            }}
        """)
    
    def _handle_nav_action(self, action: str):
        """Handle navigation actions."""
        self.add_log_entry(f"Navigation: {action}")
    
    def _handle_quick_action(self, action: str):
        """Handle quick actions."""
        self.add_log_entry(f"Action: {action}")
        self.command_requested.emit(action)
    
    def _toggle_microphone(self):
        """Toggle microphone."""
        self.microphone_active = not self.microphone_active
        self.microphone_toggled.emit(self.microphone_active)
        self.update_microphone_status(self.microphone_active)
    
    def update_microphone_status(self, active: bool):
        """Update microphone status display."""
        if active:
            self.mic_status_indicator.setStyleSheet(f"color: {PROFESSIONAL_THEME['accent_green']};")
            self.mic_status_text.setText("MICROPHONE: ONLINE")
            self.mic_status_text.setStyleSheet(f"color: {PROFESSIONAL_THEME['accent_green']};")
            self.mic_button.setText("DEACTIVATE MICROPHONE")
            self.mic_button.setStyleSheet(self._get_active_button_style())
        else:
            self.mic_status_indicator.setStyleSheet(f"color: {PROFESSIONAL_THEME['text_secondary']};")
            self.mic_status_text.setText("MICROPHONE: OFFLINE")
            self.mic_status_text.setStyleSheet(f"color: {PROFESSIONAL_THEME['text_secondary']};")
            self.mic_button.setText("ACTIVATE MICROPHONE")
            self.mic_button.setStyleSheet(self._get_action_button_style())
    
    def _get_active_button_style(self) -> str:
        """Get active state button style."""
        return f"""
            QPushButton {{
                background: {PROFESSIONAL_THEME["accent_green"]};
                color: white;
                border: 1px solid {PROFESSIONAL_THEME["accent_green"]};
                border-radius: 3px;
                padding: 10px;
                font-weight: bold;
                font-size: 10px;
            }}
            QPushButton:hover {{
                background: {PROFESSIONAL_THEME["panel_bg"]};
                color: {PROFESSIONAL_THEME["accent_green"]};
            }}
        """
    
    def update_system_state(self, state: str):
        """Update system state display."""
        self.current_state = state
        
        state_colors = {
            "operational": PROFESSIONAL_THEME["status_operational"],
            "warning": PROFESSIONAL_THEME["status_warning"],
            "error": PROFESSIONAL_THEME["status_error"],
            "processing": PROFESSIONAL_THEME["accent_orange"]
        }
        
        color = state_colors.get(state, PROFESSIONAL_THEME["status_operational"])
        
        self.system_status_text.setText(f"SYSTEM: {state.upper()}")
        self.system_status_text.setStyleSheet(f"color: {color};")
    
    def add_log_entry(self, text: str):
        """Add entry to command log."""
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.command_log.append(f"[{timestamp}] {text}")
    
    def add_command_log(self, command: str, success: bool):
        """Add command execution log."""
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        status = "✓" if success else "✗"
        self.command_log.append(f"[{timestamp}] {status} {command}")