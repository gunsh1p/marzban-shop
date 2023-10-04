from aiogram import Router, F
from aiogram import Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from keyboards import get_menu_keyboard
import glv

router = Router(name="commands-router") 

@router.message(
    Command("start")
)
async def start(message: Message, state: FSMContext):
    text = f"Hello, {message.from_user.first_name}.\n\n🎉Welcome to {glv.config['NAME']}\n\n⬇️Select an action"
    await message.answer(text, reply_markup=get_menu_keyboard())

def register_start(dp: Dispatcher):
    dp.include_router(router)