import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID"))

cakes = [
    {
        "name": "Торт «Ваниль-малина»",
        "price": 1700,
        "per": "кг",
    },
    {
        "name": "Торт «Ваниль-клубника»",
        "price": 1700,
        "per": "кг",
    },
    {
        "name": "Торт «Ваниль-вишня»",
        "price": 1700,
        "per": "кг",
    },
    {
        "name": "Торт «Шоколад-вишня»",
        "price": 1700,
        "per": "кг",
    },
    {
        "name": "Торт «Сникерс»",
        "price": 1700,
        "per": "кг",
    },
    {
        "name": "Торт «Ферреро»",
        "price": 1700,
        "per": "кг",
    },
    {
        "name": "Торт «Манго-маракуйа»",
        "price": 1700,
        "per": "кг",
    },
    {
        "name": "Торт «Фисташка-малина»",
        "price": 1800,
        "per": "кг",
    },
    {
        "name": "Бенто-торт",
        "price": 1600,
        "per": "кг",
    },
    {
        "name": "Капеейки",
        "price": 300,
        "per": "шт",
    },
    {
        "name": "Трайфлы",
        "price": 300,
        "per": "шт",
    },
]

T_BANK_PHOTO_URL = "https://cdn.tbank.ru/static/pfa-multimedia/images/a34a491f-d265-4cac-a3e2-4d56f9fb4c05.png"