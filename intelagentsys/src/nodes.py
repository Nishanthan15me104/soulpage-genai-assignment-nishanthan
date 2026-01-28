# src/nodes.py
import yfinance as yf
from langchain_groq import ChatGroq
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.messages import SystemMessage, HumanMessage
from src.state import AgentState, CompanyResearchDoc, StockData, NewsItem, AnalystReport
from src.data.mock_db import get_mock_data

from opik import track # NEW IMPORT

import os
from dotenv import load_dotenv

load_dotenv() 

# Initialize Groq (High-speed LPU inference)
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.3)

# --- Tool Helpers ---
def fetch_live_data(company: str):
    """Fetches real-time stock and news data."""
    try:
        # Simple ticker logic: in a real app, use an LLM to find the ticker first
        symbol = "TSLA" if "tesla" in company.lower() else "AAPL"
        stock = yf.Ticker(symbol)
        price = stock.fast_info.last_price
        
        search = DuckDuckGoSearchRun()
        news_text = search.invoke(f"latest business news for {company}")
        
        return {
            "symbol": symbol,
            "price": price,
            "news": news_text[:500] 
        }
    except Exception as e:
        print(f"Tool error: {e}")
        return None

# --- Agent Nodes ---

def supervisor_node(state: AgentState):
    """
    The Orchestrator Logic: 
    Returns the string name of the next node to execute.
    """
    print("--- ⚖️ SUPERVISOR: Routing ---")
    if not state.get("research_data"):
        return "collector"
    if not state.get("final_report"):
        return "analyst"
    return "end"

@track(name="Data Collector Agent") # ADD THIS
def data_collector_node(state: AgentState):
    company = state["company_name"]
    print(f"--- 🕵️‍♂️ COLLECTOR: Gathering for {company} ---")
    
    live = fetch_live_data(company)
    
    if live and live.get("price"):
        research = CompanyResearchDoc(
            company_name=company,
            source="live_api",
            stock_data=StockData(symbol=live["symbol"], current_price=live["price"]),
            latest_news=[NewsItem(title="Live Update", summary=live["news"], source="DDG")]
        )
    else:
        print("⚠️ API Fallback triggered.")
        research = get_mock_data(company)
        
    return {"research_data": research}


@track(name="Analyst Agent") # ADD THIS
def analyst_node(state: AgentState):
    print(f"--- 🧠 ANALYST: Reasoning for {state['company_name']} ---")
    data = state["research_data"]

    # 🔍 DEBUG: show exact context
    print("\n📦 CONTEXT PASSED TO LLM:")
    print(data.model_dump_json(indent=2))
    print("------------------------------------------------\n")

    structured_llm = llm.with_structured_output(AnalystReport)

    prompt = f"""
    You MUST base your analysis only on the provided data.

    Rules:
    - Every risk must reference either stock price or a news item
    - Do NOT introduce external knowledge
    - If data is insufficient, explicitly say so

    DATA:
    {data.model_dump_json(indent=2)}
    """

    report = structured_llm.invoke([
        SystemMessage(content="You are a Financial Analyst. Output valid JSON only."),
        HumanMessage(content=prompt)
    ])

    return {"final_report": report}
