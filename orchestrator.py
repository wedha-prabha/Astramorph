# orchestrator.py
from typing import Dict, Any
import os

from agents.biomechanism import BioMechanismAgent
from agents.literature import LiteratureAgent
from agents.digital_twin import DigitalTwinAgent
from agents.scoring import compute_score
from utils.logger import logger

# -------------------------------------------------------------------
# Hard-coded Gemini API key for hackathon demo
# (Replace this string with your real key)
# -------------------------------------------------------------------
from dotenv import load_dotenv
load_dotenv()

# -------------------------------------------------------------------
# Load Gemini API key from environment variables
# -------------------------------------------------------------------
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


class Orchestrator:
    """
    Orchestrates the full AstraMorph workflow:
      1. BioMechanism analysis
      2. Literature synthesis
      3. Digital twin simulation
      4. Final scoring / verdict
    """

    def __init__(self) -> None:
        # Make sure downstream code sees the key in env as well
        if GEMINI_API_KEY:
            os.environ["GEMINI_API_KEY"] = GEMINI_API_KEY

        logger.info("Initializing AstraMorph agents...")
        self.mechanism_agent = BioMechanismAgent(api_key=GEMINI_API_KEY)
        self.literature_agent = LiteratureAgent(api_key=GEMINI_API_KEY)
        self.digital_twin_agent = DigitalTwinAgent()
        logger.info("Agents initialized")

    def run_repurposing_workflow(self, drug: str, disease: str) -> Dict[str, Any]:
        """
        Run the full pipeline and return a dictionary with:
          - mechanism
          - literature
          - simulation
          - score
        """
        logger.info("Workflow started for drug=%s disease=%s", drug, disease)

        # 1. Mechanism agent
        mech = self.mechanism_agent.run(drug, disease)
        logger.info("Mechanism agent finished.")

        # 2. Literature agent
        lit = self.literature_agent.run(drug, disease)
        logger.info("Literature agent finished.")

        # 3. Digital twin agent
        sim = self.digital_twin_agent.run(drug, disease)
        logger.info("Digital twin simulation finished.")

        # 4. Scoring
        score = compute_score(mech, lit, sim)
        logger.info("Scoring finished.")

        logger.info("Workflow completed for drug=%s disease=%s", drug, disease)

        return {
            "mechanism": mech,
            "literature": lit,
            "simulation": sim,
            "score": score,
        }
# orchestrator.py
from typing import Dict, Any
import os

from agents.biomechanism import BioMechanismAgent
from agents.literature import LiteratureAgent
from agents.digital_twin import DigitalTwinAgent
from agents.scoring import compute_score
from utils.logger import logger

# -------------------------------------------------------------------
# Hard-coded Gemini API key for hackathon demo
# (Replace this string with your real key)
# -------------------------------------------------------------------
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY_HERE"


class Orchestrator:
    """
    Orchestrates the full AstraMorph workflow:
      1. BioMechanism analysis
      2. Literature synthesis
      3. Digital twin simulation
      4. Final scoring / verdict
    """

    def __init__(self) -> None:
        # Make sure downstream code sees the key in env as well
        if GEMINI_API_KEY:
            os.environ["GEMINI_API_KEY"] = GEMINI_API_KEY

        logger.info("Initializing AstraMorph agents...")
        self.mechanism_agent = BioMechanismAgent(api_key=GEMINI_API_KEY)
        self.literature_agent = LiteratureAgent(api_key=GEMINI_API_KEY)
        self.digital_twin_agent = DigitalTwinAgent()
        logger.info("Agents initialized")

    def run_repurposing_workflow(self, drug: str, disease: str) -> Dict[str, Any]:
        """
        Run the full pipeline and return a dictionary with:
          - mechanism
          - literature
          - simulation
          - score
        """
        logger.info("Workflow started for drug=%s disease=%s", drug, disease)

        # 1. Mechanism agent
        mech = self.mechanism_agent.run(drug, disease)
        logger.info("Mechanism agent finished.")

        # 2. Literature agent
        lit = self.literature_agent.run(drug, disease)
        logger.info("Literature agent finished.")

        # 3. Digital twin agent
        sim = self.digital_twin_agent.run(drug, disease)
        logger.info("Digital twin simulation finished.")

        # 4. Scoring
        score = compute_score(mech, lit, sim)
        logger.info("Scoring finished.")

        logger.info("Workflow completed for drug=%s disease=%s", drug, disease)

        return {
            "mechanism": mech,
            "literature": lit,
            "simulation": sim,
            "score": score,
        }
