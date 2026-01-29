from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

from src.chains.conversation_chain import get_conversation_chain
from src.tools.web_search import web_search

app = FastAPI()

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = "default"


@app.post("/chat")
def chat(req: ChatRequest):
    chain = get_conversation_chain(req.session_id)

    response = chain.predict(input=req.message)

    # Simple tool trigger (stable & explicit)
    if "SEARCH_NEEDED" in response:
        search_result = web_search(req.message)
        response = chain.predict(
            input=f"Here is the search result:\n{search_result}"
        )

    return {"response": response}
