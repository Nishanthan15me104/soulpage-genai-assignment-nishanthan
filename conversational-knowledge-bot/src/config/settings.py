import os
from dotenv import load_dotenv

# Force load .env from project root
load_dotenv(dotenv_path=".env", override=True)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY not found in environment variables")

MODEL_NAME = "llama-3.3-70b-versatile"
TEMPERATURE = 0.3
