# Pixlel AI

**Умный чат с собственным "мозгом"** — думает шаг за шагом, имеет память, использует инструменты и рассуждает перед ответом.

## Возможности
- ✨ Chain of Thought + ReAct стиль мышления
- 🧠 Долгосрочная и краткосрочная память
- 🛠 Инструменты (поиск, калькулятор, выполнение кода и др.)
- 🚀 Локальный запуск через Ollama
- 🎨 Красивый Gradio интерфейс

## Быстрый старт

```bash
git clone https://github.com/PIKSELi-creator/pixlel-ai.git
cd pixlel-ai
pip install -r requirements.txt
cp .env.example .env

# Запусти Ollama и скачай модель:
# ollama pull llama3.2

python main.py
```

## Структура проекта
```bash
pixlel-ai/
├── src/
│   ├── brain/          # Главный "мозг" Pixlel
│   ├── models/         # LLM провайдеры
│   ├── ui/             # Интерфейсы (Gradio)
│   └── utils/          # Промпты и утилиты
├── main.py
├── config.py
├── .env.example
└── README.md
```