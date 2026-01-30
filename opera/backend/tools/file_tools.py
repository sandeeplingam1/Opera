"""File system tools for Opera."""
import os
from typing import List
from opera.backend.tools.registry import tool, ToolPermission


@tool(
    name="read_file",
    description="Read the contents of a file",
    permissions=[ToolPermission.READ],
    examples=["read_file(path='/tmp/notes.txt')"]
)
def read_file(path: str) -> str:
    """Read and return the contents of a file."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")
    
    with open(path, 'r') as f:
        return f.read()


@tool(
    name="write_file",
    description="Write content to a file",
    permissions=[ToolPermission.WRITE],
    examples=["write_file(path='/tmp/note.txt', content='Hello World')"]
)
def write_file(path: str, content: str) -> str:
    """Write content to a file."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    
    with open(path, 'w') as f:
        f.write(content)
    
    return f"Successfully wrote to {path}"


@tool(
    name="list_files",
    description="List files in a directory",
    permissions=[ToolPermission.READ],
    examples=["list_files(directory='/tmp')"]
)
def list_files(directory: str) -> List[str]:
    """List all files in a directory."""
    if not os.path.exists(directory):
        raise FileNotFoundError(f"Directory not found: {directory}")
    
    return os.listdir(directory)
