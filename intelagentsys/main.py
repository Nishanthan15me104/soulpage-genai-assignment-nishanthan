from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.graph import app as workflow_app
import uuid
import logging

# Optional: Ensure Opik logs are quiet so they don't clutter your terminal
logging.basicConfig(level=logging.INFO)

server = FastAPI(title="Agentic Company Intelligence API")

# --- Data Models ---
class ResearchRequest(BaseModel):
    company_name: str
    thread_id: str = None

class ResearchResponse(BaseModel):
    company_name: str
    verdict: str
    summary: str
    risks: list[str]
    thread_id: str

# --- Main Agent Endpoint ---
@server.post("/research", response_model=ResearchResponse)
async def run_agentic_research(request: ResearchRequest):
    thread_id = request.thread_id or str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}
    
    initial_state = {
        "company_name": request.company_name,
        "messages": []
    }

    try:
        # The workflow_app is already wrapped with Opik in src/graph.py
        # invoke() will automatically trigger the monitoring trace
        final_state = workflow_app.invoke(initial_state, config)
        
        report = final_state.get("final_report")
        
        if not report:
            # This triggers the Pydantic-based error response in FastAPI
            raise HTTPException(status_code=500, detail="Agent failed to generate report")
            
        return ResearchResponse(
            company_name=report.company_name,
            verdict=report.investment_verdict,
            summary=report.summary,
            risks=report.key_risks,
            thread_id=thread_id
        )
        
    except Exception as e:
        # Gathers any execution error and sends it back to the UI cleanly
        print(f"!!! Error during research flow: {e}")
        raise HTTPException(status_code=500, detail=f"Research failed: {str(e)}")

# --- NEW: Health Check / Home Route ---
# This fixes the "404 Not Found" error when you open the URL in a browser
@server.get("/")
def read_root():
    return {"status": "Active", "message": "Agentic API is running. Use the Streamlit UI to interact."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(server, host="0.0.0.0", port=8000)