# Импортируем необходимые классы из библиотеки aiogram
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

# Импортируем токен бота из конфигурационного файла
from app.config import TOKEN

# Импортируем функцию для регистрации хендлеров (обработчиков)
from app.handlers import register_handlers

# Создаём объект бота с указанным токеном и устанавливаем формат сообщений по умолчанию (HTML)
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

# Создаём объект диспетчера, который будет обрабатывать обновления от Telegram
dp = Dispatcher()

# Функция для регистрации всех хендлеров (обработчиков команд и сообщений)
def register_all_handlers():
    register_handlers(dp)

# Асинхронная функция для запуска бота
async def run_bot():
    # Регистрируем все обработчики
    register_all_handlers()
    
    # Запускаем процесс опроса (polling) для получения обновлений от Telegram
    await dp.start_polling(bot)
