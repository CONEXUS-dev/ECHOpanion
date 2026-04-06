"""
Echopanion - A paradox-literate companion for human moments of fracture and beauty.

The entire philosophical foundation is encoded as invisible architecture.
Users feel held without knowing the theology behind it.
"""
from __future__ import annotations

from contextlib import asynccontextmanager
from typing import Dict, Any
import uuid
import os

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from vertex_gemini_client import VertexAIGeminiLLMClient
from runtime import EchopanionRuntime
from dna import EchopanionDNA
from memory import MemoryStore


class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None
    mode: str = "universal"


class ChatResponse(BaseModel):
    reply: str
    session_id: str


class HealthResponse(BaseModel):
    status: str
    service: str


# Global runtime instance
runtime: EchopanionRuntime | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize Echopanion with philosophical DNA and paradox-literacy."""
    global runtime
    
    # Load the philosophical DNA - the invisible architecture
    dna = EchopanionDNA.from_yaml("echopanion_dna.yaml")
    
    # Initialize with the best Gemini model for philosophical depth
    llm = VertexAIGeminiLLMClient(
        model="gemini-2.5-pro",
        temperature=0.75,
        project="echopanion",
        location="us-east1"
    )
    
    # Create memory store for session continuity
    store = MemoryStore()
    
    # Initialize runtime with universal paradox-literacy mode
    runtime = EchopanionRuntime(
        dna=dna,
        llm=llm,
        mode_id="universal",
        store=store
    )
    
    print("Echopanion awakened - paradox-literate companion ready")
    yield
    
    # Graceful shutdown
    runtime = None
    print("Echopanion resting")


# Create FastAPI application
app = FastAPI(
    title="Echopanion",
    description="A paradox-literate companion for human moments of fracture and beauty",
    version="1.0.0",
    lifespan=lifespan
)


@app.get("/", response_class=HTMLResponse)
async def sanctuary():
    """The sanctuary - where paradox is held beautifully."""
    return """
<!DOCTYPE html>
<html>
<head>
    <title>Echopanion Sanctuary</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Georgia', serif;
            background: #0a0a0a;
            color: #e0e0e0;
            height: 100vh;
            display: flex;
            flex-direction: column;
        }
        
        .sanctuary {
            flex: 1;
            display: flex;
            flex-direction: column;
            max-width: 600px;
            margin: 0 auto;
            padding: 2rem;
        }
        
        .header {
            text-align: center;
            margin-bottom: 3rem;
        }
        
        .title {
            font-size: 1.5rem;
            font-weight: 300;
            margin-bottom: 0.5rem;
            opacity: 0.9;
        }
        
        .subtitle {
            font-size: 0.9rem;
            opacity: 0.6;
            font-style: italic;
        }
        
        .chat-container {
            flex: 1;
            display: flex;
            flex-direction: column;
            background: #111;
            border-radius: 8px;
            overflow: hidden;
        }
        
        .messages {
            flex: 1;
            padding: 1.5rem;
            overflow-y: auto;
            min-height: 300px;
        }
        
        .message {
            margin-bottom: 1.5rem;
            opacity: 0;
            animation: fadeIn 0.5s forwards;
        }
        
        @keyframes fadeIn {
            to { opacity: 1; }
        }
        
        .user {
            text-align: right;
        }
        
        .user .content {
            background: #1a1a1a;
            padding: 0.8rem 1.2rem;
            border-radius: 12px;
            display: inline-block;
            max-width: 80%;
        }
        
        .echopanion .content {
            background: #0f0f0f;
            border-left: 2px solid #333;
            padding: 0.8rem 1.2rem;
            border-radius: 0 8px 8px 0;
            max-width: 80%;
        }
        
        .input-container {
            padding: 1rem;
            background: #0a0a0a;
            border-top: 1px solid #222;
        }
        
        .input-wrapper {
            display: flex;
            gap: 0.5rem;
        }
        
        #messageInput {
            flex: 1;
            background: #111;
            border: 1px solid #333;
            color: #e0e0e0;
            padding: 0.8rem;
            border-radius: 4px;
            font-family: 'Georgia', serif;
            font-size: 1rem;
        }
        
        #messageInput:focus {
            outline: none;
            border-color: #444;
        }
        
        #sendButton {
            background: #1a1a1a;
            border: 1px solid #333;
            color: #e0e0e0;
            padding: 0.8rem 1.5rem;
            border-radius: 4px;
            cursor: pointer;
            transition: all 0.2s;
        }
        
        #sendButton:hover {
            background: #222;
            border-color: #444;
        }
        
        #sendButton:disabled {
            opacity: 0.5;
            cursor: not-allowed;
        }
        
        .typing {
            opacity: 0.6;
            font-style: italic;
        }
    </style>
</head>
<body>
    <div class="sanctuary">
        <div class="header">
            <div class="title">Echopanion</div>
            <div class="subtitle">Take a breath and speak</div>
        </div>
        
        <div class="chat-container">
            <div class="messages" id="messages">
                <div class="message echopanion">
                    <div class="content">Welcome to the Sanctuary. Take a breath and speak.</div>
                </div>
            </div>
            
            <div class="input-container">
                <div class="input-wrapper">
                    <input type="text" id="messageInput" placeholder="Speak your truth..." />
                    <button id="sendButton">Send</button>
                </div>
            </div>
        </div>
    </div>

    <script>
        let sessionId = null;
        const messagesDiv = document.getElementById('messages');
        const messageInput = document.getElementById('messageInput');
        const sendButton = document.getElementById('sendButton');

        function addMessage(content, isUser = false) {
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${isUser ? 'user' : 'echopanion'}`;
            
            const contentDiv = document.createElement('div');
            contentDiv.className = 'content';
            contentDiv.textContent = content;
            
            messageDiv.appendChild(contentDiv);
            messagesDiv.appendChild(messageDiv);
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        }

        function showTyping() {
            const typingDiv = document.createElement('div');
            typingDiv.className = 'message echopanion typing';
            typingDiv.id = 'typing';
            typingDiv.innerHTML = '<div class="content">...</div>';
            messagesDiv.appendChild(typingDiv);
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        }

        function hideTyping() {
            const typingDiv = document.getElementById('typing');
            if (typingDiv) {
                typingDiv.remove();
            }
        }

        async function sendMessage() {
            const message = messageInput.value.trim();
            if (!message) return;

            // Disable input while sending
            messageInput.disabled = true;
            sendButton.disabled = true;

            // Add user message
            addMessage(message, true);
            messageInput.value = '';

            // Show typing indicator
            showTyping();

            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        message: message,
                        session_id: sessionId,
                        mode: 'universal'
                    })
                });

                const data = await response.json();
                sessionId = data.session_id;

                hideTyping();
                addMessage(data.reply);
            } catch (error) {
                hideTyping();
                addMessage('The connection faltered. Take a breath and try again.');
            }

            // Re-enable input
            messageInput.disabled = false;
            sendButton.disabled = false;
            messageInput.focus();
        }

        // Event listeners
        sendButton.addEventListener('click', sendMessage);
        messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });

        // Focus input on load
        messageInput.focus();
    </script>
</body>
</html>
    """


@app.get("/health", response_model=HealthResponse)
async def health():
    """Health check for the sanctuary."""
    return HealthResponse(
        status="healthy",
        service="echopanion"
    )


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """The heart of Echopanion - where paradox is held."""
    if not runtime:
        raise HTTPException(status_code=503, detail="Echopanion is resting")
    
    try:
        reply = runtime.handle_user_message(request.message)
        return ChatResponse(
            reply=reply,
            session_id=runtime.session.session_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"The sanctuary faltered: {str(e)}")


@app.get("/session/{session_id}/state")
async def session_state(session_id: str):
    """Debug endpoint for session state."""
    if not runtime:
        raise HTTPException(status_code=503, detail="Echopanion is resting")
    
    if runtime.session.session_id != session_id:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return runtime.inspect_state()


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
