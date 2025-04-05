# Импортируем модуль для работы с базой данных SQLite
import sqlite3

# Импортируем необходимые компоненты из aiogram
from aiogram import Dispatcher, html, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters.state import StateFilter

# Импортируем клавиатуры и сообщения из папки presentation
from presentation import keyboards as kb
from presentation.messages import START_MESSAGE

# Импортируем данные из конфигурации
from app.config import cakes, T_BANK_PHOTO_URL, ADMIN_CHAT_ID, TOKEN

# Импортируем модуль для работы с базой данных
from infrastructure.database import BotDatabase

# Импортируем функцию для генерации случайного ID заказа
from random import randint


# Класс состояний для FSM (машины состояний), используемый при заказе торта
class OrderCakeState(StatesGroup):
    waiting_for_quantity = State()  # Ожидание ввода количества от пользователя


# Обработчик команды /start
async def command_start_handler(message: Message):
    await message.answer(START_MESSAGE, reply_markup=kb.start)


# Обработчик кнопки "Ассортимент"
async def list_menu_callback(callback: CallbackQuery):
    await callback.message.edit_text("Вот наш ассортимент кондитерских изделий:", reply_markup=await kb.list_menu())


# Обработчик кнопки пагинации
async def paginate_menu_callback(callback: CallbackQuery):
    page = int(callback.data.split("_")[-1])
    await callback.message.edit_text("Вот наш ассортимент кондитерских изделий:", reply_markup=await kb.list_menu(page))


# Обработчик просмотра конкретного торта
async def view_cake_callback(callback: CallbackQuery):
    cake_index = int(callback.data.split("_")[-1])
    cake = cakes[cake_index]
    await callback.message.edit_text(
        f"{html.bold('Название')}: {cake['name']}\n{html.bold(f'Цена за {cake['per']}')}: {cake['price']} руб",
        reply_markup=await kb.view_cake(cake_index)
    )


# Обработчик возврата к главному меню
async def back_to_start_callback(callback: CallbackQuery):
    await callback.message.edit_text(START_MESSAGE , reply_markup=kb.start)


# Обработчик кнопки "Не оплачен" — меняет статус заказа на не оплачено
async def order_unpaid_callback(callback: CallbackQuery):
    db = BotDatabase()
    order_id = int(callback.data[-5:])

    db.update_order_status(order_id, False)  # Обновляем статус в базе

    new_status = False 
    await callback.message.edit_reply_markup(reply_markup=await kb.order_status(new_status, order_id))


# Обработчик кнопки "Оплачен" — меняет статус заказа на оплачен
async def order_paid_callback(callback: CallbackQuery):
    db = BotDatabase()
    order_id = int(callback.data[-5:])

    db.update_order_status(order_id, True)

    new_status = True 
    await callback.message.edit_reply_markup(reply_markup=await kb.order_status(new_status, order_id))


# Обработчик начала заказа (после нажатия "Заказать")
async def order_cake_callback(callback: CallbackQuery, state: FSMContext):
    cake_index = int(callback.data.split("_")[-1])
    cake = cakes[cake_index]

    # Сохраняем индекс выбранного торта в состоянии FSM
    await state.update_data(cake_index=cake_index)

    # Просим ввести количество в зависимости от единицы измерения
    if cake["per"] == "шт":
        await callback.message.answer("Укажите количество (шт):")
    else:
        await callback.message.answer("Укажите массу (кг):")

    # Устанавливаем состояние — ожидание количества
    await state.set_state(OrderCakeState.waiting_for_quantity)


# Инициализируем объект бота
bot = Bot(token=TOKEN)


# Обработчик ввода количества пользователем
async def process_quantity(message: Message, state: FSMContext):
    db = BotDatabase()
    user_data = await state.get_data()
    cake_index = user_data.get("cake_index")
    cake = cakes[cake_index]

    # Проверка корректности введённого числа
    try:
        quantity = float(message.text)
        if quantity <= 0:
            raise ValueError
    except ValueError:
        await message.answer("Пожалуйста, введите корректное число.")
        return

    # Подсчёт итоговой стоимости заказа
    cake_name = cake["name"]
    price = cake["price"]
    total_price = quantity * price

    # Генерация уникального ID заказа
    while True: 
        order_id = randint(10000, 99999)
        try:
            db.add_order((order_id, f"{message.from_user.full_name}", cake_name, int(quantity), total_price, False))
            break  # Если ID уникальный — выходим из цикла
        except sqlite3.IntegrityError:
            continue  # Иначе пробуем заново

    # Сообщение пользователю с реквизитами оплаты
    description = (
        f"🛒 {html.bold('Ваш заказ:')}\n"
        f"📦 {html.bold('Название')}: {cake_name}\n"
        f"💰 {html.bold(f'Цена за {cake['per']}')}: {price} руб\n"
        f"📏 {html.bold('Количество')}: {quantity} {cake['per']}\n\n"
        f"💵 {html.bold('Общая стоимость')}: {total_price} руб\n\n"
        f"{html.bold(f'Переведите общую стоимость на указанный номер с комментарием 🆔 {order_id}:')} +79017150031 - Т-Банк 🟡⚫"
    )

    await message.answer_photo(T_BANK_PHOTO_URL, description)

    # Уведомление администратору о новом заказе
    admin_message = (
        f"🛒 *Новый заказ!*\n\n"
        f"👤 *Пользователь*: [{message.from_user.full_name}](tg://user?id={message.from_user.id})\n"
        f"📦 *Название*: {cake_name}\n"
        f"💰 *Цена за {cake['per']}*: {price} руб\n"
        f"📏 *Количество*: {quantity} {cake['per']}\n"
        f"💵 *Общая стоимость*: {total_price} руб\n"
        f"🆔 *ID заказа*: {order_id}"
    )

    await bot.send_message(
        ADMIN_CHAT_ID,
        admin_message,
        parse_mode="Markdown",
        reply_markup=await kb.order_status(False, order_id)
    )

    # Очищаем состояние
    await state.clear()


# Регистрация всех хендлеров в диспетчере
def register_handlers(dp: Dispatcher):
    dp.message.register(command_start_handler, CommandStart())
    dp.callback_query.register(list_menu_callback, lambda c : c.data == "list_menu")
    dp.callback_query.register(back_to_start_callback, lambda c: c.data == "back_to_start")
    dp.callback_query.register(paginate_menu_callback, lambda c: c.data.startswith("menu_page_"))
    dp.callback_query.register(view_cake_callback, lambda c: c.data.startswith("view_cake_"))
    dp.callback_query.register(order_cake_callback, lambda c: c.data.startswith("order_cake_"))
    dp.callback_query.register(order_paid_callback, lambda c: c.data.startswith("order_paid_"))
    dp.callback_query.register(order_unpaid_callback, lambda c: c.data.startswith("order_unpaid_"))

    # Регистрируем обработчик ввода количества в состоянии ожидания
    dp.message.register(process_quantity, StateFilter(OrderCakeState.waiting_for_quantity))
