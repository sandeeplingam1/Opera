import unittest
from opera.backend.services.reasoning_service import ReasoningService
from opera.backend.models.reasoning import Intent, PlanStep

class TestReasoningService(unittest.TestCase):
    def setUp(self):
        self.service = ReasoningService()

    def test_derive_intent_retrieval(self):
        """Test that 'find' queries are classified as information_retrieval."""
        intent = self.service.derive_intent("Find my old resume")
        self.assertEqual(intent.category, "information_retrieval")
        self.assertIn("resume", intent.description)

    def test_derive_intent_management(self):
        """Test that 'delete' queries are classified as memory_management."""
        intent = self.service.derive_intent("Delete all emails")
        self.assertEqual(intent.category, "memory_management")
        self.assertIn("delete", intent.description.lower())

    def test_generate_plan_retrieval(self):
        """Test that retrieval intents generate search plans."""
        intent = Intent(
            category="information_retrieval",
            description="find something",
            confidence=1.0,
            parameters={"query": "test"}
        )
        plan = self.service.generate_plan(intent)
        self.assertTrue(len(plan.steps) > 0)
        self.assertEqual(plan.steps[1].tool_name, "vector_db")

    def test_preview_action_high_risk(self):
        """Test that delete actions are flagged as high risk."""
        step = PlanStep(step_id=1, description="Delete all matching records", tool_name="db_deleter")
        preview = self.service.preview_action(step)
        self.assertEqual(preview.risk_level, "high")
        self.assertIn("permanently remove", preview.preview_message)

    def test_derive_intent_creation(self):
        """Test that 'create' queries are classified as content_creation."""
        intent = self.service.derive_intent("Draft a new blog post")
        self.assertEqual(intent.category, "content_creation")
    
    def test_derive_intent_modification(self):
        """Test that 'update' queries are classified as memory_modification."""
        intent = self.service.derive_intent("Update the meeting time")
        self.assertEqual(intent.category, "memory_modification")
    
    def test_derive_intent_summarization(self):
        """Test that 'summarize' queries are classified as summarization."""
        intent = self.service.derive_intent("Summarize today's events")
        self.assertEqual(intent.category, "summarization")

    def test_preview_action_medium_risk(self):
        """Test that modification actions are flagged as medium risk."""
        step = PlanStep(step_id=1, description="Update the record", tool_name="db_updater")
        preview = self.service.preview_action(step)
        self.assertEqual(preview.risk_level, "medium")

    def test_preview_action_low_risk(self):
        """Test that read/store actions are flagged as low risk."""
        step = PlanStep(step_id=1, description="Store this memory", tool_name="db_writer")
        preview = self.service.preview_action(step)
        self.assertEqual(preview.risk_level, "low")

if __name__ == '__main__':
    unittest.main()
