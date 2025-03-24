from aiogram import Dispatcher
from presentation import keyboards as kb
from presentation.messages import START_MESSAGE
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

async def command_start_handler(message: Message):
    await message.answer(START_MESSAGE, reply_markup=kb.start)

async def list_menu_callback(callback: CallbackQuery):
    await callback.message.edit_text("Вот наш ассортимент кондитерских изделий:", reply_markup=await kb.list_menu())

async def paginate_menu(callback: CallbackQuery):
    page = int(callback.data.split("_")[-1])
    await callback.message.edit_reply_markup(reply_markup=await kb.list_menu(page))

async def back_to_start_callback(callback: CallbackQuery):
    await callback.message.edit_text(START_MESSAGE , reply_markup=kb.start)

def register_handlers(dp: Dispatcher):
    dp.message.register(command_start_handler, CommandStart())
    dp.callback_query.register(list_menu_callback, lambda c : c.data == "list_menu")
    dp.callback_query.register(back_to_start_callback, lambda c: c.data == "back_to_start")
    dp.callback_query.register(paginate_menu, lambda c: c.data.startswith("menu_page_"))