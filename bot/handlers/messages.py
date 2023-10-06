from aiogram import Router, F
from aiogram import Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove

from keyboards import get_buy_menu_keyboard
import glv

router = Router(name="messages-router") 

@router.message(F.text)
async def buy(message: Message):
    if message.text.lower() != "🛍️buy":
        return
    await message.answer("Read the rules before buying", reply_markup=ReplyKeyboardRemove())
    await message.answer("⬇️Tariffs", reply_markup=get_buy_menu_keyboard())

def register_messages(dp: Dispatcher):
    dp.include_router(router)