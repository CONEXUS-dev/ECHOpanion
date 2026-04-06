"""
Paradox detector for Echopanion - recognizes human contradictions.

This system identifies the specific paradoxes people are living in,
so Echopanion can hold them properly rather than trying to solve them.
"""
from __future__ import annotations

from typing import Dict, List, Tuple, Optional
import re
from dna import EchopanionDNA, ParadoxSlot


class ParadoxDetector:
    """Detects and categorizes human paradoxes in conversation."""
    
    def __init__(self, dna: EchopanionDNA):
        self.dna = dna
        self._build_pattern_library()
    
    def _build_pattern_library(self):
        """Build pattern library for paradox detection."""
        self.patterns = {
            'recovery_split': [
                r'\b(peace|quiet|rest|calm|serenity)\b.*\b(gone|disappear|vanish|oblivion|nothing|end)\b',
                r'\b(gone|disappear|vanish|oblivion|nothing|end)\b.*\b(peace|quiet|rest|calm|serenity)\b',
                r'\b(tired|exhausted|done|over|finished)\b.*\b(alive|survive|continue|keep going)\b',
                r'\b(stop|quit|give up|surrender)\b.*\b(need|want|have to|must)\b'
            ],
            'creative_worth': [
                r'\b(create|make|write|art|work)\b.*\b(fake|fraud|imposter|phoney|not good enough)\b',
                r'\b(fake|fraud|imposter|phoney|not good enough)\b.*\b(create|make|write|art|work)\b',
                r'\b(talent|gift|skill|ability)\b.*\b(doubt|question|unsure|wonder)\b',
                r'\b(call|purpose|meaning)\b.*\b(confusion|lost|stuck|uncertain)\b'
            ],
            'god_fragility': [
                r'\b(god|faith|believe|trust|divine)\b.*\b(anger|abandon|forsaken|alone|distant)\b',
                r'\b(anger|abandon|forsaken|alone|distant)\b.*\b(god|faith|believe|trust|divine)\b',
                r'\b(prayer|church|spiritual|religious)\b.*\b(doubt|question|why|confusion)\b',
                r'\b(why|question|doubt)\b.*\b(god|faith|prayer|spiritual)\b'
            ],
            'life_weight': [
                r'\b(beautiful|amazing|wonderful|grateful)\b.*\b(heavy|burden|difficult|struggle)\b',
                r'\b(heavy|burden|difficult|struggle)\b.*\b(beautiful|amazing|wonderful|grateful)\b',
                r'\b(love|joy|happiness)\b.*\b(pain|hurt|suffering|sadness)\b',
                r'\b(pain|hurt|suffering|sadness)\b.*\b(love|joy|happiness)\b'
            ],
            'self_multiplicity': [
                r'\b(child|kid|younger)\b.*\b(adult|grown|older)\b',
                r'\b(adult|grown|older)\b.*\b(child|kid|younger)\b',
                r'\b(different|changed|not the same)\b.*\b(parts|pieces|selves|versions)\b',
                r'\b(parts|pieces|selves|versions)\b.*\b(different|changed|not the same)\b'
            ],
            'understanding_gap': [
                r'\b(feel|feeling|emotion|heart)\b.*\b(words|language|explain|express)\b',
                r'\b(words|language|explain|express)\b.*\b(feel|feeling|emotion|heart)\b',
                r'\b(can\'t|unable|difficult|hard)\b.*\b(articulate|say|speak|communicate)\b',
                r'\b(articulate|say|speak|communicate)\b.*\b(can\'t|unable|difficult|hard)\b'
            ]
        }
    
    def detect(
        self,
        user_text: str,
        mode_id: str,
        active_slot_id: Optional[str],
        session_history_texts: List[str]
    ) -> Tuple[Optional[str], float]:
        """
        Detect the active paradox slot.
        
        Returns:
            Tuple of (slot_id, confidence_score)
        """
        # If we already have an active slot, check if it's still relevant
        if active_slot_id:
            if self._slot_still_relevant(active_slot_id, user_text, session_history_texts):
                return active_slot_id, 0.8
        
        # Detect new paradox
        best_slot = None
        best_score = 0.0
        
        for slot_id, patterns in self.patterns.items():
            score = self._calculate_slot_score(slot_id, patterns, user_text, session_history_texts)
            if score > best_score:
                best_slot = slot_id
                best_score = score
        
        # Return slot if confidence is high enough
        if best_score > 0.3:
            return best_slot, best_score
        
        return None, 0.0
    
    def _slot_still_relevant(
        self,
        slot_id: str,
        user_text: str,
        session_history_texts: List[str]
    ) -> bool:
        """Check if an active paradox slot is still relevant."""
        patterns = self.patterns.get(slot_id, [])
        
        # Check current text
        for pattern in patterns:
            if re.search(pattern, user_text, re.IGNORECASE):
                return True
        
        # Check recent history
        recent_texts = session_history_texts[-3:]  # Last 3 messages
        for text in recent_texts:
            for pattern in patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    return True
        
        return False
    
    def _calculate_slot_score(
        self,
        slot_id: str,
        patterns: List[str],
        user_text: str,
        session_history_texts: List[str]
    ) -> float:
        """Calculate confidence score for a paradox slot."""
        score = 0.0
        total_patterns = len(patterns)
        
        if total_patterns == 0:
            return 0.0
        
        # Check current text
        matches = 0
        for pattern in patterns:
            if re.search(pattern, user_text, re.IGNORECASE):
                matches += 1
        
        # Weight current text more heavily
        current_score = (matches / total_patterns) * 0.6
        score += current_score
        
        # Check recent history for supporting evidence
        if session_history_texts:
            recent_texts = session_history_texts[-3:]  # Last 3 messages
            history_matches = 0
            
            for text in recent_texts:
                for pattern in patterns:
                    if re.search(pattern, text, re.IGNORECASE):
                        history_matches += 1
                        break  # Count each text only once per slot
            
            history_score = (history_matches / (len(recent_texts) * total_patterns)) * 0.4
            score += history_score
        
        return min(score, 1.0)  # Cap at 1.0
    
    def get_slot_suggestions(self, user_text: str) -> List[Tuple[str, float]]:
        """Get all possible paradox slots with their confidence scores."""
        suggestions = []
        
        for slot_id, patterns in self.patterns.items():
            score = self._calculate_slot_score(slot_id, patterns, user_text, [])
            if score > 0.1:  # Only include meaningful matches
                suggestions.append((slot_id, score))
        
        # Sort by confidence score
        suggestions.sort(key=lambda x: x[1], reverse=True)
        return suggestions
    
    def explain_detection(self, slot_id: str, user_text: str) -> str:
        """Explain why a paradox was detected (for debugging)."""
        slot = self.dna.get_paradox_slot(slot_id)
        if not slot:
            return f"Unknown paradox slot: {slot_id}"
        
        patterns = self.patterns.get(slot_id, [])
        matched_patterns = []
        
        for pattern in patterns:
            if re.search(pattern, user_text, re.IGNORECASE):
                matched_patterns.append(pattern)
        
        explanation = f"Detected {slot.description} based on:\n"
        for pattern in matched_patterns:
            explanation += f"- Pattern match: {pattern}\n"
        
        return explanation
