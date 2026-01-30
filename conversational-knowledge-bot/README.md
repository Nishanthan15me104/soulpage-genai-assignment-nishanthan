# 🤖 Conversational Knowledge Bot

A conversational AI assistant built with **FastAPI**, **LangChain Groq**, and **Streamlit**, capable of remembering conversation context per session and performing web searches when needed.

---


## project strucutre

```
conversational-knowledge-bot/
│
├── src/                         # Core backend logic (pure Python)
│   ├── chains/
│   │   └── conversation_chain.py
│   │
│   ├── config/
│   │   └── settings.py
│   │
│   └── memory/
│       └── conversation.py
│
├── api/
│   └── chat_api.py              # FastAPI entry point
│
├── streamlit_app.py             # Streamlit UI (renamed from app.py)
│
├── requirements.txt
├── README.md
├── .env
└── .gitignore
```

## 🏗️ Architecture Overview



**Flow:**

1. User types a question in the **Streamlit UI**.
2. Request is sent to **FastAPI** (`/chat`) with a `session_id`.
3. FastAPI calls `get_conversation_chain(session_id)`:
   - Uses **LangChain Groq** as LLM.
   - Uses **ConversationBufferMemory** to remember session context.
4. If the LLM response includes `SEARCH_NEEDED`, a web search is triggered via **DDGS** and the result is fed back to the LLM.
5. The final response is returned to **Streamlit** and displayed.

---

## 🛠️ Tools & Libraries

- **FastAPI** – Backend API server.
- **Streamlit** – Frontend chat interface.
- **LangChain (Classic & Groq)** – For memory-enabled conversational chains.
- **Groq Chat API** – Large language model.
- **DDGS (DuckDuckGo Search)** – Lightweight web search.
- **Pydantic** – Data validation for API requests.

---

## 💾 Memory Design

We use **per-session memory** with `ConversationBufferMemory`:

- **_memory_store**: a dictionary storing memory for each `session_id`.
- Memory retains conversation history (`return_messages=True`) for context-aware replies.
- New sessions automatically initialize empty memory.


## setup instruction

```
git clone https://github.com/Nishanthan15me104/soulpage-genai-assignment-nishanthan.git
cd conversational-knowledge-bot

python -m venv venv
# Windows
venv\Scripts\activate
# Linux / Mac
source venv/bin/activate

pip install -r requirements.txt
```

### Configure environment

- Set Groq API key and model in src/config/settings.py:

### Run FatAPI

```
uvicorn api.chat_api:app --reload
```
API will be available at: http://localhost:8000/chat

### Run Streamlit UI
```
streamlit run streamlit_app.py
```
- Access the chat interface at: http://localhost:8501

## Example Usage screenshot

![RAG Query Results](img\sampleconvo.png)
