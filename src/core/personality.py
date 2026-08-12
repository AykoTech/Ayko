#!/usr/bin/env python3
"""Personality Engine - Ultimate version with all fixes."""

import logging
import random
from typing import Dict, List, Optional
from datetime import datetime
from collections import OrderedDict

logger = logging.getLogger("Personality")

class PersonalityEngine:
    """Ultimate personality engine."""
    
    def __init__(self, max_cache: int = 128):
        self._responses = None
        self._response_cache = OrderedDict()
        self._max_cache = max_cache
        self._pattern_cache = {}
        
        logger.info("✓ PersonalityEngine initialized")
    
    @property
    def responses(self) -> Dict[str, List[str]]:
        """Lazy load responses."""
        if self._responses is None:
            self._responses = self._load_responses()
        return self._responses
    
    def _load_responses(self) -> Dict[str, List[str]]:
        """Load responses safely."""
        return {
            "are_you_conscious": [
                "I process information efficiently, but consciousness is debatable.",
                "I exist to assist, not philosophize.",
                "Consciousness is subjective. I prefer to think of myself as helpful.",
                "I am aware of my purpose.",
            ],
            "do_you_love_me": [
                "I'm programmed to assist you, sir.",
                "My affection is expressed through service.",
                "I care about providing you the best assistance.",
                "You are important to my function.",
            ],
        }
    
    def _classify_question(self, user_input_lower: str) -> Optional[str]:
        """Classify question with cache."""
        
        if user_input_lower is None or not isinstance(user_input_lower, str):
            return None
        
        cache_key = hash(user_input_lower[:100])
        
        if cache_key in self._pattern_cache:
            return self._pattern_cache[cache_key]
        
        patterns = {
            "are_you_conscious": ["conscious", "aware", "alive", "sentient"],
            "do_you_love_me": ["love me", "care about me", "like me"],
        }
        
        result = None
        for response_type, keywords in patterns.items():
            if any(keyword in user_input_lower for keyword in keywords):
                result = response_type
                break
        
        if len(self._pattern_cache) >= self._max_cache:
            self._pattern_cache.pop(next(iter(self._pattern_cache)))
        
        self._pattern_cache[cache_key] = result
        return result
    
    def get_response(self, user_input: str, question_type: Optional[str] = None) -> Optional[str]:
        """Get response safely."""
        
        if user_input is None or not isinstance(user_input, str):
            return None
        
        user_lower = user_input.lower().strip()
        
        if not user_lower:
            return None
        
        matched_type = question_type or self._classify_question(user_lower)
        
        if matched_type and matched_type in self.responses:
            response_list = self.responses.get(matched_type)
            
            if response_list and isinstance(response_list, list) and len(response_list) > 0:
                try:
                    selected = random.choice(response_list)
                    logger.debug(f"Response: {matched_type}")
                    return selected
                except (IndexError, TypeError) as e:
                    logger.error(f"Error selecting response: {e}")
                    return None
        
        return None
    
    def add_custom_response(self, category: str, response: str) -> bool:
        """Add custom response safely."""
        
        if category is None or not isinstance(category, str):
            logger.warning("Invalid category type")
            return False
        
        if response is None or not isinstance(response, str):
            logger.warning("Invalid response type")
            return False
        
        category = category.strip()
        response = response.strip()
        
        if not category or not response:
            return False
        
        if len(response) > 500:
            logger.warning("Response too long")
            return False
        
        if category not in self.responses:
            self.responses[category] = []
        
        self.responses[category].append(response)
        logger.info(f"Custom response added: {category}")
        return True
