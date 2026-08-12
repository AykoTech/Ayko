#!/usr/bin/env python3
"""Footer Bar - Timeline and system states."""

import logging
from typing import List
from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QLabel, QPushButton, QScrollArea,
    QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QFont

logger = logging.getLogger("FooterBar")

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


class FooterBar(QWidget):
    """Professional footer bar with timeline and system states."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.timeline_entries = []
        self.current_operation = ""
        self.operation_progress = 0
        
        self._init_ui()
        self._apply_professional_theme()
        
        logger.info("✓ FooterBar initialized")
    
    def _init_ui(self):
        """Initialize footer bar layout."""
        self.setFixedHeight(40)
        
        layout = QHBoxLayout()
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(10)
        
        # Timeline Section
        timeline_section = self._create_timeline_section()
        layout.addWidget(timeline_section, 1)
        
        # Operation Progress
        progress_section = self._create_progress_section()
        layout.addWidget(progress_section, 2)
        
        # System States
        states_section = self._create_states_section()
        layout.addWidget(states_section, 1)
        
        self.setLayout(layout)
    
    def _create_timeline_section(self) -> QWidget:
        """Create timeline section."""
        widget = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)
        
        timeline_label = QLabel("TIMELINE:")
        timeline_label.setStyleSheet(f"color: {PROFESSIONAL_THEME['text_secondary']};")
        timeline_label.setFont(QFont("Arial", 9))
        layout.addWidget(timeline_label)
        
        self.timeline_display = QLabel("System initialized")
        self.timeline_display.setFont(QFont("Courier New", 9))
        self.timeline_display.setStyleSheet(f"color: {PROFESSIONAL_THEME['text_primary']};")
        layout.addWidget(self.timeline_display, 1)
        
        widget.setLayout(layout)
        return widget
    
    def _create_progress_section(self) -> QWidget:
        """Create operation progress section."""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)
        
        # Operation Name
        self.operation_name = QLabel("CURRENT OPERATION: NONE")
        self.operation_name.setFont(QFont("Arial", 9, QFont.Weight.Bold))
        self.operation_name.setStyleSheet(f"color: {PROFESSIONAL_THEME['text_primary']};")
        layout.addWidget(self.operation_name)
        
        # Progress Bar
        from PyQt6.QtWidgets import QProgressBar
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.setStyleSheet(f"""
            QProgressBar {{
                background: {PROFESSIONAL_THEME["panel_bg"]};
                border: 1px solid {PROFESSIONAL_THEME["panel_border"]};
                border-radius: 2px;
                text-align: center;
                font-size: 8px;
            }}
            QProgressBar::chunk {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {PROFESSIONAL_THEME["accent_blue"]},
                    stop:1 {PROFESSIONAL_THEME["accent_blue"]});
            }}
        """)
        layout.addWidget(self.progress_bar)
        
        widget.setLayout(layout)
        return widget
    
    def _create_states_section(self) -> QWidget:
        """Create system states section."""
        widget = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)
        
        # State Indicators
        self.voice_state = self._create_state_indicator("VOICE", "OFFLINE")
        layout.addWidget(self.voice_state)
        
        self.ai_state = self._create_state_indicator("AI", "READY")
        layout.addWidget(self.ai_state)
        
        self.tts_state = self._create_state_indicator("TTS", "READY")
        layout.addWidget(self.tts_state)
        
        self.audio_state = self._create_state_indicator("AUDIO", "READY")
        layout.addWidget(self.audio_state)
        
        widget.setLayout(layout)
        return widget
    
    def _create_state_indicator(self, label: str, status: str) -> QWidget:
        """Create individual state indicator."""
        widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)
        
        # Indicator dot
        indicator = QLabel("●")
        indicator.setAlignment(Qt.AlignmentFlag.AlignCenter)
        indicator.setStyleSheet(f"color: {PROFESSIONAL_THEME['text_secondary']}; font-size: 12px;")
        layout.addWidget(indicator)
        
        # Label
        state_label = QLabel(f"{label}: {status}")
        state_label.setFont(QFont("Arial", 8))
        state_label.setStyleSheet(f"color: {PROFESSIONAL_THEME['text_secondary']};")
        state_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(state_label)
        
        widget.setLayout(layout)
        return widget
    
    def _apply_professional_theme(self):
        """Apply professional theme to footer."""
        self.setStyleSheet(f"""
            FooterBar {{
                background: {PROFESSIONAL_THEME["header_bg"]};
                border-top: 2px solid {PROFESSIONAL_THEME["panel_border"]};
            }}
        """)
    
    def add_timeline_entry(self, entry: str):
        """Add entry to timeline."""
        self.timeline_entries.append(entry)
        if len(self.timeline_entries) > 3:
            self.timeline_entries.pop(0)
        
        self.timeline_display.setText(" → ".join(self.timeline_entries[-3:]))
    
    def set_operation(self, operation: str, progress: int = 0):
        """Set current operation and progress."""
        self.current_operation = operation
        self.operation_name.setText(f"CURRENT OPERATION: {operation}")
        self.progress_bar.setValue(progress)
    
    def update_state(self, component: str, state: str):
        """Update component state indicator."""
        state_colors = {
            "online": PROFESSIONAL_THEME["accent_green"],
            "ready": PROFESSIONAL_THEME["accent_green"],
            "active": PROFESSIONAL_THEME["accent_blue"],
            "offline": PROFESSIONAL_THEME["text_secondary"],
            "error": PROFESSIONAL_THEME["accent_red"],
            "processing": PROFESSIONAL_THEME["accent_orange"]
        }
        
        color = state_colors.get(state.lower(), PROFESSIONAL_THEME["text_secondary"])
        
        # Update the specific component indicator
        if component == "VOICE":
            self.voice_state.children()[0].setStyleSheet(f"color: {color}; font-size: 12px;")
            self.voice_state.children()[1].setText(f"VOICE: {state.upper()}")
        elif component == "AI":
            self.ai_state.children()[0].setStyleSheet(f"color: {color}; font-size: 12px;")
            self.ai_state.children()[1].setText(f"AI: {state.upper()}")
        elif component == "TTS":
            self.tts_state.children()[0].setStyleSheet(f"color: {color}; font-size: 12px;")
            self.tts_state.children()[1].setText(f"TTS: {state.upper()}")
        elif component == "AUDIO":
            self.audio_state.children()[0].setStyleSheet(f"color: {color}; font-size: 12px;")
            self.audio_state.children()[1].setText(f"AUDIO: {state.upper()}")
    
    def update_metrics(self, metrics: dict):
        """Update metrics display in footer."""
        pass