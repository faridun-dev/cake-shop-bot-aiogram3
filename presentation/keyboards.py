from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

start = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Посмотреть меню 🍰", callback_data="list_menu"), InlineKeyboardButton(text="Сделать заказ", callback_data="order")],
])

list_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="1. Cake with chocolate", callback_data="order_cake")],
    [InlineKeyboardButton(text="2. Cake with vanilla", callback_data="order_cake")],
    [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_start")]
])