from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.config import cakes

start = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Посмотреть меню 🍰", callback_data="list_menu")],
])

ITEMS_PER_PAGE = 5

async def list_menu(page: int = 0) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    
    start_idx = page * ITEMS_PER_PAGE
    end_idx = start_idx + ITEMS_PER_PAGE
    paginated_cakes = cakes[start_idx:end_idx]

    for cake in paginated_cakes:
        keyboard.add(InlineKeyboardButton(text=cake["name"], callback_data=f"view_cake_{cakes.index(cake)}"))

    keyboard.adjust(1)

    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton(text="⬅️ Назад", callback_data=f"menu_page_{page - 1}"))
    if end_idx < len(cakes):
        nav_buttons.append(InlineKeyboardButton(text="Вперед ➡️", callback_data=f"menu_page_{page + 1}"))

    if nav_buttons:
        keyboard.row(*nav_buttons)

    keyboard.row(InlineKeyboardButton(text="🏠 В главное меню", callback_data="back_to_start"))

    return keyboard.as_markup()


async def view_cake(cake_index: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    order_button = InlineKeyboardButton(text="✅ Оформить", callback_data=f"order_cake_{cake_index}")
    back_to_menu_button = InlineKeyboardButton(text="🍰 Назад к меню", callback_data=f"list_menu")

    keyboard.add(order_button)
    keyboard.add(back_to_menu_button)

    return keyboard.adjust(2).as_markup()

async def order_status(status: bool, order_id: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    
    paid_emoji = "✅" if status else "⚪"
    unpaid_emoji = "❌" if not status else "⚪"

    button_paid = InlineKeyboardButton(text=f"{paid_emoji} Оплачено", callback_data=f"order_paid_{order_id}")
    button_unpaid = InlineKeyboardButton(text=f"{unpaid_emoji} Не оплачено", callback_data=f"order_unpaid_{order_id}")

    keyboard.row(button_paid, button_unpaid)

    return keyboard.as_markup()

