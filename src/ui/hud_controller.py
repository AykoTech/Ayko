#!/usr/bin/env python3
"""HUD Controller - Cinematic Marvel-style HUD elements."""

import logging
import random
from typing import Dict
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QFont

logger = logging.getLogger("HUDController")


class DataStreamLabel(QLabel):
    """Animated data stream label."""
    
    def __init__(self, text: str = ""):
        super().__init__(text)
        self.streaming_text = []
        self.timer = QTimer()
        self.timer.timeout.connect(self._update_stream)
        self.timer.start(50)
    
    def _update_stream(self):
        """Update streaming text effect."""
        chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%&*"
        if random.random() < 0.3:
            char = random.choice(chars)
            self.streaming_text.append(char)
            if len(self.streaming_text) > 40:
                self.streaming_text.pop(0)
            self.setText("".join(self.streaming_text))
    
    def set_streaming(self, active: bool):
        """Enable/disable streaming effect."""
        if active:
            self.timer.start()
        else:
            self.timer.stop()


class HUDController(QWidget):
    """Cinematic HUD controller with Marvel-style elements."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.current_mode = "idle"
        self.data_streams = []
        self.metrics = {}
        
        self._init_hud()
        self._setup_data_streams()
        self._start_updates()
        
        logger.info("✓ HUDController initialized")
    
    def _init_hud(self):
        """Initialize HUD layout."""
        self.setFixedHeight(120)
        self.setStyleSheet("""
            HUDController {
                background: rgba(10, 14, 39, 0.9);
                border-top: 2px solid #00BFFF;
            }
        """)
        
        layout = QHBoxLayout()
        layout.setContentsMargins(15, 10, 15, 10)
        layout.setSpacing(20)
        
        # Left: System Status
        status_panel = self._create_status_panel()
        layout.addWidget(status_panel, 2)
        
        # Center: Data Streams
        streams_panel = self._create_data_streams_panel()
        layout.addWidget(streams_panel, 4)
        
        # Right: Metrics
        metrics_panel = self._create_metrics_panel()
        layout.addWidget(metrics_panel, 2)
        
        self.setLayout(layout)
    
    def _create_status_panel(self) -> QWidget:
        """Create system status panel."""
        panel = QFrame()
        panel.setStyleSheet("""
            QFrame {
                background: rgba(0, 191, 255, 0.1);
                border: 1px solid #00BFFF;
                border-radius: 5px;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 5, 10, 5)
        
        title = QLabel("SYSTEM STATUS")
        title.setFont(QFont("Courier New", 10, QFont.Weight.Bold))
        title.setStyleSheet("color: #00BFFF;")
        layout.addWidget(title)
        
        self.system_status = QLabel("OPERATIONAL")
        self.system_status.setFont(QFont("Courier New", 14, QFont.Weight.Bold))
        self.system_status.setStyleSheet("color: #00FF41;")
        layout.addWidget(self.system_status)
        
        self.sub_status = QLabel("All systems nominal")
        self.sub_status.setFont(QFont("Courier New", 8))
        self.sub_status.setStyleSheet("color: #A0A0A0;")
        layout.addWidget(self.sub_status)
        
        panel.setLayout(layout)
        return panel
    
    def _create_data_streams_panel(self) -> QWidget:
        """Create animated data streams panel."""
        panel = QFrame()
        panel.setStyleSheet("""
            QFrame {
                background: rgba(255, 215, 0, 0.05);
                border: 1px solid #FFD700;
                border-radius: 5px;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 5, 10, 5)
        
        title = QLabel("DATA STREAMS")
        title.setFont(QFont("Courier New", 10, QFont.Weight.Bold))
        title.setStyleSheet("color: #FFD700;")
        layout.addWidget(title)
        
        for i in range(3):
            stream = DataStreamLabel()
            stream.setFont(QFont("Courier New", 8))
            stream.setStyleSheet("color: #FFD700;")
            self.data_streams.append(stream)
            layout.addWidget(stream)
        
        panel.setLayout(layout)
        return panel
    
    def _create_metrics_panel(self) -> QWidget:
        """Create system metrics panel."""
        panel = QFrame()
        panel.setStyleSheet("""
            QFrame {
                background: rgba(0, 255, 65, 0.05);
                border: 1px solid #00FF41;
                border-radius: 5px;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 5, 10, 5)
        
        title = QLabel("SYSTEM METRICS")
        title.setFont(QFont("Courier New", 10, QFont.Weight.Bold))
        title.setStyleSheet("color: #00FF41;")
        layout.addWidget(title)
        
        self.cpu_label = QLabel("CPU: --")
        self.cpu_label.setFont(QFont("Courier New", 9))
        self.cpu_label.setStyleSheet("color: #E0E0E0;")
        layout.addWidget(self.cpu_label)
        
        self.memory_label = QLabel("MEM: --")
        self.memory_label.setFont(QFont("Courier New", 9))
        self.memory_label.setStyleSheet("color: #E0E0E0;")
        layout.addWidget(self.memory_label)
        
        self.network_label = QLabel("NET: --")
        self.network_label.setFont(QFont("Courier New", 9))
        self.network_label.setStyleSheet("color: #E0E0E0;")
        layout.addWidget(self.network_label)
        
        panel.setLayout(layout)
        return panel
    
    def _setup_data_streams(self):
        """Setup data streaming content."""
        stream_content = [
            "JARVIS_PROTOCOL_INIT",
            "NEURAL_LINK_ESTABLISHED", 
            "VOICE_RECOGNITION_ACTIVE",
            "QUANTUM_PROCESSING",
            "ARC_REACTOR_ONLINE"
        ]
        
        for i, stream in enumerate(self.data_streams):
            stream.setText(stream_content[i % len(stream_content)])
    
    def _start_updates(self):
        """Start periodic HUD updates."""
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self._update_metrics)
        self.update_timer.start(1000)
    
    def _update_metrics(self):
        """Update system metrics display."""
        try:
            import psutil
            
            cpu_percent = psutil.cpu_percent(interval=0.1)
            self.cpu_label.setText(f"CPU: {cpu_percent}%")
            
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            self.memory_label.setText(f"MEM: {memory_percent}%")
            
            network_status = "CONNECTED" if random.random() > 0.1 else "STANDBY"
            self.network_label.setText(f"NET: {network_status}")
            
            self.metrics = {
                "cpu": cpu_percent,
                "memory": memory_percent,
                "network": network_status
            }
            
        except ImportError:
            self.cpu_label.setText("CPU: N/A")
            self.memory_label.setText("MEM: N/A")
            self.network_label.setText("NET: OFFLINE")
    
    def set_mode(self, mode: str):
        """Set HUD mode based on system state."""
        self.current_mode = mode
        
        mode_config = {
            "idle": {
                "status": "OPERATIONAL",
                "sub_status": "All systems nominal",
                "status_color": "#00FF41",
                "sub_color": "#A0A0A0"
            },
            "listening": {
                "status": "RECEIVING INPUT",
                "sub_status": "Voice recognition active",
                "status_color": "#00BFFF",
                "sub_color": "#00BFFF"
            },
            "processing": {
                "status": "PROCESSING",
                "sub_status": "Neural computation in progress",
                "status_color": "#FFD700",
                "sub_color": "#FFD700"
            },
            "speaking": {
                "status": "SPEAKING",
                "sub_status": "Audio synthesis active",
                "status_color": "#00FF41",
                "sub_color": "#00FF41"
            },
            "error": {
                "status": "ERROR DETECTED",
                "sub_status": "System malfunction",
                "status_color": "#FF3333",
                "sub_color": "#FF3333"
            }
        }
        
        config = mode_config.get(mode, mode_config["idle"])
        
        self.system_status.setText(config["status"])
        self.system_status.setStyleSheet(f"color: {config['status_color']};")
        self.sub_status.setText(config["sub_status"])
        self.sub_status.setStyleSheet(f"color: {config['sub_color']};")
    
    def get_metrics(self) -> Dict:
        """Get current system metrics."""
        return self.metrics