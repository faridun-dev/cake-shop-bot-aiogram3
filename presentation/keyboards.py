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
        keyboard.add(InlineKeyboardButton(text=cake, callback_data="order_cake"))

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
