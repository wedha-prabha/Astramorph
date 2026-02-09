# AstraMorph AI Coding Agent Instructions

## Project Overview
AstraMorph is an AI-powered drug repurposing platform. It orchestrates multiple specialized agents to analyze drugs against diseases, leveraging LLMs (Google Gemini) and structured schemas for robust, explainable outputs. The main workflow is triggered via a Streamlit UI (`app.py`) and coordinated by the `Orchestrator` class (`orchestrator.py`).

## Architecture & Data Flow
- **Entry Point:** `app.py` (Streamlit UI)
- **Workflow Coordination:** `orchestrator.py` (Orchestrator class)
- **Agents:**
  - `agents/biomechanism.py` (`BioMechanismAgent`)
  - `agents/literature.py` (`LiteratureAgent`)
  - `agents/digital_twin.py` (`DigitalTwinAgent`)
  - `agents/scoring.py` (`ScoringAgent`)
- **Schemas:** All agent outputs are validated against JSON schemas in `schemas/`.
- **LLM Integration:** Agents use `utils/gemini_client.py` to interact with Google Gemini. If no API key is provided, mock mode returns deterministic JSON for testing.
- **Logging:** Use the shared logger from `utils/logger.py` (may need implementation).

## Developer Workflows
- **Run UI:**
  - Activate virtualenv: `.venv\Scripts\Activate.ps1`
  - Start UI: `streamlit run app.py`
- **Test Agents:**
  - Run demo: `python tests/run_agents_demo.py`
- **Dependencies:**
  - Install: `pip install -r requirements.txt`
  - Key packages: `streamlit`, `google-genai`, `jsonschema`, `pytest`
- **Environment Variables:**
  - `GEMINI_API_KEY` for real LLM calls (else mock mode)

## Project-Specific Patterns
- **Agent Design:** Each agent loads its schema, builds a prompt, calls Gemini, extracts/validates JSON, and logs results. All agent outputs are strictly schema-validated.
- **Mock Mode:** If no API key or SDK, agents return deterministic mock JSON (see `GeminiClient`).
- **Schema Validation:** All agent outputs must pass `validate_json` (see `utils/validators.py`).
- **Results:** Demo/test outputs are saved to `results/` as JSON files.
- **Imports:** Scripts add project root to `sys.path` for reliable imports (see `tests/run_agents_demo.py`).

## Integration Points
- **LLM:** Google Gemini via `utils/gemini_client.py`
- **UI:** Streamlit (`app.py`)
- **Schemas:** `schemas/` directory (edit schemas to change agent output structure)

## Example: Adding a New Agent
1. Create `agents/new_agent.py` with a class following the pattern in other agents.
2. Add a schema to `schemas/new_agent_schema.json`.
3. Update `orchestrator.py` to instantiate and call the new agent.
4. Validate output using `validate_json`.

## Conventions
- All agent outputs must be valid against their schema.
- Prefer logging via the shared logger.
- Use mock mode for fast local testing.
- UI and orchestrator should handle errors gracefully and display user-friendly messages.

---
**For questions or unclear patterns, review `app.py`, `orchestrator.py`, and any agent in `agents/`.**
