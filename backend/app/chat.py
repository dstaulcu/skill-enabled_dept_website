"""
Chat endpoint with streaming support using Ollama/OpenAI-compatible API
"""

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Optional, AsyncGenerator
import os
from openai import AsyncOpenAI
from app.auth.middleware import get_current_user

router = APIRouter(prefix="/api/chat", tags=["chat"])

# Initialize OpenAI client pointing to Ollama
client = AsyncOpenAI(
    base_url=os.getenv("OPENAI_BASE_URL", "http://localhost:11434/v1"),
    api_key=os.getenv("OPENAI_API_KEY", "ollama")
)

class Message(BaseModel):
    role: str  # "user", "assistant", "system"
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]
    stream: bool = True
    model: Optional[str] = None

async def generate_stream(messages: List[dict], model: str, user_identity: str) -> AsyncGenerator[str, None]:
    """Generate streaming chat responses"""
    try:
        # Add system message with user context
        system_message = {
            "role": "system",
            "content": f"You are a helpful AI assistant for a government department. You are currently assisting {user_identity}. Be concise and professional."
        }
        
        full_messages = [system_message] + [{"role": m.role, "content": m.content} for m in messages]
        
        stream = await client.chat.completions.create(
            model=model,
            messages=full_messages,
            stream=True,
            temperature=0.7,
            max_tokens=500
        )
        
        async for chunk in stream:
            if chunk.choices[0].delta.content:
                # Send server-sent event format
                content = chunk.choices[0].delta.content
                yield f"data: {content}\n\n"
        
        yield "data: [DONE]\n\n"
        
    except Exception as e:
        yield f"data: [ERROR] {str(e)}\n\n"

@router.post("/stream")
async def chat_stream(
    request: ChatRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Stream chat responses from Ollama
    """
    model = request.model or os.getenv("OPENAI_MODEL", "llama3:latest")
    
    return StreamingResponse(
        generate_stream(request.messages, model, current_user["identity"]),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )

@router.post("/")
async def chat_completion(
    request: ChatRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Non-streaming chat completion
    """
    model = request.model or os.getenv("OPENAI_MODEL", "llama3:latest")
    
    try:
        system_message = {
            "role": "system",
            "content": f"You are a helpful AI assistant for a government department. You are currently assisting {current_user['identity']}. Be concise and professional."
        }
        
        full_messages = [system_message] + [{"role": m.role, "content": m.content} for m in request.messages]
        
        response = await client.chat.completions.create(
            model=model,
            messages=full_messages,
            temperature=0.7,
            max_tokens=500
        )
        
        return {
            "message": {
                "role": "assistant",
                "content": response.choices[0].message.content
            },
            "model": model,
            "user": current_user["identity"]
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat error: {str(e)}")
