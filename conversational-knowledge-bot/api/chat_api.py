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
    """
    The main API endpoint for chatting.
    1. It fetches the conversation chain for the session.
    2. It asks the LLM for a response.
    3. If the LLM responds with 'SEARCH_NEEDED', it triggers a web search and 
       feeds that data back to the LLM for a final, informed answer.

    Args:
        req (ChatRequest): A Pydantic model containing the 'message' string 
                           and the optional 'session_id'.

    Returns:
        dict: A dictionary containing the final string "response" to be 
              displayed in the UI.
    """
    chain = get_conversation_chain(req.session_id)

    response = chain.predict(input=req.message)

    # Simple tool trigger (stable & explicit)
    if "SEARCH_NEEDED" in response:
        search_result = web_search(req.message)
        response = chain.predict(
            input=f"Here is the search result:\n{search_result}"
        )

    return {"response": response}
