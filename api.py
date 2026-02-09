from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from orchestrator import Orchestrator
import uvicorn
import os

app = FastAPI(title="AstraMorph API", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalysisRequest(BaseModel):
    drug_name: str
    disease_name: str

@app.post("/analyze")
async def analyze_drug(request: AnalysisRequest):
    try:
        orchestrator = Orchestrator()
        results = orchestrator.run_repurposing_workflow(request.drug_name, request.disease_name)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Serve React Frontend
# Mount the static directory
if os.path.exists("frontend/dist"):
    app.mount("/assets", StaticFiles(directory="frontend/dist/assets"), name="assets")

    @app.get("/{full_path:path}")
    async def serve_react_app(full_path: str):
        # API routes are already handled above
        # Serve index.html for any other route to support client-side routing
        return FileResponse("frontend/dist/index.html")
else:
    print("Warning: frontend/dist not found. Run 'npm run build' in frontend directory.")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
