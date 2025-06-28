# keyboards/reply.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📦 Спас заказ"), KeyboardButton(text="❌ Брак")],
        [KeyboardButton(text="🤯 Аномалия"), KeyboardButton(text="🤖 Аномалия распознана")],
        [KeyboardButton(text="📊 Статистика"), (KeyboardButton(text="📝 Завершить смену")
)]
    ],
    resize_keyboard=True
)
