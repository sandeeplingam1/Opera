"""Tool registry and decorator framework for Opera.

This module provides the infrastructure for registering and discovering
tools that can be executed by the plan executor.
"""
from typing import Dict, List, Callable, Any, Optional
from pydantic import BaseModel, Field
from enum import Enum
import inspect


class ToolPermission(str, Enum):
    """Permission levels for tool execution."""
    READ = "read"           # Read-only operations
    WRITE = "write"         # Write operations
    DELETE = "delete"       # Deletion operations
    NETWORK = "network"     # Network access
    SYSTEM = "system"       # System-level operations


class ToolParameter(BaseModel):
    """Schema for a tool parameter."""
    name: str
    type: str
    description: str
    required: bool = True
    default: Optional[Any] = None


class ToolSchema(BaseModel):
    """Schema definition for a tool."""
    name: str
    description: str
    parameters: List[ToolParameter]
    returns: str
    permissions: List[ToolPermission]
    examples: List[str] = Field(default_factory=list)


class Tool:
    """Wrapper class for a registered tool."""
    
    def __init__(
        self,
        func: Callable,
        schema: ToolSchema
    ):
        self.func = func
        self.schema = schema
        self.name = schema.name
    
    def execute(self, **kwargs) -> Any:
        """Execute the tool with given arguments."""
        return self.func(**kwargs)
    
    def __repr__(self) -> str:
        return f"Tool(name={self.name}, permissions={self.schema.permissions})"


class ToolRegistry:
    """Global registry for all available tools."""
    
    def __init__(self):
        self._tools: Dict[str, Tool] = {}
    
    def register(self, tool: Tool) -> None:
        """Register a tool in the registry."""
        if tool.name in self._tools:
            raise ValueError(f"Tool '{tool.name}' already registered")
        self._tools[tool.name] = tool
    
    def get(self, name: str) -> Optional[Tool]:
        """Get a tool by name."""
        return self._tools.get(name)
    
    def list_tools(self) -> List[str]:
        """List all registered tool names."""
        return list(self._tools.keys())
    
    def get_all_schemas(self) -> List[ToolSchema]:
        """Get schemas for all registered tools."""
        return [tool.schema for tool in self._tools.values()]


# Global registry instance
_registry = ToolRegistry()


def tool(
    name: str,
    description: str,
    permissions: List[ToolPermission] = None,
    examples: List[str] = None
):
    """
    Decorator to register a function as a tool.
    
    Args:
        name: Name of the tool
        description: Description of what the tool does
        permissions: Required permissions
        examples: Example usage strings
        
    Returns:
        Decorated function
        
    Example:
        @tool(
            name="read_file",
            description="Read contents of a file",
            permissions=[ToolPermission.READ],
            examples=["read_file(path='/tmp/test.txt')"]
        )
        def read_file(path: str) -> str:
            with open(path) as f:
                return f.read()
    """
    def decorator(func: Callable) -> Callable:
        # Extract parameters from function signature
        sig = inspect.signature(func)
        parameters = []
        
        for param_name, param in sig.parameters.items():
            param_type = "string"  # Default type
            if param.annotation != inspect.Parameter.empty:
                param_type = param.annotation.__name__
            
            parameters.append(ToolParameter(
                name=param_name,
                type=param_type,
                description=f"Parameter: {param_name}",
                required=param.default == inspect.Parameter.empty,
                default=param.default if param.default != inspect.Parameter.empty else None
            ))
        
        # Get return type
        return_type = "Any"
        if sig.return_annotation != inspect.Signature.empty:
            return_type = sig.return_annotation.__name__
        
        # Create schema
        schema = ToolSchema(
            name=name,
            description=description,
            parameters=parameters,
            returns=return_type,
            permissions=permissions or [ToolPermission.READ],
            examples=examples or []
        )
        
        # Create and register tool
        tool_instance = Tool(func=func, schema=schema)
        _registry.register(tool_instance)
        
        return func
    
    return decorator


def get_registry() -> ToolRegistry:
    """Get the global tool registry."""
    return _registry
