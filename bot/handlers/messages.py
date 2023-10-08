from aiogram import Router, F
from aiogram import Dispatcher
from aiogram.types import Message, PreCheckoutQuery
from aiogram.enums.content_type import ContentType
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __
from sqlalchemy.ext.asyncio import AsyncSession

from .commands import start
from keyboards import get_buy_menu_keyboard, get_back_keyboard
import glv

router = Router(name="messages-router") 

@router.message(F.text == __("🛍️Buy"))
async def buy(message: Message):
    await message.answer(_("Read the rules before buying"), reply_markup=get_back_keyboard())
    await message.answer(_("⬇️Tariffs"), reply_markup=get_buy_menu_keyboard())
    
@router.message(F.text == __("🔙Back"))
async def start_text(message: Message, session: AsyncSession):
    await start(message, session)

@router.pre_checkout_query(lambda query: True)
async def pre_checkout_query(pre_checkout_q: PreCheckoutQuery):
    await glv.bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)


@router.message(F.successful_payment)
async def successful_payment(message: Message):
    payment_info = message.successful_payment.model_dump()
    for k, v in payment_info.items():
        print(f"{k} = {v}")

    await glv.bot.send_message(message.chat.id,
                           f"Payment for the amount of {message.successful_payment.total_amount // 100} {message.successful_payment.currency} was successful!!!")


def register_messages(dp: Dispatcher):
    dp.include_router(router)