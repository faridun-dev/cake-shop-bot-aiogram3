from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.config import cakes  # Импорт списка тортов из конфигурации

# Кнопка начала: "Посмотреть меню"
start = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Посмотреть меню 🍰", callback_data="list_menu")],
])

ITEMS_PER_PAGE = 5  # Количество тортов на одной странице меню

# Функция создания клавиатуры для отображения списка тортов с пагинацией
async def list_menu(page: int = 0) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    
    # Вычисляем диапазон тортов для текущей страницы
    start_idx = page * ITEMS_PER_PAGE
    end_idx = start_idx + ITEMS_PER_PAGE
    paginated_cakes = cakes[start_idx:end_idx]

    # Добавляем кнопки для каждого торта
    for cake in paginated_cakes:
        keyboard.add(InlineKeyboardButton(
            text=cake["name"],
            callback_data=f"view_cake_{cakes.index(cake)}"  # Используем индекс торта
        ))

    keyboard.adjust(1)  # Располагаем кнопки по одной в строке

    # Кнопки навигации (назад и вперед)
    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton(text="⬅️ Назад", callback_data=f"menu_page_{page - 1}"))
    if end_idx < len(cakes):
        nav_buttons.append(InlineKeyboardButton(text="Вперед ➡️", callback_data=f"menu_page_{page + 1}"))

    if nav_buttons:
        keyboard.row(*nav_buttons)  # Добавляем навигационные кнопки в одну строку

    # Кнопка возврата в главное меню
    keyboard.row(InlineKeyboardButton(text="🏠 В главное меню", callback_data="back_to_start"))

    return keyboard.as_markup()


# Клавиатура при просмотре информации о конкретном торте
async def view_cake(cake_index: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    # Кнопка оформления заказа
    order_button = InlineKeyboardButton(text="✅ Оформить", callback_data=f"order_cake_{cake_index}")
    # Кнопка возврата к меню
    back_to_menu_button = InlineKeyboardButton(text="🍰 Назад к меню", callback_data=f"list_menu")

    keyboard.add(order_button)
    keyboard.add(back_to_menu_button)

    return keyboard.adjust(2).as_markup()  # Располагаем кнопки по 2 в строке


# Клавиатура для отображения и изменения статуса заказа (оплачен / не оплачен)
async def order_status(status: bool, order_id: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    
    # Отображаем выбранный статус с соответствующим эмодзи
    paid_emoji = "✅" if status else "⚪"
    unpaid_emoji = "❌" if not status else "⚪"

    # Кнопки для изменения статуса
    button_paid = InlineKeyboardButton(text=f"{paid_emoji} Оплачено", callback_data=f"order_paid_{order_id}")
    button_unpaid = InlineKeyboardButton(text=f"{unpaid_emoji} Не оплачено", callback_data=f"order_unpaid_{order_id}")

    keyboard.row(button_paid, button_unpaid)

    return keyboard.as_markup()
