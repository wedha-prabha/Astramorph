# utils/gemini_client.py
"""
Lightweight Gemini client wrapper.
- Put your Gemini API key in HARDCODED_API_KEY below.
- If you leave it empty, it will try environment variable GEMINI_API_KEY.
- If no key or SDK, it runs in mock mode with deterministic fake JSON.
"""

import os
import time
import logging
from typing import Optional

try:
    from google import genai  # google-genai SDK
    GENAI_AVAILABLE = True
except Exception:
    GENAI_AVAILABLE = False

logger = logging.getLogger("GeminiClient")
logger.setLevel(logging.INFO)
if not logger.handlers:
    h = logging.StreamHandler()
    h.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
    logger.addHandler(h)

DEFAULT_MODEL = "gemini-2.5-flash"
ENV_KEY = "GEMINI_API_KEY"

# 🔴 PUT YOUR KEY HERE (string). Example: "AIzaSy...."
HARDCODED_API_KEY = "AIzaSyAcY6jF23pMElbo8cxcxMEgKZXlycP-7Ik"  # <-- paste your key between the quotes


class GeminiClient:
    def __init__(self, api_key: Optional[str] = None, model: str = DEFAULT_MODEL):
        key_from_env = os.environ.get(ENV_KEY)
        self.api_key = api_key or HARDCODED_API_KEY or key_from_env
        self.model = model
        self._mock_mode = False

        if not self.api_key:
            logger.warning("No Gemini API key found – running in MOCK MODE.")
            self._mock_mode = True

        if self.api_key and GENAI_AVAILABLE:
            try:
                genai.configure(api_key=self.api_key)
                logger.info("Gemini client configured (model=%s)", self.model)
            except Exception as e:
                logger.error("Failed to configure Gemini client: %s", e)
                self._mock_mode = True
        elif self.api_key and not GENAI_AVAILABLE:
            logger.warning("google-genai SDK not installed – MOCK MODE.")
            self._mock_mode = True

    def is_mock(self) -> bool:
        return self._mock_mode

    def generate_text(self, prompt: str, timeout_sec: int = 30,
                      max_retries: int = 3) -> str:
        """Return raw text from Gemini or deterministic mock JSON string based on prompt."""
        if self._mock_mode:
            logger.info("GeminiClient in MOCK MODE – returning contextual mock JSON.")
            
            import json
            
            # Extract drug and disease from prompt for context-aware mock data
            drug_name = "Unknown Drug"
            disease_name = "Unknown Disease"
            
            # Parse prompt to extract drug and disease names
            if " of " in prompt and " for " in prompt:
                try:
                    of_idx = prompt.find(" of ")
                    for_idx = prompt.find(" for ")
                    if of_idx > 0 and for_idx > of_idx:
                        drug_name = prompt[of_idx + 4:for_idx].strip().split()[0]
                        treating_idx = prompt.find(" treating ")
                        if treating_idx > 0:
                            disease_name = prompt[treating_idx + 10:].split()[0].rstrip('.,')
                except:
                    pass
            
            # Generate contextual mock data
            mechanism_examples = {
                "montelukast": "CysLT1 receptor antagonist reducing leukotriene-mediated inflammation",
                "aspirin": "COX inhibitor reducing platelet aggregation and inflammation",
                "metformin": "AMP kinase activator improving insulin sensitivity",
                "atorvastatin": "HMG-CoA reductase inhibitor lowering cholesterol",
                "ibuprofen": "NSAID reducing prostaglandin-mediated inflammation",
            }
            
            disease_targets = {
                "copd": ["CysLT1 receptor", "Inflammatory cytokines"],
                "asthma": ["CysLT1 receptor", "Th2 cells"],
                "diabetes": ["AMPK pathway", "Glucose transporters"],
                "heart disease": ["LDL cholesterol", "Platelet aggregation"],
                "arthritis": ["COX enzymes", "Inflammatory cytokines"],
            }
            
            # Generate mechanism summary based on drug/disease
            mechanism = mechanism_examples.get(drug_name.lower(), 
                f"Modulates biological pathways relevant to {disease_name}")
            targets = disease_targets.get(disease_name.lower(), 
                [f"{disease_name} pathway 1", f"{disease_name} pathway 2"])
            
            # Build evidence based on disease
            evidence_by_disease = {
                "copd": [
                    f"Leukotriene antagonists show modest benefits in COPD with asthma overlap",
                    f"Clinical trials demonstrate inflammation reduction in {disease_name} patients",
                    f"Mechanistic studies support {disease_name} pathway involvement"
                ],
                "asthma": [
                    f"Well-established efficacy of leukotriene antagonists in asthma",
                    f"Multiple RCTs confirm reduction in asthma exacerbations",
                    f"Strong mechanistic basis for {disease_name} treatment"
                ],
                "diabetes": [
                    f"Evidence suggests {drug_name} may improve glucose metabolism",
                    f"Preclinical studies show benefits in {disease_name} models",
                    f"Limited clinical data available for {disease_name}"
                ],
            }
            
            evidence = evidence_by_disease.get(disease_name.lower(), [
                f"Preclinical studies suggest {drug_name} may benefit {disease_name}",
                f"Mechanistic evidence supports {disease_name} pathway involvement",
                f"Clinical data limited but promising for {disease_name}"
            ])
            
            gaps = [
                f"No large randomized controlled trial of {drug_name} specifically in {disease_name}",
                f"Limited long-term safety data in {disease_name} populations"
            ]
            
            # Return mock JSON with drug/disease-specific content
            return (
                '{'
                f'"summary": "{drug_name} works by {mechanism} which may help reduce {disease_name} symptoms.",'
                f'"steps": ["Bind to disease-relevant receptors", "Reduce inflammatory mediators", "Improve clinical outcomes in {disease_name}"],'
                f'"targets": {json.dumps(targets)},'
                '"confidence": 70,'
                f'"evidence": {json.dumps(evidence)},'
                f'"gaps": {json.dumps(gaps)},'
                '"support_score": 65'
                '}'
            )

        last_exc = None
        delay = 1.0
        for attempt in range(1, max_retries + 1):
            try:
                logger.info("Gemini generate_text attempt=%d", attempt)
                # Use the modern SDK API
                response = genai.GenerativeModel(self.model).generate_content(prompt)
                text = response.text if hasattr(response, 'text') else str(response)
                return text
            except Exception as e:
                last_exc = e
                logger.warning("Gemini error on attempt %d: %s", attempt, e)
                if attempt < max_retries:
                    time.sleep(delay)
                    delay *= 2
        raise RuntimeError("GeminiClient failed after retries") from last_exc
