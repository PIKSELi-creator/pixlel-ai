"""
Pixlel AI - Главный файл запуска
Файл: main.py
Версия: 0.3.0
Описание: Точка входа в приложение Pixlel AI
"""

import os
import sys
import asyncio
import logging
from typing import Optional

# Добавляем путь для импортов
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import config, print_config_info
from src.brain.agent import PixlelAgent, create_pixlel_agent
from src.ui.gradio_app import launch_gradio

# ====================== НАСТРОЙКА ЛОГГИРОВАНИЯ ======================
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format='%(asctime)s | %(levelname)s | %(name)s | %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(f"{config.LOGS_DIR}/pixlel_main.log", encoding="utf-8", mode='a')
    ]
)
logger = logging.getLogger("PixlelMain")


class PixlelApplication:
    """Главный класс приложения Pixlel AI"""

    def __init__(self):
        self.agent: Optional[PixlelAgent] = None
        self.is_running = False
        logger.info("PixlelApplication инициализирован")

    async def initialize(self):
        """Инициализация всего приложения"""
        print_config_info()
        
        logger.info("Запуск инициализации Pixlel AI...")
        
        # Создаём главного агента (мозг)
        self.agent = create_pixlel_agent()
        await self.agent.initialize()
        
        logger.info("✅ Pixlel AI успешно инициализирован!")
        print("🎉 Pixlel AI готов к работе!")

    async def chat_loop(self):
        """Простой консольный чат для тестирования"""
        print("\n" + "="*60)
        print("💬 Pixlel AI — Консольный режим")
        print("Напиши 'выход' или 'exit' для завершения")
        print("="*60 + "\n")

        while True:
            try:
                user_input = input("Ты: ").strip()
                
                if user_input.lower() in ['выход', 'exit', 'quit', 'q']:
                    print("👋 До свидания! Pixlel AI завершает работу...")
                    break
                    
                if not user_input:
                    continue

                print("🧠 Pixlel думает...")
                
                response = await self.agent.chat(user_input)
                
                print(f"\nPixlel: {response}\n")
                
            except KeyboardInterrupt:
                print("\n👋 Программа прервана пользователем.")
                break
            except Exception as e:
                logger.error(f"Ошибка в чате: {e}")
                print("❌ Произошла ошибка. Попробуй ещё раз.")

    def run_console(self):
        """Запуск в консольном режиме"""
        asyncio.run(self.console_mode())

    async def console_mode(self):
        await self.initialize()
        await self.chat_loop()

    def run_web(self):
        """Запуск веб-интерфейса (Gradio)"""
        asyncio.run(self.initialize())
        print(f"🌐 Запуск веб-интерфейса на http://localhost:{config.GRADIO_SERVER_PORT}")
        launch_gradio(self.agent)


def main():
    """Точка входа"""
    app = PixlelApplication()
    
    print(f"\n🚀 Добро пожаловать в {config.PROJECT_NAME} v{config.VERSION}!\n")
    
    mode = input("Выбери режим запуска:\n1. Консоль (1)\n2. Веб-интерфейс (2)\n→ ").strip()
    
    if mode == "1" or mode.lower() == "консоль":
        app.run_console()
    elif mode == "2" or mode.lower() == "веб":
        app.run_web()
    else:
        print("По умолчанию запускаю веб-интерфейс...")
        app.run_web()


# ====================== ЗАПУСК ======================
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.critical(f"Критическая ошибка при запуске: {e}", exc_info=True)
        print("❌ Критическая ошибка. Проверь логи.")
        sys.exit(1)