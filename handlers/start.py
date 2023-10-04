from aiogram import Router, F
from aiogram import Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states import Play

router = Router() 

@router.message(
    Command("start")
)
async def start(message: Message, state: FSMContext):
    if await state.get_state() == Play.running and await state.get_data()["step"] < 6:
        await message.answer("Your are lose!")
        await state.clear()
        return
    await state.clear()
    text = f"Hello, {message.from_user.first_name}. It's a marzban-shop bot"
    await message.answer(text)

def register_start(dp: Dispatcher):
    dp.include_router(router)