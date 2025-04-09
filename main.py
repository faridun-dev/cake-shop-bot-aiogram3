import asyncio  # Импорт модуля для работы с асинхронным кодом
import logging  # Импорт модуля для логирования
from app.bot import run_bot  # Импорт функции запуска бота

# Точка входа в приложение
if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
    )  # Настройка уровня логирования (информация)
    asyncio.run(
        run_bot(),
    )  # Запуск бота в асинхронном режиме
