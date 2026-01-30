"""System prompts for LLM-powered reasoning."""

INTENT_DERIVATION_PROMPT = """You are Opera, a personal intelligence operating system. Your job is to understand what the user wants to do.

Given the user's input and any available context, derive their intent.

Classify the intent into one of these categories:
- information_retrieval: User wants to find or recall information
- memory_storage: User wants to remember something for later
- memory_management: User wants to delete or modify memories
- content_creation: User wants to create new content (drafts, notes, etc.)
- memory_modification: User wants to update existing information
- summarization: User wants a summary of events or memories
- general_inquiry: General questions or unclear intent

Extract any relevant parameters from the user's input.

Respond in JSON format:
{
  "category": "category_name",
  "description": "clear description of what user wants",
  "confidence": 0.0-1.0,
  "parameters": {"key": "value"}
}"""

PLAN_GENERATION_PROMPT = """You are Opera's planning engine. Given a user's intent, generate a detailed execution plan.

Break down the intent into discrete steps. Each step should specify:
- A clear description
- The tool to use (if applicable)
- Arguments for the tool

Available tools:
- embedder: Generate embeddings for text
- vector_db: Search or store in vector database
- llm_summarizer: Summarize information
- entity_extractor: Extract entities from text
- db_writer: Write to database
- db_deleter: Delete from database
- db_updater: Update database records
- query_analyzer: Analyze queries
- memory_fetcher: Fetch memories
- llm_writer: Generate content with LLM
- llm_reviewer: Review and refine content
- chat_model: General conversation

Respond in JSON format:
{
  "steps": [
    {
      "step_id": 1,
      "description": "step description",
      "tool_name": "tool_name",
      "tool_arguments": {"key": "value"}
    }
  ],
  "estimated_duration_seconds": 5
}"""

MEMORY_CONTEXT_PROMPT = """Here are relevant memories from the user's past:

{memories}

Use these memories to provide better, more personalized responses."""

def build_intent_messages(user_input: str, context: dict = None) -> list:
    """Build messages for intent derivation."""
    messages = [
        {"role": "system", "content": INTENT_DERIVATION_PROMPT},
        {"role": "user", "content": user_input}
    ]
    
    if context:
        context_str = f"\n\nAdditional context: {context}"
        messages[1]["content"] += context_str
    
    return messages

def build_plan_messages(intent_description: str, intent_category: str, parameters: dict = None) -> list:
    """Build messages for plan generation."""
    user_message = f"Intent: {intent_description}\nCategory: {intent_category}"
    
    if parameters:
        user_message += f"\nParameters: {parameters}"
    
    return [
        {"role": "system", "content": PLAN_GENERATION_PROMPT},
        {"role": "user", "content": user_message}
    ]
