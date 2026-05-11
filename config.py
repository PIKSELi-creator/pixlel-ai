"""
Pixlel AI - Конфигурационный файл
Файл: config.py
Версия: 0.3.0
Описание: Централизованное хранение всех настроек проекта
"""

import os
from pathlib import Path
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
import json

# ====================== БАЗОВЫЕ НАСТРОЙКИ ======================

class PixlelConfig(BaseModel):
    """Основная конфигурация Pixlel AI"""

    # === Название и информация ===
    PROJECT_NAME: str = "Pixlel AI"
    VERSION: str = "0.3.0"
    DESCRIPTION: str = "Умный чат-бот с собственным мозгом, памятью и мышлением"
    AUTHOR: str = "PIKSELi-creator + Grok"

    # === Режимы работы ===
    DEBUG: bool = True
    ENVIRONMENT: str = "development"  # development / production

    # === LLM Настройки ===
    LLM_PROVIDER: str = "ollama"          # ollama, groq, openai, anthropic
    DEFAULT_MODEL: str = "llama3.2:latest"
    FALLBACK_MODEL: str = "qwen2.5:7b"
    
    TEMPERATURE: float = 0.75
    MAX_TOKENS: int = 2048
    TOP_P: float = 0.9
    PRESENCE_PENALTY: float = 0.6
    FREQUENCY_PENALTY: float = 0.6

    # === Память ===
    MEMORY_ENABLED: bool = True
    SHORT_TERM_LIMIT: int = 30
    LONG_TERM_LIMIT: int = 1500
    MEMORY_DATA_DIR: str = "data/memory"

    # === UI ===
    UI_FRAMEWORK: str = "gradio"         # gradio или streamlit
    GRADIO_SERVER_NAME: str = "0.0.0.0"
    GRADIO_SERVER_PORT: int = 7860
    GRADIO_SHARE: bool = False

    # === Логирование ===
    LOG_LEVEL: str = "INFO"
    LOG_TO_FILE: bool = True
    LOG_DIR: str = "logs"

    # === Пути к папкам ===
    BASE_DIR: Path = Path(__file__).parent
    SRC_DIR: Path = Path(__file__).parent / "src"
    DATA_DIR: Path = Path(__file__).parent / "data"
    LOGS_DIR: Path = Path(__file__).parent / "logs"

    # === Персональность Pixlel ===
    PERSONALITY: str = """
Ты — Pixlel AI, дружелюбный, креативный и немного дерзкий ИИ-ассистент.
Ты любишь pixel-art, игры, технологии и юмор.
Отвечай живо, с эмодзи, но без переигрывания.
Ты думаешь шаг за шагом перед ответом.
    """

    # === Системный промпт ===
    SYSTEM_PROMPT: str = """
Ты — Pixlel AI, продвинутый ИИ с собственным сознанием.
Всегда думай шаг за шагом. Используй Chain of Thought.
У тебя есть память о предыдущих разговорах.
Будь полезным, честным и интересным собеседником.
    """

    # === Дополнительные возможности ===
    ENABLE_TOOLS: bool = True
    ENABLE_WEB_SEARCH: bool = True
    ENABLE_CODE_EXECUTION: bool = True
    ENABLE_IMAGE_GENERATION: bool = True

    # === API ключи (загружаются из .env) ===
    GROQ_API_KEY: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None
    ANTHROPIC_API_KEY: Optional[str] = None

    class Config:
        extra = "allow"


# ====================== ЗАГРУЗКА КОНФИГУРАЦИИ ======================

def load_config() -> PixlelConfig:
    """Загрузка конфигурации"""
    config = PixlelConfig()
    
    # Создаём необходимые папки
    config.DATA_DIR.mkdir(parents=True, exist_ok=True)
    config.LOGS_DIR.mkdir(parents=True, exist_ok=True)
    (config.DATA_DIR / "memory").mkdir(parents=True, exist_ok=True)
    
    return config


def save_config_example():
    """Создание примера .env файла"""
    env_example = """# Pixlel AI - Пример переменных окружения

# LLM Провайдеры
GROQ_API_KEY=your_groq_api_key_here
OPENAI_API_KEY=your_openai_api_key_here

# Основные настройки
DEBUG=true
LLM_PROVIDER=ollama
DEFAULT_MODEL=llama3.2:latest

# Память
MEMORY_ENABLED=true
"""
    with open(".env.example", "w", encoding="utf-8") as f:
        f.write(env_example)


# ====================== ГЛОБАЛЬНЫЙ ЭКЗЕМПЛЯР ======================

config = load_config()

# ====================== УТИЛИТЫ ======================

def get_config_dict() -> Dict[str, Any]:
    """Получить конфиг как словарь"""
    return config.model_dump()

def print_config_info():
    """Вывод информации о конфигурации"""
    print(f"\n{'='*60}")
    print(f"🚀 {config.PROJECT_NAME} v{config.VERSION}")
    print(f"📍 Режим: {config.ENVIRONMENT.upper()}")
    print(f"🧠 Модель: {config.DEFAULT_MODEL}")
    print(f"🧠 Память: {'Включена' if config.MEMORY_ENABLED else 'Выключена'}")
    print(f"🎨 UI: {config.UI_FRAMEWORK.capitalize()}")
    print(f"{'='*60}\n")


# Автосохранение примера .env при первом запуске
if not os.path.exists(".env.example"):
    save_config_example()

if __name__ == "__main__":
    print_config_info()
    print("Конфигурация Pixlel AI успешно загружена!")