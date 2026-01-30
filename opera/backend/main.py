"""Opera backend application entry point.

This module creates the FastAPI app and includes API routers. It also
exposes endpoints for health checks. This file can be served with
``uvicorn opera.backend.main:app --reload``.
"""

from fastapi import FastAPI

from .api import memory, reasoning, search, execution, insights, agent, voice

# Import tools to register them
from .tools import file_tools, memory_tools, web_tools  # noqa


app = FastAPI(title="Opera Backend", version="0.1.0")

# Include routers
app.include_router(memory.router)
app.include_router(reasoning.router)
app.include_router(search.router)
app.include_router(execution.router)
app.include_router(insights.router)
app.include_router(agent.router)
app.include_router(voice.router)


@app.get("/health")
def health_check() -> dict[str, str]:
    """Simple health check endpoint."""
    return {"status": "ok"}