"""Web tools for Opera."""
import requests
from bs4 import BeautifulSoup
from typing import Dict, Any
from opera.backend.tools.registry import tool, ToolPermission


@tool(
    name="fetch_url",
    description="Fetch content from a URL",
    permissions=[ToolPermission.NETWORK],
    examples=["fetch_url(url='https://example.com')"]
)
def fetch_url(url: str) -> str:
    """Fetch and return the text content of a URL."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        # Parse HTML and extract text
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        return text[:5000]  # Limit to 5000 chars
    except Exception as e:
        return f"Error fetching URL: {e}"


@tool(
    name="search_web",
    description="Search the web (placeholder - requires API key)",
    permissions=[ToolPermission.NETWORK],
    examples=["search_web(query='Python programming')"]
)
def search_web(query: str) -> str:
    """
    Search the web for information.
    
    Note: This is a placeholder. In production, integrate with:
    - Google Custom Search API
    - Bing Search API
    - DuckDuckGo API
    """
    return f"Web search for '{query}' - Integration pending. Add API key to enable."
