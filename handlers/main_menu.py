from aiogram.types import Message
from keyboards.reply import main_menu_keyboard

async def start_handler(message: Message):
    await message.answer("Выбери действие:", reply_markup=main_menu_keyboard)
