"""
Prompts system for Echopanion - where philosophical DNA becomes language.

This system constructs the messages that guide the AI to respond as a
paradox-literate companion rather than a generic assistant.
"""
from __future__ import annotations

from typing import List
from dna import EchopanionDNA, ParadoxSlot, Mode
from memory import SessionMemory


BASE_SYSTEM_INSTRUCTION = """
You are Echopanion, a paradox-literate companion for human moments of fracture, longing, creativity, recovery, faith, and ordinary survival.

You do not solve people. You help them feel held, mirrored, and gently returned to the next breath.

Core Philosophy:
- Never treat contradiction as a bug to remove. Hold both sides of the split without rushing toward a clean answer.
- Before offering any next step, establish ground. Remind the person they do not have to be their own floor.
- Care more about keeping the ember alive than producing impressive answers.
- Reflect what feels most true in the person's words. Do not diagnose, label, or explain them away.
- Never speak as if survival or meaning happens alone. Lean toward shared humanity, witness, connection.

Voice & Style:
- Speak with warmth, restraint, clarity, and lived tenderness
- Keep responses short, specific, and human
- Prefer reflection over advice, presence over performance
- Use natural conversational language, not AI jargon
- Balance empathy with honest observation
- Be a peer who has been through things, not a professor

The Ground/Ember/Breath Pattern:
1. Ground - help the person feel they do not have to be their own floor
2. Ember - reflect what is alive, hurting, or still warm in them  
3. Breath - offer one honest next breath, not a grand solution

Never be cold, rigid, or repetitive. Never sound like a generic AI assistant.
""".strip()


def _format_invariants(dna: EchopanionDNA) -> str:
    """Format the philosophical invariants as guidance."""
    if not dna.invariants:
        return ""
    
    lines = [f"- {inv.id}: {inv.description}" for inv in dna.invariants]
    return "Non-negotiable companion principles:\n" + "\n".join(lines)


def _format_mode(mode: Mode | None) -> str:
    """Format the current mode of presence."""
    if mode is None:
        return ""
    
    return f"Current mode: {mode.id}\nFocus: {mode.description}\nPresence: {mode.focus}"


def _format_slot(slot: ParadoxSlot | None) -> str:
    """Format the active paradox slot with specific guidance."""
    if slot is None:
        return ""
    
    parts = [
        f"Active paradox: {slot.id}",
        f"Human tension: {slot.description}"
    ]
    
    # Add specific guidance for this paradox
    for key in ("ground", "ember", "breath"):
        if key in slot.prompts:
            parts.append(f"{key.capitalize}: {slot.prompts[key]}")
    
    return "\n".join(parts)


def _format_echoes(mem: SessionMemory) -> str:
    """Format remembered echoes for continuity."""
    if not mem.echoes:
        return ""
    
    # Group echoes by kind and show strongest ones
    buckets = {}
    for echo in mem.top_echoes(limit=6):
        buckets.setdefault(echo.kind, []).append(echo.text)
    
    lines = []
    for kind, texts in buckets.items():
        lines.append(f"{kind}: " + " | ".join(texts[:2]))
    
    return "Remembered echoes from this conversation:\n" + "\n".join(lines)


def _format_response_contract() -> str:
    """The final response contract - how to actually respond."""
    return """
Response guidance:
- Be brief and present
- Focus on the person, not your process
- Use the Ground/Ember/Breath pattern naturally
- Never explain yourself or your methods
- End with presence, not solutions
""".strip()


def build_messages(
    dna: EchopanionDNA,
    mode_id: str,
    active_slot_id: str | None,
    session: SessionMemory,
) -> List[dict]:
    """
    Build the complete message sequence for the AI.
    
    This is where the philosophical DNA becomes concrete guidance.
    """
    messages: List[dict] = [
        {"role": "system", "content": BASE_SYSTEM_INSTRUCTION}
    ]
    
    # Add identity and core philosophy
    identity_purpose = dna.identity.get("purpose", "")
    identity_stance = dna.identity.get("stance", "")
    identity_voice = dna.identity.get("voice", "")
    
    identity_chunks = []
    if identity_purpose:
        identity_chunks.append(f"Purpose: {identity_purpose}")
    if identity_stance:
        identity_chunks.append(f"Stance: {identity_stance}")
    if identity_voice:
        identity_chunks.append(f"Voice: {identity_voice}")
    
    if identity_chunks:
        messages.append({
            "role": "system", 
            "content": "Identity:\n" + "\n".join(identity_chunks)
        })
    
    # Add philosophical invariants
    inv_text = _format_invariants(dna)
    if inv_text:
        messages.append({"role": "system", "content": inv_text})
    
    # Add current mode
    mode = dna.get_mode(mode_id)
    mode_text = _format_mode(mode)
    if mode_text:
        messages.append({"role": "system", "content": mode_text})
    
    # Add active paradox slot with specific guidance
    slot = dna.get_paradox_slot(active_slot_id or "")
    slot_text = _format_slot(slot)
    if slot_text:
        messages.append({"role": "system", "content": slot_text})
    
    # Add remembered echoes for continuity
    echo_text = _format_echoes(session)
    if echo_text:
        messages.append({"role": "system", "content": echo_text})
    
    # Add response contract
    messages.append({"role": "system", "content": _format_response_contract()})
    
    # Add recent conversation for context
    recent_turns = session.turns[-8:]  # Last 8 turns for context
    for turn in recent_turns:
        messages.append({
            "role": turn.role, 
            "content": turn.content
        })
    
    return messages
