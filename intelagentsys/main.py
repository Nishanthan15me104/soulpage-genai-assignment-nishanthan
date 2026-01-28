from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.graph import app as workflow_app  # rename to avoid conflict
import uuid

server = FastAPI(title="Agentic Company Intelligence API")  # FastAPI instance

class ResearchRequest(BaseModel):
    company_name: str
    thread_id: str = None

class ResearchResponse(BaseModel):
    company_name: str
    verdict: str
    summary: str
    risks: list[str]
    thread_id: str

@server.post("/research", response_model=ResearchResponse)
async def run_agentic_research(request: ResearchRequest):
    thread_id = request.thread_id or str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}
    
    initial_state = {
        "company_name": request.company_name,
        "messages": []
    }

    try:
        final_state = workflow_app.invoke(initial_state, config)  # use workflow_app
        report = final_state.get("final_report")
        
        if not report:
            raise HTTPException(status_code=500, detail="Agent failed to generate report")
            
        return ResearchResponse(
            company_name=report.company_name,
            verdict=report.investment_verdict,
            summary=report.summary,
            risks=report.key_risks,
            thread_id=thread_id
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(server, host="0.0.0.0", port=8000)
