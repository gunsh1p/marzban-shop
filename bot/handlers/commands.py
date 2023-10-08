import hashlib

from aiogram import Router, F
from aiogram import Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from keyboards import get_main_menu_keyboard
from db.models import VPNUsers
import glv

router = Router(name="commands-router") 

@router.message(
    Command("start")
)
async def start(message: Message, session: AsyncSession):
    await session.merge(VPNUsers(
        tg_id=message.from_user.id, 
        vpn_id=hashlib.md5(str(message.from_user.id).encode()).hexdigest())
    )
    await session.commit()
    text = _("Hello, {name}.\n\n🎉Welcome to {title}\n\n⬇️Select an action").format(
        name=message.from_user.first_name,
        title=glv.config.get('SHOP_NAME', 'VPN Shop')
    )
    await message.answer(text, reply_markup=get_main_menu_keyboard())

def register_commands(dp: Dispatcher):
    dp.include_router(router)