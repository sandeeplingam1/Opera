from fastapi import APIRouter
from typing import List
import uuid

from opera.backend.models.reasoning import (
    IntentRequest, Intent,
    PlanRequest, Plan, PlanStep,
    ActionPreviewRequest, ActionPreview
)
from opera.backend.services.reasoning_service import ReasoningService

router = APIRouter(tags=["reasoning"])
service = ReasoningService()

@router.post("/intent/derive", response_model=Intent)
def derive_intent(request: IntentRequest):
    """
    Derives structured intent from user input using the reasoning service.
    """
    return service.derive_intent(request.user_input, request.context)

@router.post("/plan/generate", response_model=Plan)
def generate_plan(request: PlanRequest):
    """
    Generates a plan based on the provided intent.
    """
    return service.generate_plan(request.intent)

@router.post("/action/preview", response_model=ActionPreview)
def preview_action(request: ActionPreviewRequest):
    """
    Previews the side effects of a plan step.
    """
    return service.preview_action(request.plan_step)
