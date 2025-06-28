from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from db.database import set_user_reset  # 👈 то же, что ты и вызывал

router = Router()

class ResetState(StatesGroup):
    confirmation = State()

# Клавиатура подтверждения
confirm_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="✅ Да"), KeyboardButton(text="❌ Нет")]
    ],
    resize_keyboard=True
)

@router.message(Command("reset"))
async def resetstats_command(message: Message, state: FSMContext):
    await state.set_state(ResetState.confirmation)
    await message.answer(
        "Ты точно хочешь сбросить статистику? Это только для личного сброса!",
        reply_markup=confirm_kb
    )

@router.message(ResetState.confirmation, F.text == "✅ Да")
async def resetstats_confirm_yes(message: Message, state: FSMContext):
    set_user_reset(message.from_user.id)
    await state.clear()
    await message.answer("✅ Статистика сброшена. Начинается новый отчётный период.",
                         reply_markup=ReplyKeyboardRemove())

@router.message(ResetState.confirmation, F.text == "❌ Нет")
async def resetstats_confirm_no(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("❌ Сброс отменён.", reply_markup=ReplyKeyboardRemove())
