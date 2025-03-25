from aiogram import Dispatcher, html
from presentation import keyboards as kb
from presentation.messages import START_MESSAGE
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from app.config import cakes, T_BANK_PHOTO_URL
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters.state import StateFilter
from random import randint


class OrderCakeState(StatesGroup):
    waiting_for_quantity = State()


async def command_start_handler(message: Message):
    await message.answer(START_MESSAGE, reply_markup=kb.start)

async def list_menu_callback(callback: CallbackQuery):
    await callback.message.edit_text("Вот наш ассортимент кондитерских изделий:", reply_markup=await kb.list_menu())

async def paginate_menu_callback(callback: CallbackQuery):
    page = int(callback.data.split("_")[-1])
    await callback.message.edit_text("Вот наш ассортимент кондитерских изделий:", reply_markup=await kb.list_menu(page))

async def view_cake_callback(callback: CallbackQuery):
    cake_index = int(callback.data.split("_")[-1])
    cake = cakes[cake_index]
    await callback.message.edit_text(f"{html.bold("Название")}: {cake["name"]}\n{html.bold(f"Цена за {cake["per"]}:")} {cake["price"]} руб", reply_markup=await kb.view_cake(cake_index))

async def back_to_start_callback(callback: CallbackQuery):
    await callback.message.edit_text(START_MESSAGE , reply_markup=kb.start)

async def order_cake_callback(callback: CallbackQuery, state: FSMContext):
    cake_index = int(callback.data.split("_")[-1])
    cake = cakes[cake_index]

    await state.update_data(cake_index=cake_index)

    if cake["per"] == "шт":
        await callback.message.answer("Укажите количество (шт):")
    else:
        await callback.message.answer("Укажите массу (кг):")

    await state.set_state(OrderCakeState.waiting_for_quantity)


async def process_quantity(message: Message, state: FSMContext):
    user_data = await state.get_data()
    cake_index = user_data.get("cake_index")

    cake = cakes[cake_index]

    try:
        quantity = float(message.text)
        if quantity <= 0:
            raise ValueError
    except ValueError:
        await message.answer("Пожалуйста, введите корректное число.")
        return

    cake_name = cake["name"]
    price = cake["price"]
    total_price = quantity * price
    description = (f"{html.bold('Ваш заказ:')}\n"
                   f"{html.bold('Название')}: {cake_name}\n"
                   f"{html.bold(f'Цена за {cake['per']}')}: {price} руб\n"
                   f"{html.bold('Количество')}: {quantity} {cake['per']}\n\n"
                   f"{html.bold('Общая стоимость')}: {total_price} руб\n\n"
                   f"{html.bold(f"Переведите общую стоимость на указанный номер с комментарием ID {randint(10000, 99999)}:")} +79017150031 - Т-Банк 🟡⚫")

    await message.answer_photo(T_BANK_PHOTO_URL, description)

    await state.clear() 

        

def register_handlers(dp: Dispatcher):
    dp.message.register(command_start_handler, CommandStart())
    dp.callback_query.register(list_menu_callback, lambda c : c.data == "list_menu")
    dp.callback_query.register(back_to_start_callback, lambda c: c.data == "back_to_start")
    dp.callback_query.register(paginate_menu_callback, lambda c: c.data.startswith("menu_page_"))
    dp.callback_query.register(view_cake_callback, lambda c: c.data.startswith("view_cake_"))
    dp.callback_query.register(order_cake_callback, lambda c: c.data.startswith("order_cake_"))

    dp.message.register(process_quantity, StateFilter(OrderCakeState.waiting_for_quantity))