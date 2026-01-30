"""Plan executor for Opera."""
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from opera.backend.models.reasoning import Plan, PlanStep
from opera.backend.tools.registry import get_registry, ToolPermission


class ExecutionResult(BaseModel):
    """Result of executing a plan step."""
    step_id: int
    success: bool
    output: Any
    error: Optional[str] = None


class PlanExecutionResult(BaseModel):
    """Result of executing an entire plan."""
    plan_id: str
    success: bool
    steps: List[ExecutionResult]
    error: Optional[str] = None


class PlanExecutor:
    """Executes plans by running their steps through registered tools."""
    
    def __init__(self):
        self.registry = get_registry()
    
    def execute_plan(self, plan: Plan, allowed_permissions: List[ToolPermission] = None) -> PlanExecutionResult:
        """
        Execute a complete plan.
        
        Args:
            plan: The plan to execute
            allowed_permissions: List of permissions to allow (default: all)
            
        Returns:
            Plan execution result
        """
        if allowed_permissions is None:
            # Default: allow read and basic operations
            allowed_permissions = [
                ToolPermission.READ,
                ToolPermission.WRITE
            ]
        
        step_results = []
        
        for step in plan.steps:
            result = self.execute_step(step, allowed_permissions)
            step_results.append(result)
            
            # Stop execution if a step fails
            if not result.success:
                return PlanExecutionResult(
                    plan_id=plan.plan_id,
                    success=False,
                    steps=step_results,
                    error=f"Step {step.step_id} failed: {result.error}"
                )
        
        return PlanExecutionResult(
            plan_id=plan.plan_id,
            success=True,
            steps=step_results
        )
    
    def execute_step(
        self,
        step: PlanStep,
        allowed_permissions: List[ToolPermission]
    ) -> ExecutionResult:
        """
        Execute a single plan step.
        
        Args:
            step: The step to execute
            allowed_permissions: Allowed permissions
            
        Returns:
            Execution result
        """
        if not step.tool_name:
            return ExecutionResult(
                step_id=step.step_id,
                success=True,
                output=f"Skipped: {step.description} (no tool specified)"
            )
        
        # Get tool from registry
        tool = self.registry.get(step.tool_name)
        
        if not tool:
            return ExecutionResult(
                step_id=step.step_id,
                success=False,
                output=None,
                error=f"Tool '{step.tool_name}' not found in registry"
            )
        
        # Check permissions
        for permission in tool.schema.permissions:
            if permission not in allowed_permissions:
                return ExecutionResult(
                    step_id=step.step_id,
                    success=False,
                    output=None,
                    error=f"Permission denied: tool requires {permission}"
                )
        
        # Execute the tool
        try:
            output = tool.execute(**(step.tool_arguments or {}))
            return ExecutionResult(
                step_id=step.step_id,
                success=True,
                output=output
            )
        except Exception as e:
            return ExecutionResult(
                step_id=step.step_id,
                success=False,
                output=None,
                error=str(e)
            )
