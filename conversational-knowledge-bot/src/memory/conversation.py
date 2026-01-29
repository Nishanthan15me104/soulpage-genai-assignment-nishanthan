from langchain_classic.memory import ConversationBufferMemory

_memory_store = {}

def get_memory(session_id: str):
    if session_id not in _memory_store:
        _memory_store[session_id] = ConversationBufferMemory(
            memory_key="history",
            return_messages=True
        )
    return _memory_store[session_id]
