"""Execution API endpoint for Opera."""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional

from opera.backend.models.reasoning import Plan
from opera.backend.services.executor import PlanExecutor, PlanExecutionResult
from opera.backend.tools.registry import ToolPermission, get_registry

router = APIRouter(prefix="/execute", tags=["execution"])
executor = PlanExecutor()


class ExecutePlanRequest(BaseModel):
    plan: Plan
    allowed_permissions: Optional[List[str]] = None


@router.post("/plan", response_model=PlanExecutionResult)
def execute_plan(request: ExecutePlanRequest):
    """
    Execute a plan by running its steps through registered tools.
    
    Args:
        request: Execution request with plan and permissions
        
    Returns:
        Execution result with outputs from each step
    """
    # Convert permission strings to enum
    allowed_perms = None
    if request.allowed_permissions:
        try:
            allowed_perms = [ToolPermission(p) for p in request.allowed_permissions]
        except ValueError as e:
            raise HTTPException(status_code=400, detail=f"Invalid permission: {e}")
    
    result = executor.execute_plan(request.plan, allowed_perms)
    return result


@router.get("/tools")
def list_tools():
    """List all available tools."""
    registry = get_registry()
    schemas = registry.get_all_schemas()
    
    return {
        "tools": [
            {
                "name": schema.name,
                "description": schema.description,
                "permissions": [p.value for p in schema.permissions],
                "parameters": [
                    {
                        "name": p.name,
                        "type": p.type,
                        "required": p.required,
                        "description": p.description
                    }
                    for p in schema.parameters
                ]
            }
            for schema in schemas
        ]
    }
