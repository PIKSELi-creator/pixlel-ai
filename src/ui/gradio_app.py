"""
Pixlel AI - Продвинутый Gradio Интерфейс
Файл: src/ui/gradio_app.py
Версия: 0.4.0
Описание: Очень большой и функциональный веб-интерфейс Pixlel AI
"""

import gradio as gr
import asyncio
import time
import json
import os
import logging
from datetime import datetime
from typing import List, Dict, Optional, Any, Tuple

# ====================== ИМПОРТЫ ======================
from config import config
try:
    from src.brain.agent import PixlelAgent
    from src.brain.memory import PixlelMemory
except ImportError:
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    from src.brain.agent import PixlelAgent
    from src.brain.memory import PixlelMemory

# ====================== ЛОГГИРОВАНИЕ ======================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(name)s | %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("logs/gradio_ui.log", encoding="utf-8", mode='a')
    ]
)
logger = logging.getLogger("PixlelGradio")

# Глобальные переменные
agent: Optional[PixlelAgent] = None
memory: Optional[PixlelMemory] = None
chat_history: List = []
current_mode = "normal"

# ====================== ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ======================

def get_current_time() -> str:
    return datetime.now().strftime("%H:%M:%S")


async def initialize_system():
    """Инициализация всех компонентов"""
    global agent, memory
    if agent is None:
        from src.brain.agent import create_pixlel_agent
        agent = create_pixlel_agent()
        await agent.initialize()
    
    if memory is None:
        memory = PixlelMemory()
    logger.info("Pixlel AI система полностью инициализирована")


def format_thoughts_html(thoughts: List) -> str:
    """Красивое HTML отображение процесса мышления"""
    if not thoughts:
        return "<p>🧠 Pixlel думает...</p>"
    
    html = "<div style='background:#1a1a2e; padding:15px; border-radius:10px; margin:10px 0;'>"
    html += "<h4 style='color:#00ffcc;'>🧠 Процесс мышления Pixlel</h4><br>"
    
    for thought in thoughts:
        html += f"""
        <div style='margin-bottom:12px; padding:10px; background:#16213e; border-radius:8px;'>
            <strong>Шаг {thought.step} — {thought.title}</strong><br>
            <span style='color:#a0a0a0;'>{thought.content}</span>
        </div>
        """
    html += "</div>"
    return html


async def respond(message: str, history: List, mode: str = "normal"):
    """Основная функция ответа"""
    global current_mode
    current_mode = mode
    
    if not message or not message.strip():
        return history, "Напиши что-нибудь :)"

    await initialize_system()

    try:
        # Добавляем сообщение пользователя
        history = history + [[message, None]]
        yield history, "<p>🧠 Pixlel активировал мозг...</p>"

        # Получаем ответ от агента
        response = await agent.think(message)
        
        final_answer = response.final_answer
        thoughts = getattr(response, 'thoughts', [])

        # Сохраняем в память
        if memory:
            memory.add(message, final_answer)

        # Обновляем историю
        history[-1][1] = final_answer

        # Показываем процесс мышления
        thoughts_html = format_thoughts_html(thoughts)

        yield history, thoughts_html

    except Exception as e:
        logger.error(f"Ошибка: {e}")
        history[-1][1] = f"❌ Ошибка: {str(e)}"
        yield history, f"<p style='color:red'>Произошла ошибка: {str(e)}</p>"


def clear_chat():
    """Очистка чата"""
    global chat_history
    chat_history = []
    return [], "<p>✅ Чат очищен</p>"


def load_memory_stats():
    """Статистика памяти"""
    if memory:
        stats = memory.get_stats()
        return f"""
        **Всего записей:** {stats.get('long_term', 0)}<br>
        **Сессий:** {stats.get('sessions', 0)}<br>
        **В короткой памяти:** {stats.get('short_term', 0)}
        """
    return "Память не инициализирована"


# ====================== GRADIO ИНТЕРФЕЙС ======================

with gr.Blocks(
    title="Pixlel AI",
    theme=gr.themes.Dark(),
    css="""
    body {font-family: 'Segoe UI', sans-serif;}
    .chatbot {height: 65vh !important; border-radius: 15px;}
    .message-user {background: #2a2a4a !important;}
    .message-bot {background: #1f2a44 !important;}
    h1 {text-align: center; color: #00ffcc;}
    """
) as demo:

    gr.HTML("""
    <h1 style='margin-bottom:0;'>🎨 Pixlel AI</h1>
    <p style='text-align:center; color:#888;'>Умный ИИ с собственным мозгом и памятью</p>
    """)

    with gr.Tabs():
        
        # ====================== TAB 1: ЧАТ ======================
        with gr.Tab("💬 Основной чат"):
            with gr.Row():
                with gr.Column(scale=7):
                    chatbot = gr.Chatbot(
                        height=580,
                        label="Разговор с Pixlel",
                        show_copy_button=True,
                        bubble_full_width=False
                    )
                    msg = gr.Textbox(
                        placeholder="Напиши сообщение Pixlel...",
                        label="Сообщение",
                        lines=3,
                        container=False
                    )
                
                with gr.Column(scale=3):
                    gr.Markdown("### ⚙️ Настройки")
                    
                    mode_selector = gr.Radio(
                        choices=["Обычный", "Креативный 🔥", "Логический 🧠", "Pixel-арт 🎨"],
                        value="Обычный",
                        label="Режим Pixlel"
                    )
                    
                    with gr.Group():
                        submit = gr.Button("Отправить", variant="primary", size="large")
                        clear = gr.Button("🗑️ Очистить чат", variant="secondary")
                    
                    gr.Markdown("---")
                    memory_status = gr.Markdown(value=load_memory_stats(), label="Память")
                    
                    refresh_memory = gr.Button("Обновить статистику")

        # ====================== TAB 2: МЫШЛЕНИЕ ======================
        with gr.Tab("🧠 Процесс мышления"):
            thought_display = gr.HTML(
                value="<p>Здесь будет отображаться подробный процесс мышления Pixlel</p>",
                label="Подробное мышление"
            )
            gr.Markdown("Pixlel всегда показывает, как он думает шаг за шагом.")

        # ====================== TAB 3: ПАМЯТЬ ======================
        with gr.Tab("📚 Память"):
            with gr.Row():
                search_query = gr.Textbox(label="Поиск в памяти", placeholder="Что ищем?")
                search_btn = gr.Button("🔍 Искать")
            
            memory_output = gr.Textbox(
                label="Результаты поиска",
                lines=15,
                interactive=False
            )

        # ====================== TAB 4: НАСТРОЙКИ ======================
        with gr.Tab("⚙️ Настройки"):
            with gr.Group():
                gr.Markdown("### Модель и параметры")
                model_name = gr.Dropdown(
                    choices=["llama3.2:latest", "qwen2.5:7b", "mistral"],
                    value=config.DEFAULT_MODEL,
                    label="Модель LLM"
                )
                temperature = gr.Slider(0.0, 1.0, value=config.TEMPERATURE, label="Креативность (Temperature)")
            
            with gr.Group():
                gr.Markdown("### Персональность")
                personality_text = gr.Textbox(
                    value=config.PERSONALITY,
                    label="Описание характера Pixlel",
                    lines=6
                )

    # ====================== ПРИМЕРЫ ======================
    gr.Examples(
        examples=[
            ["Привет! Расскажи о себе"],
            ["Нарисуй в голове pixel-art воина"],
            ["Расскажи шутку про программистов"],
            ["Какой сегодня день? Что интересного происходит?"],
            ["Помоги написать код для простой игры"],
        ],
        inputs=msg,
        label="Примеры запросов"
    )

    gr.Markdown("---\n**Pixlel AI v0.4.0** • Сделано с душой и большим количеством строк кода ❤️")

    # ====================== СОБЫТИЯ ======================
    submit.click(
        fn=respond,
        inputs=[msg, chatbot, mode_selector],
        outputs=[chatbot, thought_display]
    ).then(lambda: "", None, msg)

    msg.submit(
        fn=respond,
        inputs=[msg, chatbot, mode_selector],
        outputs=[chatbot, thought_display]
    ).then(lambda: "", None, msg)

    clear.click(
        fn=clear_chat,
        inputs=None,
        outputs=[chatbot, thought_display]
    )

    refresh_memory.click(
        fn=load_memory_stats,
        inputs=None,
        outputs=memory_status
    )

    # Запуск
    def launch_interface():
        print(f"\n🌐 Pixlel AI запущен на http://127.0.0.1:{config.GRADIO_SERVER_PORT}")
        print("Нажми Ctrl+C для остановки\n")
        demo.launch(
            server_name=config.GRADIO_SERVER_NAME,
            server_port=config.GRADIO_SERVER_PORT,
            share=False,
            show_api=False
        )


if __name__ == "__main__":
    asyncio.run(initialize_system())
    launch_interface()