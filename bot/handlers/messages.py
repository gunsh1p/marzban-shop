import uuid

from aiogram import Router, F
from aiogram import Dispatcher
from aiogram.types import Message, PreCheckoutQuery
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from marzpy import Marzban
from marzpy.api.user import User

from .commands import start
from keyboards import get_buy_menu_keyboard, get_back_keyboard, get_main_menu_keyboard
from db.models import VPNUsers
from utils import marzban_api, goods
import glv

router = Router(name="messages-router") 

@router.message(F.text == __("🛍️Buy"))
async def buy(message: Message):
    await message.answer(
        _("Read the <a href=\"{rules}\">rules</a> before buying").format(
            rules=glv.config['RULES_LINK']), 
        reply_markup=get_back_keyboard()
    )
    await message.answer(_("⬇️Tariffs"), reply_markup=get_buy_menu_keyboard())

@router.message(F.text == __("👤Profile"))
async def profile(message: Message, session: AsyncSession):
    panel = Marzban(glv.config['PANEL_USER'], glv.config['PANEL_PASS'], glv.config['PANEL_HOST'])
    mytoken = panel.get_token()
    sql_query = select(VPNUsers).where(VPNUsers.tg_id == message.from_user.id)
    result = (await session.execute(sql_query)).fetchone()[0]
    if not marzban_api.check_if_exists(result.vpn_id, panel):
        await message.answer(_("You haven't the VPN profile. Just buy the subscription to join out family"), reply_markup=get_main_menu_keyboard())
        return
    user = panel.get_user(result.vpn_id, mytoken)
    await message.answer(_("You can find out more about your subscription by following this <a href=\"{link}\">link</a>").format(
                        link=glv.config['PANEL_GLOBAL'] + user.subscription_url), 
                        reply_markup=get_back_keyboard())

@router.message(F.text == __("ℹ️Information"))
async def information(message: Message):
    await message.answer(text=glv.config['ABOUT'],reply_markup=get_back_keyboard())

@router.message(F.text == __("☎️Support"))
async def support(message: Message):
    await message.answer(
        _("Follow the <a href=\"{link}\">link</a> for help").format(
            link=glv.config['SUPPORT_LINK']),
        reply_markup=get_back_keyboard())
    
@router.message(F.text == __("🔙Back"))
async def start_text(message: Message, session: AsyncSession):
    await start(message, session)

@router.pre_checkout_query(lambda query: True)
async def pre_checkout_query(pre_checkout_q: PreCheckoutQuery):
    await glv.bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)


@router.message(F.successful_payment)
async def successful_payment(message: Message, session: AsyncSession):
    good = goods.get(message.successful_payment.invoice_payload)
    panel = Marzban(glv.config['PANEL_USER'], glv.config['PANEL_PASS'], glv.config['PANEL_HOST'])
    mytoken = panel.get_token()
    sql_query = select(VPNUsers).where(VPNUsers.tg_id == message.from_user.id)
    result = (await session.execute(sql_query)).fetchone()[0]
    if marzban_api.check_if_exists(result.vpn_id, panel):
        user = panel.get_user(result.vpn_id, mytoken)
        user.expire += marzban_api.get_subscription_end_date(good['months'], True)
        result = panel.modify_user(result.vpn_id, mytoken, user)
    else:
        user = User(
            username=result.vpn_id,
            proxies={
                "vless": {
                    "id": str(uuid.uuid4()),
                    "flow": "xtls-rprx-vision"
                },
            },
            inbounds={
                "vless": ["VLESS TCP REALITY"]
            },
            expire=marzban_api.get_subscription_end_date(good['months']),
            data_limit=0,
            data_limit_reset_strategy="no_reset",
        )
        result = panel.add_user(user=user, token=mytoken)
    await glv.bot.send_message(message.chat.id,
                           _("Thank you for your purchase. For instructions on how to connect, please follow this <a href=\"{link}\">link</a>").format(
                               link=glv.config['PANEL_GLOBAL'] + result.subscription_url
                           ),
                           reply_markup=get_main_menu_keyboard()
                        )
    await start(message, session)

def register_messages(dp: Dispatcher):
    dp.include_router(router)