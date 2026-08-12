#!/usr/bin/env python3
"""Audio Visualizer - Real-time waveform visualization."""

import logging
import math
from typing import List
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush, QPainterPath, QLinearGradient

logger = logging.getLogger("AudioVisualizer")


class AudioVisualizer(QWidget):
    """Real-time audio waveform visualizer with cinematic effects."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.audio_data = []
        self.max_data_points = 100
        self.is_active = False
        
        self.waveform_color = QColor(0, 191, 255)  # Arc Reactor Blue
        self.background_color = QColor(10, 14, 39, 200)
        
        self.setMinimumHeight(80)
        self.setStyleSheet("""
            AudioVisualizer {
                background: rgba(10, 14, 39, 0.8);
                border: 1px solid #00BFFF;
                border-radius: 5px;
            }
        """)
        
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self._animate)
        self.animation_timer.start(30)
        
        self.phase = 0.0
        
        logger.info("✓ AudioVisualizer initialized")
    
    def update_waveform(self, audio_data: List[float]):
        """Update waveform with new audio data."""
        self.audio_data = audio_data[-self.max_data_points:]
        self.is_active = len(audio_data) > 0
        self.update()
    
    def _animate(self):
        """Animation loop for visual effects."""
        if self.is_active:
            self.phase += 0.1
            self.update()
    
    def paintEvent(self, event):
        """Paint the audio visualization."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        painter.fillRect(self.rect(), self.background_color)
        self._draw_grid(painter)
        
        if self.audio_data:
            self._draw_waveform(painter)
        else:
            self._draw_idle_waveform(painter)
    
    def _draw_grid(self, painter: QPainter):
        """Draw cinematic grid lines."""
        pen = QPen(QColor(0, 191, 255, 50))
        pen.setWidth(1)
        painter.setPen(pen)
        
        for i in range(0, self.height(), 20):
            painter.drawLine(0, i, self.width(), i)
        
        for i in range(0, self.width(), 40):
            painter.drawLine(i, 0, i, self.height())
    
    def _draw_waveform(self, painter: QPainter):
        """Draw actual audio waveform."""
        if not self.audio_data:
            return
        
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0.0, QColor(0, 191, 255, 200))
        gradient.setColorAt(0.5, QColor(0, 255, 65, 200))
        gradient.setColorAt(1.0, QColor(0, 191, 255, 200))
        
        pen = QPen(gradient)
        pen.setWidth(2)
        painter.setPen(pen)
        
        path = QPainterPath()
        
        width = self.width()
        height = self.height()
        mid_height = height / 2
        
        if len(self.audio_data) > 1:
            step = width / len(self.audio_data)
            
            for i, value in enumerate(self.audio_data):
                x = i * step
                normalized = max(-1, min(1, value))
                y = mid_height + (normalized * mid_height * 0.8)
                
                if i == 0:
                    path.moveTo(x, y)
                else:
                    prev_x = (i - 1) * step
                    prev_value = max(-1, min(1, self.audio_data[i - 1]))
                    prev_y = mid_height + (prev_value * mid_height * 0.8)
                    
                    cx = (prev_x + x) / 2
                    path.quadTo(cx, prev_y, x, y)
        
        painter.drawPath(path)
        
        painter.setPen(Qt.PenStyle.NoPen)
        glow_color = QColor(0, 191, 255, 50)
        painter.setBrush(glow_color)
        
        if len(self.audio_data) > 1:
            glow_path = QPainterPath()
            step = width / len(self.audio_data)
            
            glow_path.moveTo(0, mid_height)
            
            for i, value in enumerate(self.audio_data):
                x = i * step
                normalized = max(-1, min(1, value))
                y = mid_height + (normalized * mid_height * 0.8)
                glow_path.lineTo(x, y)
            
            glow_path.lineTo(width, mid_height)
            glow_path.closeSubpath()
            
            painter.drawPath(glow_path)
    
    def _draw_idle_waveform(self, painter: QPainter):
        """Draw idle animation when no audio."""
        width = self.width()
        height = self.height()
        mid_height = height / 2
        
        pen = QPen(QColor(0, 191, 255, 100))
        pen.setWidth(1)
        painter.setPen(pen)
        
        path = QPainterPath()
        
        for x in range(0, width, 2):
            y = mid_height + math.sin((x / 50.0) + self.phase) * 10
            
            if x == 0:
                path.moveTo(x, y)
            else:
                path.lineTo(x, y)
        
        painter.drawPath(path)
    
    def set_active(self, active: bool):
        """Set visualizer active state."""
        self.is_active = active
        
        if active:
            self.waveform_color = QColor(0, 191, 255)
        else:
            self.waveform_color = QColor(0, 255, 65)
        
        self.update()