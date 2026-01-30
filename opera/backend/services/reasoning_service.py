from typing import List, Dict
import uuid
import json
from opera.backend.models.reasoning import (
    Intent, Plan, PlanStep, ActionPreview
)
from opera.backend.services.llm_client import get_llm_client
from opera.backend.services.prompts import build_intent_messages, build_plan_messages


class ReasoningService:
    def __init__(self):
        """Initialize reasoning service with LLM client."""
        try:
            self.llm = get_llm_client()
            self.use_llm = True
        except ValueError as e:
            print(f"Warning: LLM not available, falling back to rule-based: {e}")
            self.llm = None
            self.use_llm = False
    
    def derive_intent(self, user_input: str, context: dict = None) -> Intent:
        """
        Derives intent using LLM or falls back to rule-based heuristics.
        """
        if self.use_llm and self.llm:
            return self._derive_intent_llm(user_input, context)
        else:
            return self._derive_intent_rules(user_input)
    
    def _derive_intent_llm(self, user_input: str, context: dict = None) -> Intent:
        """Use LLM to derive intent."""
        messages = build_intent_messages(user_input, context)
        
        try:
            response = self.llm.complete(messages, temperature=0.3, max_tokens=300)
            # Parse JSON response
            intent_data = json.loads(response)
            
            return Intent(
                category=intent_data.get("category", "general_inquiry"),
                description=intent_data.get("description", user_input),
                confidence=intent_data.get("confidence", 0.8),
                parameters=intent_data.get("parameters", {"query": user_input})
            )
        except Exception as e:
            print(f"LLM intent derivation failed: {e}, falling back to rules")
            return self._derive_intent_rules(user_input)
    
    def _derive_intent_rules(self, user_input: str) -> Intent:
        """Fallback rule-based intent derivation."""
        text = user_input.lower()
        
        if "find" in text or "search" in text or "what is" in text:
            category = "information_retrieval"
            description = f"User wants to retrieve information: {user_input}"
        elif "remember" in text or "save" in text or "store" in text:
            category = "memory_storage"
            description = f"User wants to store a memory: {user_input}"
        elif "delete" in text or "remove" in text:
            category = "memory_management"
            description = f"User wants to delete information: {user_input}"
        elif "create" in text or "draft" in text or "write" in text:
            category = "content_creation"
            description = f"User wants to create content: {user_input}"
        elif "update" in text or "edit" in text or "modify" in text:
            category = "memory_modification"
            description = f"User wants to modify information: {user_input}"
        elif "summarize" in text or "summarise" in text:
            category = "summarization"
            description = f"User wants a summary: {user_input}"
        else:
            category = "general_inquiry"
            description = f"User wants to: {user_input}"
            
        return Intent(
            category=category,
            description=description,
            confidence=0.85,
            parameters={"query": user_input}
        )

    def generate_plan(self, intent: Intent) -> Plan:
        """
        Generates a plan using LLM or falls back to rule-based generation.
        """
        if self.use_llm and self.llm:
            return self._generate_plan_llm(intent)
        else:
            return self._generate_plan_rules(intent)
    
    def _generate_plan_llm(self, intent: Intent) -> Plan:
        """Use LLM to generate execution plan."""
        messages = build_plan_messages(
            intent.description,
            intent.category,
            intent.parameters
        )
        
        try:
            response = self.llm.complete(messages, temperature=0.3, max_tokens=500)
            plan_data = json.loads(response)
            
            steps = [
                PlanStep(
                    step_id=step.get("step_id", i+1),
                    description=step.get("description", ""),
                    tool_name=step.get("tool_name"),
                    tool_arguments=step.get("tool_arguments", {})
                )
                for i, step in enumerate(plan_data.get("steps", []))
            ]
            
            return Plan(
                plan_id=str(uuid.uuid4()),
                steps=steps,
                estimated_duration_seconds=plan_data.get("estimated_duration_seconds", 5)
            )
        except Exception as e:
            print(f"LLM plan generation failed: {e}, falling back to rules")
            return self._generate_plan_rules(intent)
    
    def _generate_plan_rules(self, intent: Intent) -> Plan:
        """Fallback rule-based plan generation."""
        steps = []
        plan_id = str(uuid.uuid4())
        
        if intent.category == "information_retrieval":
            steps = [
                PlanStep(step_id=1, description="Embed user query", tool_name="embedder", tool_arguments={"text": intent.parameters.get("query")}),
                PlanStep(step_id=2, description="Search vector database", tool_name="vector_db", tool_arguments={"op": "query"}),
                PlanStep(step_id=3, description="Summarize results", tool_name="llm_summarizer", tool_arguments={})
            ]
            duration = 3
        elif intent.category == "memory_storage":
            steps = [
                PlanStep(step_id=1, description="Extract memory entities", tool_name="entity_extractor", tool_arguments={}),
                PlanStep(step_id=2, description="Store in database", tool_name="db_writer", tool_arguments={})
            ]
            duration = 2
        elif intent.category == "memory_management":
             steps = [
                PlanStep(step_id=1, description="Identify items to delete", tool_name="query_analyzer", tool_arguments={}),
                PlanStep(step_id=2, description="Execute deletion", tool_name="db_deleter", tool_arguments={})
            ]
             duration = 5
        elif intent.category == "content_creation":
            steps = [
                PlanStep(step_id=1, description="Retrieve relevant context", tool_name="vector_db", tool_arguments={}),
                PlanStep(step_id=2, description="Draft content", tool_name="llm_writer", tool_arguments={}),
                PlanStep(step_id=3, description="Review and refine", tool_name="llm_reviewer", tool_arguments={})
            ]
            duration = 10
        elif intent.category == "memory_modification":
            steps = [
                PlanStep(step_id=1, description="Locate item to modify", tool_name="vector_db", tool_arguments={}),
                PlanStep(step_id=2, description="Apply modification", tool_name="db_updater", tool_arguments={})
            ]
            duration = 4
        elif intent.category == "summarization":
            steps = [
                PlanStep(step_id=1, description="Retrieve recent memories", tool_name="memory_fetcher", tool_arguments={}),
                PlanStep(step_id=2, description="Generate summary", tool_name="llm_summarizer", tool_arguments={})
            ]
            duration = 5
        else:
            steps = [
                PlanStep(step_id=1, description="Process general inquiry", tool_name="chat_model", tool_arguments={})
            ]
            duration = 2
            
        return Plan(
            plan_id=plan_id,
            steps=steps,
            estimated_duration_seconds=duration
        )

    def preview_action(self, step: PlanStep) -> ActionPreview:
        """
        Previews the side effects and risks of a plan step.
        """
        desc = step.description.lower()
        if "delete" in desc or "remove" in desc:
            return ActionPreview(
                preview_message="This action will permanently remove data.",
                side_effects=["Data deletion", "Audit log entry"],
                risk_level="high"
            )
        elif "store" in desc or "save" in desc:
             return ActionPreview(
                preview_message="This action will save new data to long-term memory.",
                side_effects=["Database write"],
                risk_level="low"
            )
        elif "modify" in desc or "update" in desc or "edit" in desc:
            return ActionPreview(
                preview_message="This action will modify existing data.",
                side_effects=["Database update", "Version history"],
                risk_level="medium"
            )
        elif "draft" in desc or "write" in desc or "generate" in desc:
             return ActionPreview(
                preview_message="This action generates new content but doesn't persist it yet.",
                side_effects=["Compute usage"],
                risk_level="low"
            )
        else:
            return ActionPreview(
                preview_message="This action reads data or performs internal processing.",
                side_effects=["Read access"],
                risk_level="low"
            )

