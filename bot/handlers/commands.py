from aiogram import Router
from aiogram import Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __

from keyboards import get_main_menu_keyboard
import glv

router = Router(name="commands-router") 

@router.message(
    Command("start")
)
async def start(message: Message):
    text = _("Hello, {name}.\n\n🎉Welcome to {title}\n\n⬇️Select an action").format(
        name=message.from_user.first_name,
        title=glv.config.get('SHOP_NAME', 'VPN Shop')
    )
    await message.answer(text, reply_markup=get_main_menu_keyboard())

def register_commands(dp: Dispatcher):
    dp.include_router(router)