import os
import sys
import unittest
from unittest.mock import MagicMock

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import generate_brief

class TestTaskAutomationAgent(unittest.TestCase):
    def test_empty_topic_handling(self):
        """Test handling of empty and whitespace topics without API call."""
        res_empty = generate_brief("")
        self.assertIn("Error: Topic cannot be empty", res_empty)

        res_whitespace = generate_brief("   \n\t  ")
        self.assertIn("Error: Topic cannot be empty", res_whitespace)

    def test_bullet_formatting_with_mock_client(self):
        """Test mock Groq client returning exactly 3 bullet points."""
        mock_client = MagicMock()
        mock_choice = MagicMock()
        mock_choice.message.content = (
            "- MLOps automates the deployment, monitoring, and governance of machine learning models in production.\n"
            "- Continuous Integration and Continuous Deployment (CI/CD) pipelines ensure repeatable releases and test coverage.\n"
            "- Observability tools track model drift, latency, and system health to maintain performance over time."
        )
        mock_response = MagicMock()
        mock_response.choices = [mock_choice]
        mock_client.chat.completions.create.return_value = mock_response

        result = generate_brief("MLOps Pipelines", client=mock_client)

        self.assertNotIn("Error", result)
        lines = [line.strip() for line in result.strip().split("\n") if line.strip()]
        self.assertEqual(len(lines), 3)
        for line in lines:
            self.assertTrue(line.startswith("-") or line.startswith("*"))
        mock_client.chat.completions.create.assert_called_once()

    def test_fallback_model_on_primary_failure(self):
        """Test fallback model behavior when primary model raises an exception."""
        mock_client = MagicMock()
        # First call fails, second call succeeds
        mock_choice = MagicMock()
        mock_choice.message.content = (
            "* Fallback bullet one.\n"
            "* Fallback bullet two.\n"
            "* Fallback bullet three."
        )
        mock_response = MagicMock()
        mock_response.choices = [mock_choice]

        mock_client.chat.completions.create.side_effect = [
            RuntimeError("Primary compound-mini unavailable"),
            mock_response
        ]

        result = generate_brief("Containerization", client=mock_client)
        self.assertIn("Fallback bullet one", result)
        self.assertEqual(mock_client.chat.completions.create.call_count, 2)

    def test_missing_api_key_handling(self):
        """Test behavior when GROQ_API_KEY is not set."""
        original_key = os.environ.get("GROQ_API_KEY")
        try:
            if "GROQ_API_KEY" in os.environ:
                del os.environ["GROQ_API_KEY"]
            result = generate_brief("Docker Architecture")
            self.assertIn("Error: GROQ_API_KEY is not configured", result)
        finally:
            if original_key is not None:
                os.environ["GROQ_API_KEY"] = original_key

if __name__ == "__main__":
    unittest.main()
