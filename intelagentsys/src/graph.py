import os
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

# Import your nodes and state
from src.state import AgentState
from src.nodes import data_collector_node, analyst_node, supervisor_node

# --- Opik Integration ---
from opik.integrations.langchain import OpikTracer, track_langgraph

load_dotenv()

# Map your specific key to what Opik expects internally
if os.getenv("COMET_API_KEY"):
    os.environ["OPIK_API_KEY"] = os.getenv("COMET_API_KEY")

if os.getenv("OPIK_PROJECT_NAME"):
    os.environ["OPIK_PROJECT_NAME"] = os.getenv("OPIK_PROJECT_NAME")

# Define the Graph
workflow = StateGraph(AgentState)

workflow.add_node("collector", data_collector_node)
workflow.add_node("analyst", analyst_node)

# Routing Logic
workflow.add_conditional_edges(
    START,
    supervisor_node,
    {"collector": "collector", "analyst": "analyst", "end": END}
)

workflow.add_conditional_edges(
    "collector",
    supervisor_node,
    {"collector": "collector", "analyst": "analyst", "end": END}
)

workflow.add_conditional_edges(
    "analyst",
    supervisor_node,
    {"collector": "collector", "analyst": "analyst", "end": END}
)

memory = MemorySaver()
app = workflow.compile(checkpointer=memory)

# Wrap the app with Opik Tracing
try:
    # We call OpikTracer without arguments because it will read from os.environ
    opik_tracer = OpikTracer() 
    app = track_langgraph(app, opik_tracer)
    print("✅ Opik Monitoring: Successfully linked using COMET_API_KEY")
except Exception as e:
    print(f"⚠️ Opik Notice: Tracing skipped. System is still functional. Error: {e}")