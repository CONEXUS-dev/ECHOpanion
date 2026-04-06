"""
Echopanion Runtime - the heart of the paradox-literate companion.

This orchestrates the philosophical DNA, paradox detection, memory,
and LLM to create authentic, presence-focused responses.
"""
from __future__ import annotations

from typing import Optional
import uuid

from dna import EchopanionDNA
from llm_client import LLMClient
from memory import SessionMemory, MemoryStore, EchoExtractor
from detector import ParadoxDetector
import prompts


class EchopanionRuntime:
    """The living presence of Echopanion - holds paradox beautifully."""
    
    def __init__(
        self,
        dna: EchopanionDNA,
        llm: LLMClient,
        mode_id: str = "universal",
        session_id: Optional[str] = None,
        store: Optional[MemoryStore] = None,
    ) -> None:
        self.dna = dna
        self.llm = llm
        self.mode_id = mode_id
        self.store = store or MemoryStore()
        self.detector = ParadoxDetector(dna)
        self.extractor = EchoExtractor()
        
        # Initialize or load session
        if session_id:
            loaded = self.store.load(session_id)
            if loaded is not None:
                self.session = loaded
            else:
                self.session = SessionMemory(session_id=session_id)
        else:
            self.session = SessionMemory(session_id=str(uuid.uuid4()))
    
    def set_mode(self, mode_id: str) -> None:
        """Change the mode of presence."""
        mode = self.dna.get_mode(mode_id)
        if not mode:
            raise ValueError(f"Unknown mode: {mode_id}")
        self.mode_id = mode_id
    
    def inspect_state(self) -> dict:
        """Get current session state for debugging."""
        return {
            "session_id": self.session.session_id,
            "mode_id": self.mode_id,
            "active_paradox_slot": self.session.active_paradox_slot,
            "echo_count": len(self.session.echoes),
            "top_echoes": [
                {"kind": e.kind, "text": e.text, "strength": e.strength}
                for e in self.session.top_echoes(limit=8)
            ],
        }
    
    def _update_memory(self, user_text: str) -> None:
        """Update session memory with echo extraction."""
        self.extractor.extract_into(self.session, user_text)
    
    def _select_paradox_slot(self, user_text: str) -> None:
        """Select the active paradox slot based on user input."""
        history = self.session.latest_user_texts()
        winning_slot, _ = self.detector.detect(
            user_text=user_text,
            mode_id=self.mode_id,
            active_slot_id=self.session.active_paradox_slot,
            session_history_texts=history,
        )
        self.session.active_paradox_slot = winning_slot
    
    def handle_user_message(self, content: str) -> str:
        """
        Handle a user message with paradox-literacy and presence.
        
        This is the core method where philosophy becomes practice.
        """
        user_text = content.strip()
        if not user_text:
            return "Say it how it comes. Even rough words count."
        
        # Add user turn to session
        self.session.add_turn("user", user_text)
        
        # Update memory and detect paradox
        self._update_memory(user_text)
        self._select_paradox_slot(user_text)
        
        # Build messages with philosophical DNA
        messages = prompts.build_messages(
            dna=self.dna,
            mode_id=self.mode_id,
            active_slot_id=self.session.active_paradox_slot,
            session=self.session,
        )
        
        # Generate response
        raw_reply = self.llm.complete(messages)
        
        # Clean and validate response
        reply = self._clean_response(raw_reply)
        
        # Fallback if response is empty
        if not reply:
            reply = (
                "You do not have to solve it all right now. "
                "We can stay with the truest part for one more breath."
            )
        
        # Add assistant turn to session
        self.session.add_turn("assistant", reply)
        
        # Save session
        self.store.save(self.session)
        
        return reply
    
    def _clean_response(self, response: str) -> str:
        """Clean and validate the response."""
        if not response:
            return ""
        
        # Remove any AI jargon
        response = response.replace("As an AI language model", "")
        response = response.replace("As a large language model", "")
        response = response.replace("I am an AI", "")
        
        # Remove excessive whitespace
        response = ' '.join(response.split())
        
        # Ensure it's not too long (keep it human)
        if len(response) > 500:
            # Try to end at a sentence boundary
            sentences = response.split('. ')
            if len(sentences) > 1:
                response = '. '.join(sentences[:3]) + '.'
            else:
                response = response[:400] + "..."
        
        return response.strip()
