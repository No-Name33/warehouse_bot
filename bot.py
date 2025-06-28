import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram import F
from aiogram.types import Message
from config import BOT_TOKEN
from handlers.main_menu import start_handler
from handlers.actions import (
    handle_repack,
    handle_defect,
    handle_anomaly,
    handle_detected_anomaly,
    handle_stats,
)
from db.database import init_db
from handlers import reset, report


async def main():
    init_db()
    bot = Bot(token=BOT_TOKEN)   # создаём объект бота с токеном
    dp = Dispatcher()            # диспетчер для регистрации обработчиков

    dp.message.register(start_handler, Command(commands=["start"]))
    dp.message.register(handle_repack, F.text == "📦 Спас заказ")
    dp.message.register(handle_defect, F.text == "❌ Брак")
    dp.message.register(handle_anomaly, F.text == "🤯 Аномалия")
    dp.message.register(handle_detected_anomaly, F.text == "🤖 Аномалия распознана")
    dp.message.register(handle_stats, F.text == "📊 Статистика")
    dp.include_router(reset.router)
    dp.include_router(report.router)


    await dp.start_polling(bot)  # запускаем бота

if __name__ == "__main__":
    asyncio.run(main())
