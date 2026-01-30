"""Autonomous agent API endpoints."""
from fastapi import APIRouter, BackgroundTasks
from typing import List
from opera.backend.services.autonomous_agent import get_agent, AutonomousMessage, Thought

router = APIRouter(prefix="/agent", tags=["autonomous"])


@router.post("/start")
async def start_agent(background_tasks: BackgroundTasks):
    """
    Start Opera's autonomous consciousness.
    
    Opera will begin thinking continuously in the background.
    """
    agent = get_agent()
    
    if not agent.is_active:
        background_tasks.add_task(agent.start_consciousness)
        return {
            "status": "started",
            "message": "Opera's consciousness is now active. I'm thinking independently!"
        }
    else:
        return {
            "status": "already_active",
            "message": "I'm already thinking!"
        }


@router.post("/stop")
async def stop_agent():
    """Stop Opera's autonomous consciousness."""
    agent = get_agent()
    agent.stop_consciousness()
    
    return {
        "status": "stopped",
        "message": "Opera's consciousness paused."
    }


@router.get("/messages", response_model=List[dict])
async def get_messages():
    """
    Get unsolicited messages from Opera.
    
    These are things Opera wants to tell you without being asked.
    """
    agent = get_agent()
    messages = agent.get_unread_messages()
    return messages


@router.post("/messages/read")
async def mark_messages_read():
    """Mark all autonomous messages as read."""
    agent = get_agent()
    agent.mark_messages_read()
    return {"status": "messages_marked_read"}


@router.get("/thoughts", response_model=List[dict])
async def get_thoughts(limit: int = 10):
    """
    See what Opera is thinking about right now.
    
    Peek into Opera's mind - see its current thoughts and observations.
    """
    agent = get_agent()
    thoughts = agent.get_current_thoughts(limit=limit)
    return thoughts


@router.get("/status")
async def get_status():
    """Check if Opera's consciousness is active."""
    agent = get_agent()
    return {
        "is_active": agent.is_active,
        "total_thoughts": len(agent.thoughts),
        "unread_messages": len(agent.get_unread_messages()),
        "personality": agent.personality
    }
