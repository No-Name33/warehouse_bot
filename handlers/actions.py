from aiogram.types import Message
from db.database import get_user_stats_since, get_user_last_reset, save_action
from datetime import datetime


async def handle_repack(message: Message):
    save_action(user_id=message.from_user.id, action="repack")
    await message.answer("✅ +1 спасенный заказ!")

async def handle_defect(message: Message):
    save_action(user_id=message.from_user.id, action="defect")
    await message.answer("❌ Брак отмечен.")

async def handle_anomaly(message: Message):
    save_action(user_id=message.from_user.id, action="anomaly")
    await message.answer("🤯 Аномалия зарегистрирована.")

async def handle_detected_anomaly(message: Message):
    save_action(user_id=message.from_user.id, action="detected_anomaly")
    await message.answer("🤖 Аномалия распознана.")

async def handle_stats(message: Message):
    # Получаем дату последнего сброса
    last_reset = get_user_last_reset(message.from_user.id)

    # Получаем статистику с этой даты
    stats = get_user_stats_since(message.from_user.id, last_reset)

    if not stats:
        await message.answer("📊 Пока нет данных за текущую смену.\n\n"
                             "⚠️ Чтобы сбросить статистику, используй команду /reset"
        )
        return

    msg_lines = [f"📊 Статистика с {last_reset.strftime('%Y-%m-%d %H:%M:%S')}:"]
    labels = {
        "repack": "📦 Спасенных",
        "defect": "❌ Брак",
        "anomaly": "⚠️ Аномалия",
        "detected_anomaly": "🤖 Распознанная аномалия"
    }

    for key, label in labels.items():
        msg_lines.append(f"{label}: {stats.get(key, 0)}")
        
    msg_lines.append("\n⚠️ Чтобы сбросить статистику, используй команду /reset")

    await message.answer("\n".join(msg_lines))

