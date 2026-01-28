# streamlit_ui.py
import streamlit as st
import requests
import uuid

# --- Configuration ---
# Ensure this matches the port in your main.py (default 8000)
API_URL = "http://localhost:8000/research"

st.set_page_config(
    page_title="Agentic Research Hub",
    page_icon="🕵️‍♂️",
    layout="wide"
)

# --- Session State ---
# We store the thread_id to maintain "Memory" context within the same user session
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

if "last_report" not in st.session_state:
    st.session_state.last_report = None

# --- UI Layout ---
st.title("🕵️‍♂️ Agentic Company Intelligence")
st.markdown("""
Gathering real-time stock data and business news using a **Multi-Agent LangGraph workflow** powered by **Groq**.
""")

# Sidebar for inputs
with st.sidebar:
    st.header("Search Parameters")
    company_name = st.text_input("Enter Company Name", placeholder="e.g. Tesla, Microsoft, Apple")
    
    analyze_btn = st.button("Run Research Agent", type="primary", use_container_width=True)
    
    st.divider()
    st.info(f"**Session Memory Active**\nThread ID: `{st.session_state.thread_id}`")
    st.caption("Using ephemeral MemorySaver. Memory resets if FastAPI server restarts.")

# --- Execution Logic ---
if analyze_btn:
    if not company_name:
        st.warning("Please enter a company name first.")
    else:
        with st.spinner(f"🚀 Specialist Agents are working on {company_name}..."):
            try:
                payload = {
                    "company_name": company_name,
                    "thread_id": st.session_state.thread_id
                }
                # Call our FastAPI backend
                response = requests.post(API_URL, json=payload, timeout=60)
                
                if response.status_code == 200:
                    st.session_state.last_report = response.json()
                    st.toast("Analysis Complete!", icon="✅")
                else:
                    st.error(f"Agent Error ({response.status_code}): {response.text}")
            except Exception as e:
                st.error(f"Connection Failed: Is your FastAPI (main.py) server running? \n\nError: {e}")

# --- Display Results ---
if st.session_state.last_report:
    report = st.session_state.last_report
    
    st.divider()
    
    # Header Row with Metric
    col1, col2 = st.columns([3, 1])
    with col1:
        st.subheader(f"Financial Intelligence Report: {report['company_name']}")
    with col2:
        verdict = report['verdict'].upper()
        # Visual color coding for the verdict
        if "BUY" in verdict:
            st.success(f"🎯 **VERDICT: {verdict}**")
        elif "SELL" in verdict:
            st.error(f"🚨 **VERDICT: {verdict}**")
        else:
            st.warning(f"⚖️ **VERDICT: {verdict}**")

    # Layout for Details
    tab1, tab2 = st.tabs(["📝 Executive Summary", "⚠️ Risk Assessment"])
    
    with tab1:
        st.markdown("### Summary")
        st.write(report['summary'])
    
    with tab2:
        st.markdown("### Critical Risks")
        for risk in report['risks']:
            st.markdown(f"- {risk}")
            
    # Metadata footer
    st.caption(f"Report generated for thread: {report['thread_id']}")