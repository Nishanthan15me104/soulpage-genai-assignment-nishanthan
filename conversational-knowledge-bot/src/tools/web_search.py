"""3. Web Research Utility
src/tools/web_search.py

Purpose: Interface for external data retrieval when the LLM lacks specific real-time facts."""

from ddgs import DDGS

def web_search(query: str) -> str:
    """
    Performs a live web search using DuckDuckGo.
    
    Args:
        query (str): The search term or question provided by the user.
        
    Returns:
        str: A concatenated string containing the 'body' text of the 
             top 3 search results, used to provide context to the LLM.
    """
    with DDGS() as ddgs:
        results = ddgs.text(query, max_results=3)
        return "\n".join(r["body"] for r in results)
