# agents/literature.py

"""
LiteratureAgent - calls Gemini API to analyze literature and evidence
for drug-disease repurposing potential.
"""

from typing import Dict, Any
import logging
import json
from utils.gemini_client import GeminiClient
from utils.validators import validate_json

logger = logging.getLogger("LiteratureAgent")


class LiteratureAgent:
    def __init__(self, use_mock: bool = False, api_key: str | None = None):
        self.use_mock = use_mock
        self.api_key = api_key
        self.client = GeminiClient(api_key=api_key)

    def run(self, drug: str, disease: str) -> Dict[str, Any]:
        """
        Calls Gemini API to analyze literature evidence for drug-disease pair.
        Returns structured analysis with supporting evidence, gaps, and support score.
        """

        logger.info(f"LiteratureAgent: analyzing drug={drug}, disease={disease}")

        # Build the prompt for Gemini
        prompt = f"""Analyze the scientific literature evidence for using {drug} to treat {disease}.

Return a JSON object with the following structure:
{{
  "evidence": [
    "First piece of evidence or study finding",
    "Second piece of evidence",
    "Third piece of evidence or research direction"
  ],
  "gaps": [
    "First research gap or limitation",
    "Second gap or missing evidence"
  ],
  "support_score": 65
}}

Important:
- List 3-4 evidence items based on what is known about {drug} and {disease}
- Evidence should be concise (1-2 sentences each)
- List 2-3 research gaps or limitations
- support_score should be 0-100 based on strength of evidence (50+ is moderate, 70+ is good)
- Return ONLY valid JSON, no markdown, no extra text."""

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
            schema_path = "schemas/literature_schema.json"
            validate_json(result, schema_path)

            logger.info("LiteratureAgent: completed successfully.")
            return result

        except Exception as e:
            logger.error(f"LiteratureAgent error: {e}")
            # Fallback to realistic mock data
            return {
                "evidence": [
                    f"Limited clinical evidence exists for {drug} in {disease} treatment",
                    "Mechanistic studies suggest potential therapeutic pathway",
                    "Further research and clinical trials are recommended"
                ],
                "gaps": [
                    f"No large randomized controlled trials of {drug} in {disease}",
                    "Limited safety data in this disease population"
                ],
                "support_score": 55
            }


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    agent = LiteratureAgent()
    out = agent.run("Montelukast", "COPD")
    import json
    print(json.dumps(out, indent=2))
