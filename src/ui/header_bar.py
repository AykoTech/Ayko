#!/usr/bin/env python3
"""Header Bar - Status and menu for professional interface."""

import logging
from datetime import datetime
from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QLabel, QPushButton, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QFont

logger = logging.getLogger("HeaderBar")

PROFESSIONAL_THEME = {
    "header_bg": "#1a1f3a",
    "panel_bg": "#0f1428",
    "panel_border": "#2a3a5a",
    "text_primary": "#e0e0e0",
    "text_secondary": "#9090a0",
    "accent_blue": "#4a7cba",
    "accent_green": "#4a7a4a",
    "accent_red": "#7a4a4a",
    "accent_orange": "#7a6a4a",
}


class HeaderBar(QWidget):
    """Professional header bar with status and menu."""
    
    settings_requested = pyqtSignal()
    help_requested = pyqtSignal()
    exit_requested = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.current_state = "operational"
        
        self._init_ui()
        self._apply_professional_theme()
        self._start_clock()
        
        logger.info("✓ HeaderBar initialized")
    
    def _init_ui(self):
        """Initialize header bar layout."""
        self.setFixedHeight(50)
        
        layout = QHBoxLayout()
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(15)
        
        # Logo / Title
        title_layout = QHBoxLayout()
        
        logo_label = QLabel("AYKO")
        logo_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        logo_label.setStyleSheet(f"color: {PROFESSIONAL_THEME['accent_blue']};")
        title_layout.addWidget(logo_label)
        
        version_label = QLabel("v0.0.01")
        version_label.setFont(QFont("Arial", 10))
        version_label.setStyleSheet(f"color: {PROFESSIONAL_THEME['text_secondary']};")
        title_layout.addWidget(version_label)
        
        title_layout.addStretch()
        layout.addLayout(title_layout)
        
        layout.addStretch()
        
        # System Status Indicator
        status_layout = QHBoxLayout()
        
        status_label = QLabel("STATUS:")
        status_label.setStyleSheet(f"color: {PROFESSIONAL_THEME['text_secondary']};")
        status_layout.addWidget(status_label)
        
        self.status_indicator = QLabel("OPERATIONAL")
        self.status_indicator.setFont(QFont("Courier New", 11, QFont.Weight.Bold))
        self.status_indicator.setStyleSheet(f"color: {PROFESSIONAL_THEME['status_operational']};")
        status_layout.addWidget(self.status_indicator)
        
        status_separator = QLabel("|")
        status_separator.setStyleSheet(f"color: {PROFESSIONAL_THEME['panel_border']};")
        status_layout.addWidget(status_separator)
        
        # Active Operations
        self.active_operations = QLabel("IDLE")
        self.active_operations.setFont(QFont("Courier New", 11))
        self.active_operations.setStyleSheet(f"color: {PROFESSIONAL_THEME['text_secondary']};")
        status_layout.addWidget(self.active_operations)
        
        status_separator2 = QLabel("|")
        status_separator2.setStyleSheet(f"color: {PROFESSIONAL_THEME['panel_border']};")
        status_layout.addWidget(status_separator2)
        
        # User
        user_label = QLabel("USER: OPERATOR")
        user_label.setFont(QFont("Courier New", 10))
        user_label.setStyleSheet(f"color: {PROFESSIONAL_THEME['text_secondary']};")
        status_layout.addWidget(user_label)
        
        layout.addLayout(status_layout)
        
        layout.addStretch()
        
        # Clock
        self.clock_label = QLabel("")
        self.clock_label.setFont(QFont("Courier New", 12, QFont.Weight.Bold))
        self.clock_label.setStyleSheet(f"color: {PROFESSIONAL_THEME['text_primary']};")
        layout.addWidget(self.clock_label)
        
        layout.addSpacing(15)
        
        # Menu Buttons
        menu_layout = QHBoxLayout()
        
        help_btn = QPushButton("?")
        help_btn.setStyleSheet(self._get_menu_button_style())
        help_btn.setFixedSize(30, 30)
        help_btn.clicked.connect(self.help_requested.emit)
        menu_layout.addWidget(help_btn)
        
        settings_btn = QPushButton("⚙")
        settings_btn.setStyleSheet(self._get_menu_button_style())
        settings_btn.setFixedSize(30, 30)
        settings_btn.clicked.connect(self.settings_requested.emit)
        menu_layout.addWidget(settings_btn)
        
        exit_btn = QPushButton("✕")
        exit_btn.setStyleSheet(self._get_exit_button_style())
        exit_btn.setFixedSize(30, 30)
        exit_btn.clicked.connect(self.exit_requested.emit)
        menu_layout.addWidget(exit_btn)
        
        layout.addLayout(menu_layout)
        
        self.setLayout(layout)
    
    def _apply_professional_theme(self):
        """Apply professional theme to header."""
        self.setStyleSheet(f"""
            HeaderBar {{
                background: {PROFESSIONAL_THEME["header_bg"]};
                border-bottom: 2px solid {PROFESSIONAL_THEME["panel_border"]};
            }}
        """)
    
    def _get_menu_button_style(self) -> str:
        """Get menu button style."""
        return f"""
            QPushButton {{
                background: {PROFESSIONAL_THEME["panel_bg"]};
                color: {PROFESSIONAL_THEME["text_primary"]};
                border: 1px solid {PROFESSIONAL_THEME["panel_border"]};
                border-radius: 3px;
            }}
            QPushButton:hover {{
                background: {PROFESSIONAL_THEME["accent_blue"]};
                color: white;
                border: 1px solid {PROFESSIONAL_THEME["accent_blue"]};
            }}
        """
    
    def _get_exit_button_style(self) -> str:
        """Get exit button style."""
        return f"""
            QPushButton {{
                background: {PROFESSIONAL_THEME["accent_red"]};
                color: white;
                border: 1px solid {PROFESSIONAL_THEME["accent_red"]};
                border-radius: 3px;
            }}
            QPushButton:hover {{
                background: #9a5a5a;
            }}
        """
    
    def _start_clock(self):
        """Start clock update."""
        self.clock_timer = QTimer()
        self.clock_timer.timeout.connect(self._update_clock)
        self.clock_timer.start(1000)
        self._update_clock()
    
    def _update_clock(self):
        """Update clock display."""
        current_time = datetime.now().strftime("%H:%M:%S")
        current_date = datetime.now().strftime("%Y-%m-%d")
        self.clock_label.setText(f"{current_time} | {current_date}")
    
    def set_system_state(self, state: str, operation: str = ""):
        """Update system state display."""
        self.current_state = state
        
        state_colors = {
            "operational": PROFESSIONAL_THEME["status_operational"],
            "warning": PROFESSIONAL_THEME["accent_orange"],
            "error": PROFESSIONAL_THEME["accent_red"],
            "processing": PROFESSIONAL_THEME["accent_blue"]
        }
        
        color = state_colors.get(state, PROFESSIONAL_THEME["status_operational"])
        
        self.status_indicator.setText(state.upper())
        self.status_indicator.setStyleSheet(f"color: {color};")
        
        if operation:
            self.active_operations.setText(operation)
        else:
            self.active_operations.setText("IDLE")