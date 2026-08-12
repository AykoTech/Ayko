#!/usr/bin/env python3
"""Hotkey Manager - Ultimate version with all fixes."""

import logging
import threading
from typing import Dict, Optional, Set, Tuple
from pynput import keyboard
from PyQt6.QtCore import QObject, pyqtSignal
import time

logger = logging.getLogger("HotkeyManager")

class HotkeyManager(QObject):
    """Ultimate hotkey manager."""
    
    hotkey_triggered = pyqtSignal(str)
    hotkey_activated = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.pressed_keys: Set = set()
        self.keys_lock = threading.RLock()
        self.listener = None
        self._cleanup_event = threading.Event()
        
        self.hotkeys = {
            "activate": {
                "keys": {keyboard.Key.alt, keyboard.KeyCode(char='j')},
                "description": "Activate JARVIS"
            },
            "settings": {
                "keys": {keyboard.Key.alt, keyboard.KeyCode(char='j'), keyboard.KeyCode(char='s')},
                "description": "Open Settings"
            },
            "help": {
                "keys": {keyboard.Key.alt, keyboard.KeyCode(char='j'), keyboard.KeyCode(char='h')},
                "description": "Show Help"
            },
            "clear": {
                "keys": {keyboard.Key.alt, keyboard.KeyCode(char='j'), keyboard.KeyCode(char='c')},
                "description": "Clear History"
            },
        }
        
        self._start_listener()
        logger.info("✓ HotkeyManager initialized")
    
    def _start_listener(self) -> None:
        """Start global keyboard listener."""
        try:
            self.listener = keyboard.Listener(
                on_press=self._on_key_press,
                on_release=self._on_key_release
            )
            self.listener.start()
            logger.debug("Keyboard listener started")
        except Exception as e:
            logger.error(f"Failed to start listener: {e}", exc_info=True)
    
    def _on_key_press(self, key) -> None:
        """Handle key press (no deadlock)."""
        try:
            should_trigger = False
            triggered_action = None
            
            with self.keys_lock:
                if key is None:
                    return
                
                self.pressed_keys.add(key)
                should_trigger, triggered_action = self._check_hotkeys_internal()
            
            if should_trigger and triggered_action:
                logger.debug(f"Hotkey: {triggered_action}")
                try:
                    self.hotkey_triggered.emit(triggered_action)
                    if triggered_action == "activate":
                        self.hotkey_activated.emit()
                except RuntimeError as e:
                    logger.warning(f"Signal emit error: {e}")
        
        except Exception as e:
            logger.error(f"Key press error: {e}", exc_info=True)
    
    def _on_key_release(self, key) -> None:
        """Handle key release."""
        try:
            with self.keys_lock:
                if key is not None:
                    self.pressed_keys.discard(key)
        except Exception as e:
            logger.error(f"Key release error: {e}", exc_info=True)
    
    def _check_hotkeys_internal(self) -> Tuple[bool, Optional[str]]:
        """Check hotkeys (call with lock held)."""
        
        for action, hotkey_config in self.hotkeys.items():
            if hotkey_config is None:
                continue
            
            required_keys = hotkey_config.get("keys", set())
            if not required_keys or not isinstance(required_keys, set):
                continue
            
            if self._keys_match(required_keys):
                self.pressed_keys.clear()
                return True, action
        
        return False, None
    
    def _keys_match(self, required_keys: set) -> bool:
        """Check key match safely."""
        
        try:
            pressed = set()
            
            for key in self.pressed_keys:
                if key is None:
                    continue
                
                if isinstance(key, keyboard.Key):
                    pressed.add(key)
                elif isinstance(key, keyboard.KeyCode):
                    if key.char:
                        pressed.add(keyboard.KeyCode(char=key.char.lower()))
                    else:
                        pressed.add(key)
            
            return required_keys.issubset(pressed)
        
        except Exception as e:
            logger.error(f"Key match error: {e}", exc_info=True)
            return False
    
    def cleanup(self):
        """Cleanup resources."""
        try:
            self._cleanup_event.set()
            if self.listener:
                self.listener.stop()
                self.listener = None
            
            with self.keys_lock:
                self.pressed_keys.clear()
            
            logger.info("HotkeyManager cleanup complete")
        except Exception as e:
            logger.error(f"Cleanup error: {e}", exc_info=True)
    
    def __del__(self):
        """Destructor."""
        try:
            self.cleanup()
        except:
            pass
