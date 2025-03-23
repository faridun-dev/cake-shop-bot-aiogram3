from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from app.config import TOKEN
from app.handlers import register_handlers

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

def register_all_handlers():
    register_handlers(dp)

async def run_bot():
    register_all_handlers()
    await dp.start_polling(bot)
