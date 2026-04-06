"""
Vertex AI Gemini client for Echopanion - designed for philosophical depth.

This client is optimized for holding paradox and providing authentic,
human-like responses rather than generic AI assistance.
"""
from __future__ import annotations

from typing import List, Dict
from llm_client import LLMClient

try:
    from google import genai
    from google.genai import types
except ImportError:
    genai = None
    types = None


class VertexAIGeminiLLMClient(LLMClient):
    """Vertex AI Gemini client optimized for paradox-literacy and philosophical depth."""
    
    def __init__(
        self,
        model: str = "gemini-2.5-pro",
        temperature: float = 0.75,
        project: str = "echopanion",
        location: str = "us-east1",
    ) -> None:
        if genai is None:
            raise RuntimeError(
                "The 'google-genai' package is not installed. "
                "Run `pip install google-genai>=0.3.0`."
            )
        
        # Initialize Google Gen AI client with Vertex AI and ADC
        self.client = genai.Client(
            vertexai=True,
            project=project,
            location=location
        )
        
        # Store configuration
        self.model_name = model
        self.temperature = temperature
        self.project = project
        self.location = location

    def complete(self, messages: List[Dict[str, str]]) -> str:
        """Generate response using Gemini with philosophical depth optimization."""
        print(f"🔍 Echopanion: Processing {len(messages)} messages")
        
        # Extract system instruction and build conversation
        system_instruction = None
        conversation_parts = []
        
        for msg in messages:
            role = msg["role"]
            content = msg["content"]
            
            if role == "system":
                system_instruction = content
            elif role == "user":
                conversation_parts.append(content)
            elif role == "assistant":
                conversation_parts.append(f"Echopanion: {content}")
        
        # Build the prompt for philosophical engagement
        if conversation_parts:
            prompt = "\n\n".join(conversation_parts)
        else:
            prompt = "Welcome to the Sanctuary."
        
        print(f"📝 Echopanion: System instruction present: {bool(system_instruction)}")
        print(f"📝 Echopanion: Prompt: {prompt[:100]}...")
        
        try:
            # Generate content using Google Gen AI SDK
            print(f"🚀 Echopanion: Calling model {self.model_name}")
            
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=self.temperature,
                    max_output_tokens=2048,
                    system_instruction=system_instruction,
                )
            )
            
            result = response.text.strip()
            print(f"✅ Echopanion: Response received: {result[:100]}...")
            return result
            
        except Exception as e:
            # Enhanced error handling for therapeutic continuity
            error_msg = f"Vertex AI Error: {str(e)}"
            print(f"❌ {error_msg}")
            
            # Fallback response that maintains the philosophical stance
            return "The connection shifted. Take a breath. I'm still here with you in this moment."
