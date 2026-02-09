# agents/biomechanism.py

"""
BioMechanismAgent - calls Gemini API to analyze drug mechanism of action.
"""

from typing import Dict, Any
import logging
import json
from utils.gemini_client import GeminiClient
from utils.validators import validate_json

logger = logging.getLogger("BioMechanismAgent")


class BioMechanismAgent:
    def __init__(self, use_mock: bool = False, api_key: str | None = None):
        self.use_mock = use_mock
        self.api_key = api_key
        self.client = GeminiClient(api_key=api_key)

    def run(self, drug: str, disease: str) -> Dict[str, Any]:
        """
        Calls Gemini API to analyze drug mechanism against disease.
        Returns structured analysis with mechanism summary, targets, and confidence.
        """

        logger.info(f"BioMechanismAgent: analyzing drug={drug}, disease={disease}")

        # Build the prompt for Gemini
        prompt = f"""Analyze the mechanism of action of {drug} for treating {disease}.

Return a JSON object with the following structure:
{{
  "summary": "A clear 2-3 sentence explanation of how {drug} might work against {disease}",
  "steps": ["step 1 of mechanism", "step 2", "step 3"],
  "targets": ["primary target protein/receptor", "secondary target if applicable"],
  "confidence": 75
}}

Important: Return ONLY valid JSON, no markdown, no extra text.
The confidence score should be 0-100 based on how well-established the mechanism is."""

        try:
            # Call Gemini API
            response_text = self.client.generate_text(prompt)
            logger.info(f"Gemini response: {response_text[:200]}...")

            # Extract JSON from response
            json_str = response_text.strip()
            if "```json" in json_str:
                json_str = json_str.split("```json")[1].split("```")[0].strip()
            elif "```" in json_str:
                json_str = json_str.split("```")[1].split("```")[0].strip()

            result = json.loads(json_str)

            # Validate against schema
            schema_path = "schemas/biomechanism_schema.json"
            validate_json(result, schema_path)

            logger.info("BioMechanismAgent: completed successfully.")
            return result

        except Exception as e:
            logger.error(f"BioMechanismAgent error: {e}")
            # Fallback to basic analysis
            return {
                "summary": f"Unable to retrieve mechanism analysis for {drug} treating {disease}. Please check your API key.",
                "steps": ["Analysis failed"],
                "targets": ["Unknown"],
                "confidence": 0
            }


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    agent = BioMechanismAgent()
    out = agent.run("Montelukast", "COPD")
    import json
    print(json.dumps(out, indent=2))
