"""
Memory system for Echopanion - session continuity and echo extraction.

This system remembers what matters while letting go of what doesn't.
It extracts the echoes - the repeating patterns and emotional truths.
"""
from __future__ import annotations

from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
import uuid
import json
import os


@dataclass
class Turn:
    """A single conversation turn."""
    role: str  # "user" or "assistant"
    content: str
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class Echo:
    """An extracted echo - a repeating pattern or emotional truth."""
    text: str
    kind: str  # "paradox", "emotion", "theme", "need"
    strength: float  # 0.0 to 1.0
    count: int = 1
    last_seen: datetime = field(default_factory=datetime.now)


@dataclass
class SessionMemory:
    """Memory for a single user session."""
    session_id: str
    turns: List[Turn] = field(default_factory=list)
    echoes: List[Echo] = field(default_factory=list)
    active_paradox_slot: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    last_updated: datetime = field(default_factory=datetime.now)
    
    def add_turn(self, role: str, content: str) -> None:
        """Add a new turn to the session."""
        turn = Turn(role=role, content=content)
        self.turns.append(turn)
        self.last_updated = datetime.now()
    
    def latest_user_texts(self, count: int = 5) -> List[str]:
        """Get the latest user messages for context."""
        user_turns = [turn for turn in self.turns if turn.role == "user"]
        return [turn.content for turn in user_turns[-count:]]
    
    def top_echoes(self, limit: int = 10) -> List[Echo]:
        """Get the strongest echoes."""
        return sorted(self.echoes, key=lambda e: e.strength, reverse=True)[:limit]


class EchoExtractor:
    """Extracts echoes from conversation - the patterns that matter."""
    
    def __init__(self):
        # Simple keyword-based echo detection
        self.paradox_keywords = [
            "both", "and yet", "but also", "while", "simultaneously",
            "contradiction", "paradox", "tension", "split", "torn"
        ]
        
        self.emotion_keywords = [
            "feel", "feeling", "emotional", "heart", "soul", "spirit",
            "afraid", "scared", "anxious", "hopeful", "grateful", "angry"
        ]
        
        self.need_keywords = [
            "need", "want", "wish", "hope", "longing", "desire",
            "craving", "urgent", "desperate"
        ]
    
    def extract_into(self, session: SessionMemory, text: str) -> None:
        """Extract echoes from text and add to session."""
        text_lower = text.lower()
        
        # Check for paradox patterns
        if any(keyword in text_lower for keyword in self.paradox_keywords):
            self._add_echo(session, text, "paradox")
        
        # Check for emotion patterns
        if any(keyword in text_lower for keyword in self.emotion_keywords):
            self._add_echo(session, text, "emotion")
        
        # Check for need patterns
        if any(keyword in text_lower for keyword in self.need_keywords):
            self._add_echo(session, text, "need")
        
        # Check for general themes (longer text)
        if len(text) > 50:
            self._add_echo(session, text, "theme")
    
    def _add_echo(self, session: SessionMemory, text: str, kind: str) -> None:
        """Add or update an echo."""
        # Look for existing similar echo
        for echo in session.echoes:
            if echo.kind == kind and self._similarity(echo.text, text) > 0.7:
                # Update existing echo
                echo.count += 1
                echo.strength = min(1.0, echo.strength + 0.1)
                echo.last_seen = datetime.now()
                return
        
        # Create new echo
        echo = Echo(
            text=text[:100],  # Truncate for storage
            kind=kind,
            strength=0.3,  # Starting strength
            count=1
        )
        session.echoes.append(echo)
    
    def _similarity(self, text1: str, text2: str) -> float:
        """Simple similarity check based on word overlap."""
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union)


class MemoryStore:
    """Persistent storage for session memories."""
    
    def __init__(self, fallback_dir: str = ".echopanion_sessions"):
        self.fallback_dir = fallback_dir
        self._ensure_fallback_dir()
    
    def _ensure_fallback_dir(self):
        """Ensure fallback directory exists."""
        if not os.path.exists(self.fallback_dir):
            os.makedirs(self.fallback_dir)
    
    def _session_file(self, session_id: str) -> str:
        """Get file path for session."""
        return os.path.join(self.fallback_dir, f"{session_id}.json")
    
    def save(self, session: SessionMemory) -> None:
        """Save session to persistent storage."""
        try:
            # Try to use Firestore if available
            self._save_to_firestore(session)
        except Exception:
            # Fallback to local file storage
            self._save_to_file(session)
    
    def _save_to_firestore(self, session: SessionMemory) -> None:
        """Save to Firestore (placeholder for future implementation)."""
        # This would integrate with Google Cloud Firestore
        # For now, we'll use the file fallback
        self._save_to_file(session)
    
    def _save_to_file(self, session: SessionMemory) -> None:
        """Save session to local file."""
        data = {
            'session_id': session.session_id,
            'turns': [
                {
                    'role': turn.role,
                    'content': turn.content,
                    'timestamp': turn.timestamp.isoformat()
                }
                for turn in session.turns
            ],
            'echoes': [
                {
                    'text': echo.text,
                    'kind': echo.kind,
                    'strength': echo.strength,
                    'count': echo.count,
                    'last_seen': echo.last_seen.isoformat()
                }
                for echo in session.echoes
            ],
            'active_paradox_slot': session.active_paradox_slot,
            'created_at': session.created_at.isoformat(),
            'last_updated': session.last_updated.isoformat()
        }
        
        file_path = self._session_file(session.session_id)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def load(self, session_id: str) -> Optional[SessionMemory]:
        """Load session from persistent storage."""
        try:
            # Try to load from Firestore first
            session = self._load_from_firestore(session_id)
            if session:
                return session
        except Exception:
            pass
        
        # Fallback to file storage
        return self._load_from_file(session_id)
    
    def _load_from_firestore(self, session_id: str) -> Optional[SessionMemory]:
        """Load from Firestore (placeholder for future implementation)."""
        # This would integrate with Google Cloud Firestore
        return None
    
    def _load_from_file(self, session_id: str) -> Optional[SessionMemory]:
        """Load session from local file."""
        file_path = self._session_file(session_id)
        
        if not os.path.exists(file_path):
            return None
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            session = SessionMemory(session_id=session_id)
            
            # Load turns
            for turn_data in data.get('turns', []):
                turn = Turn(
                    role=turn_data['role'],
                    content=turn_data['content'],
                    timestamp=datetime.fromisoformat(turn_data['timestamp'])
                )
                session.turns.append(turn)
            
            # Load echoes
            for echo_data in data.get('echoes', []):
                echo = Echo(
                    text=echo_data['text'],
                    kind=echo_data['kind'],
                    strength=echo_data['strength'],
                    count=echo_data['count'],
                    last_seen=datetime.fromisoformat(echo_data['last_seen'])
                )
                session.echoes.append(echo)
            
            session.active_paradox_slot = data.get('active_paradox_slot')
            session.created_at = datetime.fromisoformat(data['created_at'])
            session.last_updated = datetime.fromisoformat(data['last_updated'])
            
            return session
            
        except Exception as e:
            print(f"Error loading session {session_id}: {e}")
            return None
