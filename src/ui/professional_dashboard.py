#!/usr/bin/env python3
"""Professional Dashboard - Control Room style interface."""

import logging
from typing import Dict, Optional
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QSplitter
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

try:
    from .sphere_manager import SphereManager
    from .left_panel import LeftPanel
    from .right_panel import RightPanel
    from .header_bar import HeaderBar
    from .footer_bar import FooterBar
except ImportError:
    SphereManager = None
    LeftPanel = None
    RightPanel = None
    HeaderBar = None
    FooterBar = None

logger = logging.getLogger("ProfessionalDashboard")

# Professional Control Room Theme
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
    "status_operational": "#4a7a4a",
    "status_warning": "#7a6a4a",
    "status_error": "#7a4a4a",
}


class ProfessionalDashboard(QWidget):
    """Professional control room dashboard interface."""
    
    command_requested = pyqtSignal(str)
    microphone_toggled = pyqtSignal(bool)
    settings_requested = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.current_state = "operational"
        self.system_metrics = {}
        
        self._init_ui()
        self._apply_professional_theme()
        self._connect_signals()
        
        logger.info("✓ ProfessionalDashboard initialized")
    
    def _init_ui(self):
        """Initialize professional dashboard layout."""
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Header Bar (Top)
        if HeaderBar:
            self.header_bar = HeaderBar()
            main_layout.addWidget(self.header_bar)
        else:
            self.header_bar = None
            header_placeholder = self._create_placeholder("HEADER BAR")
            main_layout.addWidget(header_placeholder)
        
        # Main Content Area with Splitter
        main_splitter = QSplitter(Qt.Orientation.Horizontal)
        main_splitter.setHandleWidth(2)
        main_splitter.setStyleSheet("""
            QSplitter::handle {
                background: #2a3a5a;
            }
        """)
        
        # Left Panel (Navigation & Controls)
        if LeftPanel:
            self.left_panel = LeftPanel()
            self.left_panel.setMinimumWidth(250)
            self.left_panel.setMaximumWidth(350)
            main_splitter.addWidget(self.left_panel)
        else:
            self.left_panel = None
            left_placeholder = self._create_placeholder("LEFT PANEL")
            left_placeholder.setFixedWidth(300)
            main_splitter.addWidget(left_placeholder)
        
        # Center Dashboard (Main Display)
        center_widget = self._create_center_dashboard()
        main_splitter.addWidget(center_widget)
        
        # Right Panel (Metrics & System Info)
        if RightPanel:
            self.right_panel = RightPanel()
            self.right_panel.setMinimumWidth(250)
            self.right_panel.setMaximumWidth(350)
            main_splitter.addWidget(self.right_panel)
        else:
            self.right_panel = None
            right_placeholder = self._create_placeholder("RIGHT PANEL")
            right_placeholder.setFixedWidth(300)
            main_splitter.addWidget(right_placeholder)
        
        # Set splitter proportions (15-70-15)
        main_splitter.setStretchFactor(0, 15)
        main_splitter.setStretchFactor(1, 70)
        main_splitter.setStretchFactor(2, 15)
        
        main_layout.addWidget(main_splitter, 1)
        
        # Footer Bar (Bottom)
        if FooterBar:
            self.footer_bar = FooterBar()
            main_layout.addWidget(self.footer_bar)
        else:
            self.footer_bar = None
            footer_placeholder = self._create_placeholder("FOOTER BAR")
            main_layout.addWidget(footer_placeholder)
        
        self.setLayout(main_layout)
    
    def _create_center_dashboard(self) -> QWidget:
        """Create center dashboard area."""
        center_widget = QWidget()
        center_layout = QVBoxLayout()
        center_layout.setContentsMargins(0, 0, 0, 0)
        center_layout.setSpacing(0)
        
        # 3D Sphere / Main Visualization
        if SphereManager:
            self.sphere_manager = SphereManager()
            sphere_widget = self.sphere_manager.get_sphere_widget()
            
            # Add frame around sphere
            sphere_frame = QWidget()
            sphere_frame.setStyleSheet(f"""
                QWidget {{
                    background: {PROFESSIONAL_THEME["panel_bg"]};
                    border: 1px solid {PROFESSIONAL_THEME["panel_border"]};
                }}
            """)
            sphere_layout = QVBoxLayout(sphere_frame)
            sphere_layout.setContentsMargins(0, 0, 0, 0)
            sphere_layout.addWidget(sphere_widget)
            center_layout.addWidget(sphere_frame, 3)
            
        else:
            sphere_placeholder = self._create_placeholder("3D VISUALIZATION")
            center_layout.addWidget(sphere_placeholder, 3)
            self.sphere_manager = None
        
        # Status Display Area
        self.status_display = QWidget()
        self.status_display.setStyleSheet(f"""
            QWidget {{
                background: {PROFESSIONAL_THEME["panel_bg"]};
                border-top: 1px solid {PROFESSIONAL_THEME["panel_border"]};
                border-left: 1px solid {PROFESSIONAL_THEME["panel_border"]};
                border-right: 1px solid {PROFESSIONAL_THEME["panel_border"]};
            }}
        """)
        status_layout = QVBoxLayout(self.status_display)
        status_layout.setContentsMargins(15, 10, 15, 10)
        
        from PyQt6.QtWidgets import QLabel
        self.system_status_label = QLabel("SYSTEM: OPERATIONAL")
        self.system_status_label.setFont(QFont("Courier New", 12, QFont.Weight.Bold))
        self.system_status_label.setStyleSheet(f"color: {PROFESSIONAL_THEME['status_operational']};")
        status_layout.addWidget(self.system_status_label)
        
        self.current_operation_label = QLabel("OPERATION: IDLE")
        self.current_operation_label.setFont(QFont("Courier New", 10))
        self.current_operation_label.setStyleSheet(f"color: {PROFESSIONAL_THEME['text_secondary']};")
        status_layout.addWidget(self.current_operation_label)
        
        center_layout.addWidget(self.status_display, 1)
        
        center_widget.setLayout(center_layout)
        return center_widget
    
    def _create_placeholder(self, text: str) -> QWidget:
        """Create placeholder panel when component not available."""
        placeholder = QWidget()
        placeholder.setStyleSheet(f"""
            QWidget {{
                background: {PROFESSIONAL_THEME["panel_bg"]};
                border: 1px solid {PROFESSIONAL_THEME["panel_border"]};
            }}
        """)
        layout = QVBoxLayout(placeholder)
        
        from PyQt6.QtWidgets import QLabel
        label = QLabel(text)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        label.setStyleSheet(f"color: {PROFESSIONAL_THEME['text_secondary']};")
        layout.addWidget(label)
        
        placeholder.setLayout(layout)
        return placeholder
    
    def _apply_professional_theme(self):
        """Apply professional control room theme."""
        self.setStyleSheet(f"""
            ProfessionalDashboard {{
                background: #0a0e27;
            }}
        """)
    
    def _connect_signals(self):
        """Connect signals from panels."""
        if self.left_panel:
            self.left_panel.command_requested.connect(self.command_requested.emit)
            self.left_panel.microphone_toggled.connect(self._toggle_microphone)
        
        if self.right_panel:
            self.right_panel.settings_requested.connect(self.settings_requested.emit)
    
    def _toggle_microphone(self, active: bool):
        """Toggle microphone with visual feedback."""
        self.microphone_toggled.emit(active)
        
        if active:
            self.system_status_label.setText("SYSTEM: ACTIVE LISTENING")
            self.system_status_label.setStyleSheet(f"color: {PROFESSIONAL_THEME['accent_blue']};")
            self.current_operation_label.setText("OPERATION: VOICE INPUT")
            if self.sphere_manager:
                self.sphere_manager.set_state("listening")
        else:
            self.system_status_label.setText("SYSTEM: OPERATIONAL")
            self.system_status_label.setStyleSheet(f"color: {PROFESSIONAL_THEME['status_operational']};")
            self.current_operation_label.setText("OPERATION: IDLE")
            if self.sphere_manager:
                self.sphere_manager.set_state("idle")
        
        if self.left_panel:
            self.left_panel.update_microphone_status(active)
    
    def set_system_state(self, state: str, operation: str = ""):
        """Set overall system state."""
        self.current_state = state
        
        state_colors = {
            "operational": PROFESSIONAL_THEME["status_operational"],
            "warning": PROFESSIONAL_THEME["status_warning"],
            "error": PROFESSIONAL_THEME["status_error"],
            "processing": PROFESSIONAL_THEME["accent_orange"]
        }
        
        color = state_colors.get(state, PROFESSIONAL_THEME["status_operational"])
        
        self.system_status_label.setText(f"SYSTEM: {state.upper()}")
        self.system_status_label.setStyleSheet(f"color: {color};")
        
        if operation:
            self.current_operation_label.setText(f"OPERATION: {operation}")
        
        if self.sphere_manager:
            self.sphere_manager.set_state(state)
        
        if self.left_panel:
            self.left_panel.update_system_state(state)
        
        if self.right_panel:
            self.right_panel.update_system_state(state)
    
    def update_metrics(self, metrics: Dict):
        """Update system metrics display."""
        self.system_metrics = metrics
        
        if self.right_panel:
            self.right_panel.update_metrics(metrics)
        
        if self.footer_bar:
            self.footer_bar.update_metrics(metrics)


def launch_professional_ui():
    """Launch AYKO professional control room interface."""
    import sys
    try:
        from PyQt6.QtWidgets import QApplication
    except ImportError:
        print("PyQt6 not found. Run: pip install PyQt6 PyQt6-WebEngine")
        sys.exit(1)

    app = QApplication(sys.argv)
    app.setApplicationName("AYKO")
    app.setApplicationVersion("0.0.01")

    window = ProfessionalDashboard()
    window.setWindowTitle("AYKO v0.0.01 - Professional Control Room")
    window.setGeometry(50, 50, 1600, 900)
    window.show()

    print("🏛️ AYKO Professional Control Room started successfully")
    print("📊 Monitor metrics and control systems from main dashboard")
    
    import sys
    sys.exit(app.exec())


if __name__ == "__main__":
    launch_professional_ui()