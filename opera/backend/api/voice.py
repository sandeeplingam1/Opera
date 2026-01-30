"""Voice API endpoints for Opera."""
from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel
from opera.backend.services.llm_client import get_llm_client
from opera.backend.config import config
from openai import OpenAI

router = APIRouter(prefix="/voice", tags=["voice"])


class SpeakRequest(BaseModel):
    text: str
    voice: str = "alloy"  # alloy, echo, fable, onyx, nova, shimmer
    speed: float = 1.0


@router.post("/speak")
async def speak(request: SpeakRequest):
    """
    Convert text to speech using OpenAI TTS.
    
    Opera speaks the provided text out loud.
    """
    if not config.OPENAI_API_KEY:
        raise HTTPException(status_code=503, detail="OpenAI API key not configured")
    
    try:
        client = OpenAI(api_key=config.OPENAI_API_KEY)
        
        response = client.audio.speech.create(
            model="tts-1",
            voice=request.voice,
            input=request.text,
            speed=request.speed
        )
        
        # Return audio as MP3
        audio_content = response.content
        
        return Response(
            content=audio_content,
            media_type="audio/mpeg",
            headers={
                "Content-Disposition": f"inline; filename=speech.mp3"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TTS failed: {str(e)}")


@router.post("/announce")
async def announce_message(text: str):
    """
    Have Opera announce a message autonomously.
    
    Opera will speak this message out loud to the user.
    This is used for proactive communication.
    """
    # Store in autonomous messages queue
    from opera.backend.services.autonomous_agent import get_agent
    
    agent = get_agent()
    from opera.backend.services.autonomous_agent import AutonomousMessage
    
    message = AutonomousMessage(
        message=text,
        trigger="voice_announcement",
        urgency="high"
    )
    agent.messages.append(message)
    
    return {"status": "announced", "text": text}
