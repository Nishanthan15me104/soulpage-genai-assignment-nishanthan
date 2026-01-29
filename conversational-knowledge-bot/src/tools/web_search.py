from ddgs import DDGS

def web_search(query: str) -> str:
    with DDGS() as ddgs:
        results = ddgs.text(query, max_results=3)
        return "\n".join(r["body"] for r in results)
