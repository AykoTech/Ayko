#!/usr/bin/env python3
"""Settings Panel - Complete configuration interface."""

import logging
import json
from pathlib import Path
from typing import Dict, Any
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QSlider, QComboBox, QCheckBox, QSpinBox, QDoubleSpinBox,
    QTextEdit, QGroupBox, QTabWidget, QFileDialog, QFormLayout
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QColor

logger = logging.getLogger("SettingsPanel")

MARVEL_THEME = {
    "arc_blue": "#00BFFF",
    "iron_gold": "#FFD700",
    "hud_black": "#0A0E27",
    "hud_panel": "#1A1F3A",
    "success_green": "#00FF41",
}


class SettingsPanel(QWidget):
    """Complete settings panel with Marvel-style design."""
    
    settings_changed = pyqtSignal(dict)
    settings_reset = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.current_settings = {}
        self.config_path = Path(__file__).parent.parent.parent / "config" / "settings.json"
        
        self._init_ui()
        self._load_settings()
        
        logger.info("✓ SettingsPanel initialized")
    
    def _init_ui(self):
        """Initialize settings UI with tabs."""
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet(f"""
            QTabWidget::pane {{
                background: {MARVEL_THEME["hud_panel"]};
                border: 2px solid {MARVEL_THEME["arc_blue"]};
                border-radius: 5px;
            }}
            QTabBar::tab {{
                background: {MARVEL_THEME["hud_black"]};
                color: {MARVEL_THEME["text_primary"]};
                padding: 10px 20px;
                border: 1px solid {MARVEL_THEME["arc_blue"]};
                border-bottom: none;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
            }}
            QTabBar::tab:selected {{
                background: {MARVEL_THEME["arc_blue"]};
                color: white;
            }}
        """)
        
        self.tabs.addTab(self._create_voice_tab(), "🎤 Voice")
        self.tabs.addTab(self._create_ai_tab(), "🧠 AI Settings")
        self.tabs.addTab(self._create_ui_tab(), "🎨 UI Theme")
        self.tabs.addTab(self._create_privacy_tab(), "🔒 Privacy")
        self.tabs.addTab(self._create_advanced_tab(), "⚙ Advanced")
        
        layout.addWidget(self.tabs)
        
        button_layout = QHBoxLayout()
        
        save_btn = QPushButton("💾 Save Settings")
        save_btn.setStyleSheet(self._get_marvel_button_style())
        save_btn.clicked.connect(self._save_settings)
        button_layout.addWidget(save_btn)
        
        reset_btn = QPushButton("🔄 Reset to Default")
        reset_btn.setStyleSheet(self._get_secondary_button_style())
        reset_btn.clicked.connect(self._reset_settings)
        button_layout.addWidget(reset_btn)
        
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def _create_voice_tab(self) -> QWidget:
        """Create voice settings tab."""
        widget = QWidget()
        layout = QVBoxLayout()
        
        engine_group = QGroupBox("Voice Engine")
        engine_group.setStyleSheet(self._get_group_style())
        engine_layout = QFormLayout()
        
        self.engine_combo = QComboBox()
        self.engine_combo.addItems(["pyttsx3", "espeak", "sapi5"])
        self.engine_combo.setStyleSheet(self._get_combo_style())
        engine_layout.addRow("Engine:", self.engine_combo)
        
        self.rate_spin = QSpinBox()
        self.rate_spin.setRange(50, 300)
        self.rate_spin.setValue(150)
        self.rate_spin.setStyleSheet(self._get_spin_style())
        engine_layout.addRow("Speech Rate:", self.rate_spin)
        
        self.volume_spin = QSpinBox()
        self.volume_spin.setRange(0, 100)
        self.volume_spin.setValue(90)
        self.volume_spin.setStyleSheet(self._get_spin_style())
        engine_layout.addRow("Volume:", self.volume_spin)
        
        engine_group.setLayout(engine_layout)
        layout.addWidget(engine_group)
        
        recognition_group = QGroupBox("Voice Recognition")
        recognition_group.setStyleSheet(self._get_group_style())
        recognition_layout = QFormLayout()
        
        self.wake_word_edit = QTextEdit()
        self.wake_word_edit.setMaximumHeight(60)
        self.wake_word_edit.setPlainText("AYKO")
        self.wake_word_edit.setStyleSheet(self._get_text_style())
        recognition_layout.addRow("Wake Word:", self.wake_word_edit)
        
        self.sensitivity_spin = QDoubleSpinBox()
        self.sensitivity_spin.setRange(0.1, 1.0)
        self.sensitivity_spin.setSingleStep(0.1)
        self.sensitivity_spin.setValue(0.5)
        self.sensitivity_spin.setStyleSheet(self._get_spin_style())
        recognition_layout.addRow("Sensitivity:", self.sensitivity_spin)
        
        recognition_group.setLayout(recognition_layout)
        layout.addWidget(recognition_group)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def _create_ai_tab(self) -> QWidget:
        """Create AI settings tab."""
        widget = QWidget()
        layout = QVBoxLayout()
        
        llm_group = QGroupBox("Language Model")
        llm_group.setStyleSheet(self._get_group_style())
        llm_layout = QFormLayout()
        
        self.model_combo = QComboBox()
        self.model_combo.addItems(["tinyllama", "llama2", "mistral", "gpt-3.5-turbo"])
        self.model_combo.setStyleSheet(self._get_combo_style())
        llm_layout.addRow("Model:", self.model_combo)
        
        self.host_edit = QTextEdit()
        self.host_edit.setMaximumHeight(60)
        self.host_edit.setPlainText("http://localhost:11434")
        self.host_edit.setStyleSheet(self._get_text_style())
        llm_layout.addRow("Ollama Host:", self.host_edit)
        
        llm_group.setLayout(llm_layout)
        layout.addWidget(llm_group)
        
        features_group = QGroupBox("AI Features")
        features_group.setStyleSheet(self._get_group_style())
        features_layout = QVBoxLayout()
        
        self.learning_check = QCheckBox("Enable Learning")
        self.learning_check.setChecked(True)
        self.learning_check.setStyleSheet(self._get_checkbox_style())
        features_layout.addWidget(self.learning_check)
        
        self.personality_check = QCheckBox("Enable Personality")
        self.personality_check.setChecked(True)
        self.personality_check.setStyleSheet(self._get_checkbox_style())
        features_layout.addWidget(self.personality_check)
        
        features_group.setLayout(features_layout)
        layout.addWidget(features_group)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def _create_ui_tab(self) -> QWidget:
        """Create UI theme tab."""
        widget = QWidget()
        layout = QVBoxLayout()
        
        theme_group = QGroupBox("UI Theme")
        theme_group.setStyleSheet(self._get_group_style())
        theme_layout = QFormLayout()
        
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Marvel Cinematic", "Matrix", "Cyberpunk", "Minimal", "Custom"])
        self.theme_combo.setStyleSheet(self._get_combo_style())
        theme_layout.addRow("Theme:", self.theme_combo)
        
        self.animation_speed_spin = QDoubleSpinBox()
        self.animation_speed_spin.setRange(0.1, 3.0)
        self.animation_speed_spin.setSingleStep(0.1)
        self.animation_speed_spin.setValue(1.0)
        self.animation_speed_spin.setStyleSheet(self._get_spin_style())
        theme_layout.addRow("Animation Speed:", self.animation_speed_spin)
        
        theme_group.setLayout(theme_layout)
        layout.addWidget(theme_group)
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def _create_privacy_tab(self) -> QWidget:
        """Create privacy settings tab."""
        widget = QWidget()
        layout = QVBoxLayout()
        
        privacy_group = QGroupBox("Privacy & Security")
        privacy_group.setStyleSheet(self._get_group_style())
        privacy_layout = QVBoxLayout()
        
        self.offline_check = QCheckBox("Offline Mode (No Cloud)")
        self.offline_check.setChecked(True)
        self.offline_check.setStyleSheet(self._get_checkbox_style())
        privacy_layout.addWidget(self.offline_check)
        
        self.store_commands_check = QCheckBox("Store Command History")
        self.store_commands_check.setChecked(True)
        self.store_commands_check.setStyleSheet(self._get_checkbox_style())
        privacy_layout.addWidget(self.store_commands_check)
        
        privacy_group.setLayout(privacy_layout)
        layout.addWidget(privacy_group)
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def _create_advanced_tab(self) -> QWidget:
        """Create advanced settings tab."""
        widget = QWidget()
        layout = QVBoxLayout()
        
        hotkey_group = QGroupBox("Hotkeys")
        hotkey_group.setStyleSheet(self._get_group_style())
        hotkey_layout = QFormLayout()
        
        self.activate_hotkey = QTextEdit()
        self.activate_hotkey.setMaximumHeight(40)
        self.activate_hotkey.setPlainText("Alt+J")
        self.activate_hotkey.setStyleSheet(self._get_text_style())
        hotkey_layout.addRow("Activate:", self.activate_hotkey)
        
        hotkey_group.setLayout(hotkey_layout)
        layout.addWidget(hotkey_group)
        
        debug_group = QGroupBox("Debug Options")
        debug_group.setStyleSheet(self._get_group_style())
        debug_layout = QVBoxLayout()
        
        self.debug_check = QCheckBox("Enable Debug Mode")
        self.debug_check.setChecked(False)
        self.debug_check.setStyleSheet(self._get_checkbox_style())
        debug_layout.addWidget(self.debug_check)
        
        debug_group.setLayout(debug_layout)
        layout.addWidget(debug_group)
        
        layout.addStretch()
        widget.setLayout(layout)
        return widget
    
    def _get_group_style(self) -> str:
        return f"""
            QGroupBox {{
                color: {MARVEL_THEME["arc_blue"]};
                font-weight: bold;
                border: 2px solid {MARVEL_THEME["arc_blue"]};
                border-radius: 5px;
                margin-top: 10px;
                padding: 10px;
            }}
        """
    
    def _get_combo_style(self) -> str:
        return f"""
            QComboBox {{
                background: {MARVEL_THEME["hud_black"]};
                color: #E0E0E0;
                border: 1px solid {MARVEL_THEME["arc_blue"]};
                border-radius: 3px;
                padding: 5px;
            }}
        """
    
    def _get_spin_style(self) -> str:
        return f"""
            QSpinBox, QDoubleSpinBox {{
                background: {MARVEL_THEME["hud_black"]};
                color: #E0E0E0;
                border: 1px solid {MARVEL_THEME["arc_blue"]};
                border-radius: 3px;
                padding: 5px;
            }}
        """
    
    def _get_text_style(self) -> str:
        return f"""
            QTextEdit {{
                background: {MARVEL_THEME["hud_black"]};
                color: #E0E0E0;
                border: 1px solid {MARVEL_THEME["arc_blue"]};
                border-radius: 3px;
                padding: 5px;
            }}
        """
    
    def _get_checkbox_style(self) -> str:
        return f"""
            QCheckBox {{
                color: #E0E0E0;
                spacing: 5px;
            }}
        """
    
    def _get_marvel_button_style(self) -> str:
        return f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {MARVEL_THEME["arc_blue"]}, 
                    stop:1 {MARVEL_THEME["arc_blue"]});
                color: white;
                border: 2px solid {MARVEL_THEME["arc_blue"]};
                border-radius: 8px;
                padding: 10px 20px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {MARVEL_THEME["iron_gold"]}, 
                    stop:1 {MARVEL_THEME["iron_gold"]});
                border: 2px solid {MARVEL_THEME["iron_gold"]};
            }}
        """
    
    def _get_secondary_button_style(self) -> str:
        return f"""
            QPushButton {{
                background: {MARVEL_THEME["hud_black"]};
                color: #E0E0E0;
                border: 2px solid {MARVEL_THEME["arc_blue"]};
                border-radius: 8px;
                padding: 10px 20px;
                font-weight: bold;
            }}
        """
    
    def _load_settings(self):
        """Load settings from configuration file."""
        try:
            if self.config_path.exists():
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    self.current_settings = json.load(f)
                self._apply_settings_to_ui()
                logger.info("✓ Settings loaded from file")
            else:
                logger.warning("Settings file not found, using defaults")
                self._use_default_settings()
        except Exception as e:
            logger.error(f"Failed to load settings: {e}")
            self._use_default_settings()
    
    def _apply_settings_to_ui(self):
        """Apply loaded settings to UI elements."""
        settings = self.current_settings
        
        if "voice" in settings:
            voice = settings["voice"]
            self.engine_combo.setCurrentText(voice.get("engine", "pyttsx3"))
            self.rate_spin.setValue(int(voice.get("rate", 1.0) * 150))
            self.volume_spin.setValue(int(voice.get("volume", 0.9) * 100))
        
        if "ai" in settings:
            ai = settings["ai"]
            self.model_combo.setCurrentText(ai.get("model", "tinyllama"))
            self.host_edit.setPlainText(ai.get("host", "http://localhost:11434"))
        
        if "ui" in settings:
            ui = settings["ui"]
            self.theme_combo.setCurrentText(ui.get("theme", "Marvel Cinematic"))
            self.animation_speed_spin.setValue(ui.get("animation_speed", 1.0))
    
    def _use_default_settings(self):
        """Use default settings when file not available."""
        self.current_settings = {
            "voice": {
                "engine": "pyttsx3",
                "rate": 1.0,
                "volume": 0.9
            },
            "ai": {
                "model": "tinyllama",
                "host": "http://localhost:11434"
            },
            "ui": {
                "theme": "Marvel Cinematic",
                "animation_speed": 1.0
            }
        }
        self._apply_settings_to_ui()
    
    def _save_settings(self):
        """Save current settings to configuration file."""
        try:
            settings = {
                "voice": {
                    "engine": self.engine_combo.currentText(),
                    "rate": self.rate_spin.value() / 150.0,
                    "volume": self.volume_spin.value() / 100.0
                },
                "ai": {
                    "model": self.model_combo.currentText(),
                    "host": self.host_edit.toPlainText()
                },
                "ui": {
                    "theme": self.theme_combo.currentText(),
                    "animation_speed": self.animation_speed_spin.value()
                }
            }
            
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=2)
            
            self.current_settings = settings
            self.settings_changed.emit(settings)
            
            logger.info("✓ Settings saved successfully")
            
        except Exception as e:
            logger.error(f"Failed to save settings: {e}")
    
    def _reset_settings(self):
        """Reset settings to defaults."""
        self._use_default_settings()
        self.settings_reset.emit()
        logger.info("✓ Settings reset to defaults")
    
    def get_current_settings(self) -> dict:
        """Get current settings as dictionary."""
        return self.current_settings.copy()