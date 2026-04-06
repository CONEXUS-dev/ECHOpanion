"""
LLM Client interface for Echopanion.

Abstract interface for different language model backends.
Currently implemented for Vertex AI Gemini with philosophical optimization.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Dict


class LLMClient(ABC):
    """Abstract interface for language model clients."""
    
    @abstractmethod
    def complete(self, messages: List[Dict[str, str]]) -> str:
        """
        Generate a response based on conversation messages.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            
        Returns:
            Generated response text
        """
        pass
