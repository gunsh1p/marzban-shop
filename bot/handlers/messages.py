from aiogram import Router, F
from aiogram import Dispatcher
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __

from keyboards import get_buy_menu_keyboard
import glv

router = Router(name="messages-router") 

@router.message(F.text == __("🛍️Buy"))
async def buy(message: Message):
    await message.answer(_("Read the rules before buying"), reply_markup=ReplyKeyboardRemove())
    await message.answer(_("⬇️Tariffs"), reply_markup=get_buy_menu_keyboard())

def register_messages(dp: Dispatcher):
    dp.include_router(router)