from langchain_classic.chains import ConversationChain
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq

from src.config.settings import GROQ_API_KEY, MODEL_NAME, TEMPERATURE
from src.memory.conversation import get_memory
from src.tools.web_search import web_search


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
