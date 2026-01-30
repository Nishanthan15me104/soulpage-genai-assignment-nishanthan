"""1. Conversation Orchestration Logic
src/chains/conversation_chain.py

Purpose: Manages the Large Language Model (LLM) configuration and the reasoning prompt. """

from langchain_classic.chains import ConversationChain
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq

from src.config.settings import GROQ_API_KEY, MODEL_NAME, TEMPERATURE
from src.memory.conversation import get_memory
from src.tools.web_search import web_search

# The blueprint for how the LLM should behave and when to trigger a search
PROMPT = PromptTemplate(
    input_variables=["history", "input"],
    template="""
You are a helpful assistant.

Conversation so far:
{history}

User question:
{input}

Rules:
- Use your general knowledge to answer common biographical questions.
- Only say SEARCH_NEEDED if the answer depends on very recent or unknown information.
- Do NOT say SEARCH_NEEDED if the answer can be answered from general knowledge.
"""
)



def get_conversation_chain(session_id: str):
    """
    Initializes and returns a LangChain ConversationChain.
    It configures the Groq LLM, retrieves the specific memory for the session, 
    and applies the custom PromptTemplate.

    Args:
        session_id (str): A unique identifier for the user session to track 
                          their specific chat history.

    Returns:
        ConversationChain: A fully configured LangChain object ready to 
                          process user messages with memory and LLM logic.

    """
    llm = ChatGroq(
        groq_api_key=GROQ_API_KEY,
        model_name=MODEL_NAME,
        temperature=TEMPERATURE
    )

    memory = get_memory(session_id)

    chain = ConversationChain(
        llm=llm,
        memory=memory,
        prompt=PROMPT,
        verbose=True
    )

    return chain
