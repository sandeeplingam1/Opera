"""LLM client abstraction for Opera."""
from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Iterator
from openai import OpenAI
from opera.backend.config import config


class LLMClient(ABC):
    """Abstract base class for LLM clients."""
    
    @abstractmethod
    def complete(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Generate a completion from messages."""
        pass
    
    @abstractmethod
    def stream(self, messages: List[Dict[str, str]], **kwargs) -> Iterator[str]:
        """Stream a completion from messages."""
        pass


class OpenAIClient(LLMClient):
    """OpenAI API client."""
    
    def __init__(self, model: Optional[str] = None):
        """Initialize OpenAI client."""
        if not config.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY not set in environment")
        self.client = OpenAI(api_key=config.OPENAI_API_KEY)
        self.model = model or config.OPENAI_MODEL
    
    def complete(
        self, 
        messages: List[Dict[str, str]], 
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> str:
        """
        Generate a completion from messages.
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            
        Returns:
            The completion text
        """
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        )
        return response.choices[0].message.content
    
    def stream(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> Iterator[str]:
        """
        Stream a completion from messages.
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            
        Yields:
            Chunks of completion text
        """
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=True,
            **kwargs
        )
        
        for chunk in response:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content


class HuggingFaceClient(LLMClient):
    """Local Hugging Face model client for completely free inference."""
    
    def __init__(self, model: Optional[str] = None):
        """Initialize Hugging Face pipeline."""
        from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
        import torch
        
        self.model_name = model or config.LOCAL_MODEL_NAME
        print(f"Loading local model: {self.model_name}...")
        
        # Determine device
        self.device = "mps" if torch.backends.mps.is_available() else "cpu"
        print(f"Using device: {self.device}")
        
        # Load tokenizer and model
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_name,
            cache_dir=config.MODEL_CACHE_DIR
        )
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            cache_dir=config.MODEL_CACHE_DIR,
            torch_dtype=torch.float16 if self.device == "mps" else torch.float32
        ).to(self.device)
        
        print(f"Model loaded successfully on {self.device}")
    
    def _format_messages(self, messages: List[Dict[str, str]]) -> str:
        """Convert chat messages to a prompt string."""
        formatted = ""
        for msg in messages:
            role = msg["role"]
            content = msg["content"]
            if role == "system":
                formatted += f"System: {content}\n\n"
            elif role == "user":
                formatted += f"User: {content}\n\n"
            elif role == "assistant":
                formatted += f"Assistant: {content}\n\n"
        formatted += "Assistant:"
        return formatted
    
    def complete(
        self, 
        messages: List[Dict[str, str]], 
        temperature: float = 0.7,
        max_tokens: Optional[int] = 512,
        **kwargs
    ) -> str:
        """
        Generate a completion using local Llama model.
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            
        Returns:
            The completion text
        """
        import torch
        
        prompt = self._format_messages(messages)
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_tokens or 512,
                temperature=temperature,
                do_sample=temperature > 0,
                pad_token_id=self.tokenizer.eos_token_id
            )
        
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        # Extract only the new generated text
        response = response[len(prompt):].strip()
        return response
    
    def stream(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = 512,
        **kwargs
    ) -> Iterator[str]:
        """
        Stream a completion (simplified - returns full response for now).
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            
        Yields:
            Chunks of completion text
        """
        # For now, return the full response as one chunk
        # TODO: Implement proper streaming with TextIteratorStreamer
        response = self.complete(messages, temperature, max_tokens, **kwargs)
        yield response



# Global LLM client instance
_llm_client: Optional[LLMClient] = None

def get_llm_client() -> LLMClient:
    """Get or create the global LLM client based on configuration."""
    global _llm_client
    if _llm_client is None:
        if config.USE_LOCAL_MODEL:
            print("Initializing local Hugging Face model...")
            _llm_client = HuggingFaceClient()
        else:
            print("Initializing OpenAI client...")
            _llm_client = OpenAIClient()
    return _llm_client

