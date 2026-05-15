
import pyttsx3
import logging
import threading
import platform

logger = logging.getLogger("TTSEngine")

class TTSEngine:
    """Text-to-Speech with cross-platform support"""
    
    def __init__(self, rate: int = 150, volume: float = 0.7, language: str = "it"):
        self.engine = pyttsx3.init()
        self.rate = rate
        self.volume = max(0.0, min(1.0, volume))
        self.language = language
        self.is_speaking = False
        
        # Configure engine
        self.engine.setProperty('rate', self.rate)
        self.engine.setProperty('volume', self.volume)
        
        # Set voice language
        self._set_language()
        
        logger.info(f"✓ TTS initialized. Rate: {rate}, Volume: {volume}")
    
    def _set_language(self):
        """Set voice language based on OS and availability"""
        try:
            voices = self.engine.getProperty('voices')
            system = platform.system()
            
            # Language mapping
            lang_prefixes = {
                "it": ["italian", "it-IT", "it"],
                "en": ["english", "en-US", "en"],
            }
            
            target_lang = lang_prefixes.get(self.language[:2], [])
            
            for voice in voices:
                voice_lang = voice.languages[0] if voice.languages else ""
                if any(prefix.lower() in voice_lang.lower() for prefix in target_lang):
                    self.engine.setProperty('voice', voice.id)
                    logger.info(f"Voice set to: {voice.name}")
                    return
        except Exception as e:
            logger.warning(f"Language setting failed: {e}")
    
    def speak(self, text: str, wait: bool = True):
        """Speak text asynchronously"""
        if not text or not text.strip():
            return
        
        def _speak_thread():
            try:
                self.is_speaking = True
                self.engine.say(text)
                self.engine.runAndWait()
                self.is_speaking = False
                logger.debug(f"Spoke: {text[:50]}")
            except Exception as e:
                logger.error(f"TTS error: {e}")
                self.is_speaking = False
        
        if wait:
            _speak_thread()
        else:
            thread = threading.Thread(target=_speak_thread, daemon=True)
            thread.start()
    
    def set_rate(self, rate: int):
        """Change speech rate (50-300)"""
        self.rate = max(50, min(300, rate))
        self.engine.setProperty('rate', self.rate)
    
    def set_volume(self, volume: float):
        """Change volume (0.0-1.0)"""
        self.volume = max(0.0, min(1.0, volume))
        self.engine.setProperty('volume', self.volume)
    
    def cleanup(self):
        """Cleanup engine"""
        try:
            self.engine.stop()
        except:
            pass
