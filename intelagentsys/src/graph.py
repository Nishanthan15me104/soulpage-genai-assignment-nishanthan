from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from src.state import AgentState
from src.nodes import data_collector_node, analyst_node, supervisor_node

workflow = StateGraph(AgentState)

workflow.add_node("collector", data_collector_node)
workflow.add_node("analyst", analyst_node)

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
