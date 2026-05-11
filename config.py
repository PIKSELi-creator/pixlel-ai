import os
from dotenv import load_dotenv

load_dotenv()

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")
TEMPERATURE = 0.7
MAX_TOKENS = 2048