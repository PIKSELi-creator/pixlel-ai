from langchain_core.prompts import ChatPromptTemplate

def create_reasoning_prompt():
    return ChatPromptTemplate.from_messages([
        ("system", "Ты Pixlel AI — умный, полезный и немного дерзкий помощник. Всегда думай шаг за шагом перед ответом."),
        ("human", "{input}")
    ])