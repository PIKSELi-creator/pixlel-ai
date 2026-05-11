from langchain_ollama import ChatOllama
from config import OLLAMA_MODEL

def get_llm():
    return ChatOllama(
        model=OLLAMA_MODEL,
        temperature=0.7,
        num_ctx=8192
    )