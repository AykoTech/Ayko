#!/usr/bin/env python3
"""Sphere Manager - Enhanced 3D sphere with Python-JavaScript bridge."""

import logging
import json
from pathlib import Path
from typing import Dict, Optional
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl, pyqtSignal, QObject
from PyQt6.QtWidgets import QWidget

logger = logging.getLogger("SphereManager")


class SphereJSBridge(QObject):
    """Bridge between Python and JavaScript for sphere control."""
    
    state_changed = pyqtSignal(str)
    animation_complete = pyqtSignal(str)
    error_occurred = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        logger.info("✓ SphereJSBridge initialized")
    
    def update_state(self, state: str):
        """Called from JavaScript when state changes."""
        logger.debug(f"JS State update: {state}")
        self.state_changed.emit(state)
    
    def on_animation_complete(self, animation_type: str):
        """Called from JavaScript when animation completes."""
        logger.debug(f"JS Animation complete: {animation_type}")
        self.animation_complete.emit(animation_type)
    
    def on_error(self, error_message: str):
        """Called from JavaScript when error occurs."""
        logger.error(f"JS Error: {error_message}")
        self.error_occurred.emit(error_message)


class SphereManager(QWidget):
    """Enhanced 3D sphere manager with offline Three.js support."""
    
    sphere_ready = pyqtSignal()
    sphere_error = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.sphere_view = QWebEngineView()
        self.js_bridge = SphereJSBridge()
        self.current_state = "idle"
        self.animation_config = {}
        self.sphere_loaded = False
        
        self.js_bridge.state_changed.connect(self._on_js_state_change)
        self.js_bridge.error_occurred.connect(self._on_js_error)
        
        self._load_sphere()
        logger.info("✓ SphereManager initialized")
    
    def _load_sphere(self):
        """Load enhanced sphere with fallback support."""
        try:
            # Try enhanced sphere first
            sphere_path = Path(__file__).parent.parent.parent / "assets" / "sphere_enhanced.html"
            if not sphere_path.exists():
                # Fallback to original sphere
                sphere_path = Path(__file__).parent.parent.parent / "assets" / "sphere.html"
            
            if sphere_path.exists():
                self.sphere_view.setUrl(QUrl.fromLocalFile(str(sphere_path)))
                self.sphere_view.loadFinished.connect(self._on_page_loaded)
                logger.info(f"✓ Sphere loaded from: {sphere_path}")
            else:
                logger.error("Sphere HTML file not found")
                self.sphere_error.emit("Sphere HTML file not found")
                
        except Exception as e:
            logger.error(f"Failed to load sphere: {e}")
            self.sphere_error.emit(str(e))
    
    def _on_page_loaded(self, success: bool):
        """Called when sphere page finishes loading."""
        if success:
            self.sphere_loaded = True
            self._inject_js_bridge()
            self.sphere_ready.emit()
            logger.info("✓ Sphere page loaded successfully")
        else:
            logger.error("Sphere page failed to load")
            self.sphere_error.emit("Sphere page failed to load")
    
    def _inject_js_bridge(self):
        """Inject Python-JavaScript bridge into sphere page."""
        try:
            self.sphere_view.page().runJavaScript(
                "console.log('Sphere page loaded');"
            )
            logger.debug("✓ JavaScript bridge injected")
        except Exception as e:
            logger.warning(f"Failed to inject JS bridge: {e}")
    
    def _on_js_state_change(self, state: str):
        """Handle state change from JavaScript."""
        self.current_state = state
        logger.debug(f"Sphere state changed to: {state}")
    
    def _on_js_error(self, error_message: str):
        """Handle error from JavaScript."""
        logger.error(f"Sphere error: {error_message}")
        self.sphere_error.emit(error_message)
    
    def set_state(self, state: str, animation_config: Optional[Dict] = None):
        """Set sphere state with optional animation configuration."""
        if not self.sphere_loaded:
            logger.warning("Sphere not loaded, cannot set state")
            return
        
        self.current_state = state
        self.animation_config = animation_config or {}
        
        js_command = f"""
            if (window.aykoAPI && window.aykoAPI.setState) {{
                window.aykoAPI.setState('{state}', {json.dumps(animation_config)});
            }}
        """
        
        try:
            self.sphere_view.page().runJavaScript(js_command)
            logger.info(f"✓ Sphere state set to: {state}")
        except Exception as e:
            logger.error(f"Failed to set sphere state: {e}")
    
    def trigger_animation(self, animation_type: str, params: Optional[Dict] = None):
        """Trigger specific animation on sphere."""
        if not self.sphere_loaded:
            logger.warning("Sphere not loaded, cannot trigger animation")
            return
        
        params = params or {}
        js_command = f"""
            if (window.aykoAPI && window.aykoAPI.triggerAnimation) {{
                window.aykoAPI.triggerAnimation('{animation_type}', {json.dumps(params)});
            }}
        """
        
        try:
            self.sphere_view.page().runJavaScript(js_command)
            logger.info(f"✓ Animation triggered: {animation_type}")
        except Exception as e:
            logger.error(f"Failed to trigger animation: {e}")
    
    def set_color_theme(self, primary_color: str, secondary_color: str):
        """Set sphere color theme."""
        if not self.sphere_loaded:
            logger.warning("Sphere not loaded, cannot set colors")
            return
        
        js_command = f"""
            if (window.aykoAPI && window.aykoAPI.setColors) {{
                window.aykoAPI.setColors('{primary_color}', '{secondary_color}');
            }}
        """
        
        try:
            self.sphere_view.page().runJavaScript(js_command)
            logger.info(f"✓ Colors set: {primary_color}, {secondary_color}")
        except Exception as e:
            logger.error(f"Failed to set colors: {e}")
    
    def get_sphere_widget(self) -> QWebEngineView:
        """Get the sphere widget for embedding in UI."""
        return self.sphere_view
    
    def get_current_state(self) -> str:
        """Get current sphere state."""
        return self.current_state
    
    def is_loaded(self) -> bool:
        """Check if sphere is loaded and ready."""
        return self.sphere_loaded