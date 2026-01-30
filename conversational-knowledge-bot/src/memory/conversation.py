"""2. Stateful Memory Management
src/memory/conversation.py

Purpose: Provides a centralized store for managing chat history across multiple users."""

from langchain_classic.memory import ConversationBufferMemory

_memory_store = {}

def get_memory(session_id: str):
    """
    Retrieves the conversation history for a specific session.
    If a session_id is new, it creates a new ConversationBufferMemory object; 
    otherwise, it returns the existing one to maintain context.

    Args:
        session_id (str): The unique ID linked to a specific chat window or user.

    Returns:
        ConversationBufferMemory: The memory object containing the 
                                   history of messages for that session.
    """
    if session_id not in _memory_store:
        _memory_store[session_id] = ConversationBufferMemory(
            memory_key="history",
            return_messages=True
        )
    return _memory_store[session_id]
