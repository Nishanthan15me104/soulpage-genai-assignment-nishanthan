# test_run.py
import uuid
from dotenv import load_dotenv
from src.graph import app

load_dotenv()

def run_research(company: str):
    # 'thread_id' is required for the MemorySaver to store state
    config = {"configurable": {"thread_id": str(uuid.uuid4())}}
    
    # Start with empty messages and the company name
    initial_state = {
        "company_name": company,
        "messages": []
    }

    print(f"🚀 Starting Research for {company}...")
    
    # We use .stream() to see the nodes fire in real-time
    for event in app.stream(initial_state, config):
        for node_name, state_update in event.items():
            print(f"✔️ Finished Node: {node_name}")

    # Final State Retrieval
    final_state = app.get_state(config).values
    report = final_state.get("final_report")

    if report:
        print("\n" + "="*40)
        print(f"REPORT: {report.company_name}")
        print(f"VERDICT: {report.investment_verdict}")
        print(f"RISKS: {', '.join(report.key_risks)}")
        print("="*40)

if __name__ == "__main__":
    run_research("Tesla")