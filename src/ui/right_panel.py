#!/usr/bin/env python3
"""Right Panel - Metrics and system information."""

import logging
import platform
try:
    import psutil
except ImportError:
    psutil = None
from typing import Dict
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QProgressBar, QGroupBox, QScrollArea
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QFont

logger = logging.getLogger("RightPanel")

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


class RightPanel(QWidget):
    """Professional right panel with metrics and system info."""
    
    settings_requested = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.current_state = "operational"
        self.metrics = {}
        
        self._init_ui()
        self._apply_professional_theme()
        self._start_metrics_update()
        
        logger.info("✓ RightPanel initialized")
    
    def _init_ui(self):
        """Initialize right panel layout."""
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)
        
        # System Metrics Section
        metrics_section = self._create_system_metrics_section()
        layout.addWidget(metrics_section)
        
        # Performance Metrics Section
        performance_section = self._create_performance_section()
        layout.addWidget(performance_section)
        
        # Network Status Section
        network_section = self._create_network_section()
        layout.addWidget(network_section)
        
        # Storage Section
        storage_section = self._create_storage_section()
        layout.addWidget(storage_section)
        
        # System Info Section
        info_section = self._create_system_info_section()
        layout.addWidget(info_section)
        
        # Settings Button
        settings_btn = QPushButton("⚙️ SETTINGS")
        settings_btn.setStyleSheet(self._get_main_button_style())
        settings_btn.clicked.connect(self.settings_requested.emit)
        layout.addWidget(settings_btn)
        
        self.setLayout(layout)
    
    def _create_system_metrics_section(self) -> QWidget:
        """Create system metrics section."""
        section = QGroupBox("SYSTEM METRICS")
        section.setStyleSheet(self._get_section_style())
        
        layout = QVBoxLayout()
        layout.setSpacing(10)
        
        # CPU Metric
        cpu_label = QLabel("CPU USAGE:")
        cpu_label.setStyleSheet(f"color: {PROFESSIONAL_THEME['text_secondary']};")
        layout.addWidget(cpu_label)
        
        self.cpu_bar = QProgressBar()
        self.cpu_bar.setStyleSheet(self._get_progress_style())
        self.cpu_bar.setValue(45)
        layout.addWidget(self.cpu_bar)
        
        self.cpu_value_label = QLabel("45%")
        self.cpu_value_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.cpu_value_label.setStyleSheet(f"color: {PROFESSIONAL_THEME['text_primary']};")
        layout.addWidget(self.cpu_value_label)
        
        # Memory Metric
        mem_label = QLabel("MEMORY USAGE:")
        mem_label.setStyleSheet(f"color: {PROFESSIONAL_THEME['text_secondary']};")
        layout.addWidget(mem_label)
        
        self.memory_bar = QProgressBar()
        self.memory_bar.setStyleSheet(self._get_progress_style())
        self.memory_bar.setValue(62)
        layout.addWidget(self.memory_bar)
        
        self.memory_value_label = QLabel("62%")
        self.memory_value_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.memory_value_label.setStyleSheet(f"color: {PROFESSIONAL_THEME['text_primary']};")
        layout.addWidget(self.memory_value_label)
        
        # Thread Count
        threads_layout = QHBoxLayout()
        threads_label = QLabel("THREADS:")
        threads_label.setStyleSheet(f"color: {PROFESSIONAL_THEME['text_secondary']};")
        threads_layout.addWidget(threads_label)
        
        self.threads_value = QLabel("24")
        self.threads_value.setStyleSheet(f"color: {PROFESSIONAL_THEME['text_primary']};")
        threads_layout.addWidget(self.threads_value)
        threads_layout.addStretch()
        layout.addLayout(threads_layout)
        
        section.setLayout(layout)
        return section
    
    def _create_performance_section(self) -> QWidget:
        """Create performance metrics section."""
        section = QGroupBox("PERFORMANCE")
        section.setStyleSheet(self._get_section_style())
        
        layout = QVBoxLayout()
        layout.setSpacing(8)
        
        # Response Time
        response_layout = QHBoxLayout()
        response_label = QLabel("RESPONSE TIME:")
        response_label.setStyleSheet(f"color: {PROFESSIONAL_THEME['text_secondary']};")
        response_layout.addWidget(response_label)
        
        self.response_value = QLabel("120ms")
        self.response_value.setStyleSheet(f"color: {PROFESSIONAL_THEME['accent_green']};")
        response_layout.addWidget(self.response_value)
        response_layout.addStretch()
        layout.addLayout(response_layout)
        
        # Process Count
        process_layout = QHBoxLayout()
        process_label = QLabel("PROCESSES:")
        process_label.setStyleSheet(f"color: {PROFESSIONAL_THEME['text_secondary']};")
        process_layout.addWidget(process_label)
        
        self.process_value = QLabel("156")
        self.process_value.setStyleSheet(f"color: {PROFESSIONAL_THEME['text_primary']};")
        process_layout.addWidget(self.process_value)
        process_layout.addStretch()
        layout.addLayout(process_layout)
        
        # Uptime
        uptime_layout = QHBoxLayout()
        uptime_label = QLabel("UPTIME:")
        uptime_label.setStyleSheet(f"color: {PROFESSIONAL_THEME['text_secondary']};")
        uptime_layout.addWidget(uptime_label)
        
        self.uptime_value = QLabel("02:34:56")
        self.uptime_value.setStyleSheet(f"color: {PROFESSIONAL_THEME['text_primary']};")
        uptime_layout.addWidget(self.uptime_value)
        uptime_layout.addStretch()
        layout.addLayout(uptime_layout)
        
        section.setLayout(layout)
        return section
    
    def _create_network_section(self) -> QWidget:
        """Create network status section."""
        section = QGroupBox("NETWORK STATUS")
        section.setStyleSheet(self._get_section_style())
        
        layout = QVBoxLayout()
        layout.setSpacing(8)
        
        # Connection Status
        conn_layout = QHBoxLayout()
        conn_label = QLabel("CONNECTION:")
        conn_label.setStyleSheet(f"color: {PROFESSIONAL_THEME['text_secondary']};")
        conn_layout.addWidget(conn_label)
        
        self.conn_status = QLabel("CONNECTED")
        self.conn_status.setStyleSheet(f"color: {PROFESSIONAL_THEME['accent_green']};")
        conn_layout.addWidget(self.conn_status)
        conn_layout.addStretch()
        layout.addLayout(conn_layout)
        
        # Network I/O
        net_layout = QHBoxLayout()
        net_label = QLabel("NETWORK I/O:")
        net_label.setStyleSheet(f"color: {PROFESSIONAL_THEME['text_secondary']};")
        net_layout.addWidget(net_label)
        
        self.net_value = QLabel("1.2 MB/s")
        self.net_value.setStyleSheet(f"color: {PROFESSIONAL_THEME['text_primary']};")
        net_layout.addWidget(self.net_value)
        net_layout.addStretch()
        layout.addLayout(net_layout)
        
        section.setLayout(layout)
        return section
    
    def _create_storage_section(self) -> QWidget:
        """Create storage information section."""
        section = QGroupBox("STORAGE")
        section.setStyleSheet(self._get_section_style())
        
        layout = QVBoxLayout()
        layout.setSpacing(8)
        
        # Disk Usage
        disk_label = QLabel("DISK USAGE:")
        disk_label.setStyleSheet(f"color: {PROFESSIONAL_THEME['text_secondary']};")
        layout.addWidget(disk_label)
        
        self.disk_bar = QProgressBar()
        self.disk_bar.setStyleSheet(self._get_progress_style())
        self.disk_bar.setValue(73)
        layout.addWidget(self.disk_bar)
        
        self.disk_value_label = QLabel("73% (234.5 GB / 320 GB)")
        self.disk_value_label.setStyleSheet(f"color: {PROFESSIONAL_THEME['text_primary']};")
        self.disk_value_label.setFont(QFont("Arial", 9))
        layout.addWidget(self.disk_value_label)
        
        # Available Space
        avail_layout = QHBoxLayout()
        avail_label = QLabel("AVAILABLE:")
        avail_label.setStyleSheet(f"color: {PROFESSIONAL_THEME['text_secondary']};")
        avail_layout.addWidget(avail_label)
        
        self.avail_value = QLabel("85.5 GB")
        self.avail_value.setStyleSheet(f"color: {PROFESSIONAL_THEME['text_primary']};")
        avail_layout.addWidget(self.avail_value)
        avail_layout.addStretch()
        layout.addLayout(avail_layout)
        
        section.setLayout(layout)
        return section
    
    def _create_system_info_section(self) -> QWidget:
        """Create system information section."""
        section = QGroupBox("SYSTEM INFO")
        section.setStyleSheet(self._get_section_style())
        
        layout = QVBoxLayout()
        layout.setSpacing(8)
        
        # OS Information
        os_info = f"{platform.system()} {platform.release()}"
        os_label = QLabel(f"OS: {os_info}")
        os_label.setStyleSheet(f"color: {PROFESSIONAL_THEME['text_primary']};")
        os_label.setFont(QFont("Arial", 9))
        layout.addWidget(os_label)
        
        # Python Version
        py_label = QLabel(f"Python: {platform.python_version()}")
        py_label.setStyleSheet(f"color: {PROFESSIONAL_THEME['text_primary']};")
        py_label.setFont(QFont("Arial", 9))
        layout.addWidget(py_label)
        
        # CPU Information
        cpu_info = f"CPU: {platform.processor()}"
        cpu_label = QLabel(cpu_info)
        cpu_label.setStyleSheet(f"color: {PROFESSIONAL_THEME['text_primary']};")
        cpu_label.setFont(QFont("Arial", 9))
        layout.addWidget(cpu_label)
        
        # Memory Information (if psutil available)
        if psutil:
            mem = psutil.virtual_memory()
            mem_info = f"RAM: {mem.total // (1024**3)} GB"
            mem_label = QLabel(mem_info)
            mem_label.setStyleSheet(f"color: {PROFESSIONAL_THEME['text_primary']};")
            mem_label.setFont(QFont("Arial", 9))
            layout.addWidget(mem_label)
        else:
            mem_label = QLabel("RAM: N/A (install psutil)")
            mem_label.setStyleSheet(f"color: {PROFESSIONAL_THEME['text_secondary']};")
            mem_label.setFont(QFont("Arial", 9))
            layout.addWidget(mem_label)
        
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
    
    def _get_progress_style(self) -> str:
        """Get progress bar style."""
        return f"""
            QProgressBar {{
                background: {PROFESSIONAL_THEME["panel_bg"]};
                border: 1px solid {PROFESSIONAL_THEME["panel_border"]};
                border-radius: 3px;
                text-align: center;
                color: {PROFESSIONAL_THEME["text_primary"]};
            }}
            QProgressBar::chunk {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {PROFESSIONAL_THEME["accent_blue"]},
                    stop:1 {PROFESSIONAL_THEME["accent_blue"]});
                }}
        """
    
    def _get_main_button_style(self) -> str:
        """Get main button style."""
        return f"""
            QPushButton {{
                background: {PROFESSIONAL_THEME["accent_blue"]};
                color: white;
                border: 1px solid {PROFESSIONAL_THEME["accent_blue"]};
                border-radius: 3px;
                padding: 12px;
                font-weight: bold;
                font-size: 10px;
            }}
            QPushButton:hover {{
                background: {PROFESSIONAL_THEME["panel_bg"]};
                color: {PROFESSIONAL_THEME["accent_blue"]};
            }}
        """
    
    def _apply_professional_theme(self):
        """Apply professional theme to panel."""
        self.setStyleSheet(f"""
            RightPanel {{
                background: {PROFESSIONAL_THEME["panel_bg"]};
                border-left: 1px solid {PROFESSIONAL_THEME["panel_border"]};
            }}
        """)
    
    def _start_metrics_update(self):
        """Start periodic metrics update."""
        if not psutil:
            logger.warning("psutil not available, metrics update disabled")
            self._update_metrics()  # Set to N/A once
            return
        
        self.metrics_timer = QTimer()
        self.metrics_timer.timeout.connect(self._update_metrics)
        self.metrics_timer.start(1000)
    
    def _update_metrics(self):
        """Update system metrics."""
        if not psutil:
            # If psutil not available, show N/A
            self.cpu_bar.setValue(0)
            self.cpu_value_label.setText("N/A")
            self.memory_bar.setValue(0)
            self.memory_value_label.setText("N/A")
            self.threads_value.setText("N/A")
            self.process_value.setText("N/A")
            return
        
        try:
            # CPU
            cpu_percent = psutil.cpu_percent(interval=0.1)
            self.cpu_bar.setValue(cpu_percent)
            self.cpu_value_label.setText(f"{cpu_percent}%")
            
            # Memory
            memory = psutil.virtual_memory()
            mem_percent = memory.percent
            self.memory_bar.setValue(mem_percent)
            self.memory_value_label.setText(f"{mem_percent}%")
            
            # Threads
            threads = psutil.cpu_count()
            self.threads_value.setText(str(threads))
            
            # Processes
            processes = len(psutil.pids())
            self.process_value.setText(str(processes))
            
            # Update metrics dict
            self.metrics = {
                "cpu": cpu_percent,
                "memory": mem_percent,
                "threads": threads,
                "processes": processes
            }
            
        except Exception as e:
            logger.error(f"Failed to update metrics: {e}")
    
    def update_metrics(self, metrics: Dict):
        """Update metrics from external source."""
        if "cpu" in metrics:
            self.cpu_bar.setValue(metrics["cpu"])
            self.cpu_value_label.setText(f"{metrics['cpu']}%")
        
        if "memory" in metrics:
            self.memory_bar.setValue(metrics["memory"])
            self.memory_value_label.setText(f"{metrics['memory']}%")
    
    def update_system_state(self, state: str):
        """Update system state display."""
        self.current_state = state
        
        state_colors = {
            "operational": PROFESSIONAL_THEME["accent_green"],
            "warning": PROFESSIONAL_THEME["accent_orange"],
            "error": PROFESSIONAL_THEME["accent_red"],
            "processing": PROFESSIONAL_THEME["accent_blue"]
        }
        
        color = state_colors.get(state, PROFESSIONAL_THEME["accent_green"])
        
        if hasattr(self, 'conn_status'):
            if state == "error":
                self.conn_status.setText("DISCONNECTED")
                self.conn_status.setStyleSheet(f"color: {PROFESSIONAL_THEME['accent_red']};")
            else:
                self.conn_status.setText("CONNECTED")
                self.conn_status.setStyleSheet(f"color: {PROFESSIONAL_THEME['accent_green']};")