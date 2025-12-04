from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from db.database import get_user_stats_since, get_user_last_reset
from keyboards.reply import main_menu_keyboard

router = Router()

class ReportState(StatesGroup):
    clean = State()
    processes = State()
    sender = State()
    receiver = State()

# Список сотрудников (потом можно заменить на данные из базы)
staff = ["Сущенко", "Дударчук", "Мелихова", "Зимина"]

yes_no_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Да"), KeyboardButton(text="Нет")]],
    resize_keyboard=True
)

staff_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text=name)] for name in staff],
    resize_keyboard=True
)

@router.message(F.text == "📝 Завершить смену")
async def start_report(message: Message, state: FSMContext):
    await state.set_state(ReportState.clean)
    await message.answer("Наведён ли порядок на зоне?", reply_markup=yes_no_kb)

@router.message(ReportState.clean)
async def step_clean(message: Message, state: FSMContext):
    await state.update_data(clean=message.text)
    await state.set_state(ReportState.processes)
    await message.answer("Забирали в операции?", reply_markup=yes_no_kb)

@router.message(ReportState.processes)
async def step_processes(message: Message, state: FSMContext):
    await state.update_data(processes=message.text)
    await state.set_state(ReportState.sender)
    await message.answer("Кто сдал смену?", reply_markup=staff_kb)

@router.message(ReportState.sender)
async def step_sender(message: Message, state: FSMContext):
    await state.update_data(sender=message.text)
    await state.set_state(ReportState.receiver)
    await message.answer("Кто принял смену?", reply_markup=staff_kb)

@router.message(ReportState.receiver)
async def step_receiver(message: Message, state: FSMContext):
    await state.update_data(receiver=message.text)
    data = await state.get_data()
    await state.clear()

    user_id = message.from_user.id
    last_reset = get_user_last_reset(user_id)
    stats = get_user_stats_since(user_id, last_reset)

    labels = {
        "repack": "📦 Спасено заказов",
        "defect": "❌ Оформленно браков",
        "anomaly": "🤯 Оформленно аномалий",
        "detected_anomaly": "🤖 Распознано аномалий"
    }

    report = (
        "📦 Завершение смены:\n\n"
        f"✅ Порядок на зоне: {data['clean']}\n"
        f"🔄 Забирали в процессы: {data['processes']}\n\n"
        f"👤 Сдаёт: {data['sender']}\n"
        f"👤 Принимает: {data['receiver']}\n\n"
        f"📊 Личная статистика за смену:\n"
    )

    for key, label in labels.items():
        report += f"{label}: {stats.get(key, 0)}\n"

    await message.answer("📝 Отчёт готов. Можешь переслать его в группу:\n\n" + report, reply_markup=main_menu_keyboard)
    await message.answer(
        "⚠️ Не забудь сбросить свою статистику по команде /reset, чтобы начать новый отчётный период.\n"
    "Это сообщение не нужно пересылать в группу."
    )
