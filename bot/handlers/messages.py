from aiogram import Router, F
from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __

from .commands import start
from keyboards import get_buy_menu_keyboard, get_back_keyboard, get_main_menu_keyboard
from db.methods import can_get_test_sub, update_test_subscription_state, create_vpn_profile
from utils import marzban_api
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
async def profile(message: Message):
    user = await marzban_api.get_marzban_profile(message.from_user.id)
    if user is None:
        await message.answer(_("You haven't the VPN profile. Just buy the subscription to join out family"), reply_markup=get_main_menu_keyboard())
        return
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

@router.message(F.text == __("⏳️Test subscription"))
async def test_subscription(message: Message):
    result = await can_get_test_sub(message.from_user.id)
    if result:
        await message.answer(
            _("Sorry but you've already activated test subscription"),
            reply_markup=get_main_menu_keyboard())
        return
    await message.answer(_("Wait, the test subscription is being generated"))
    result = await create_vpn_profile(message.from_user.id)
    result = marzban_api.generate_test_subscription(result.vpn_id)
    await update_test_subscription_state(message.from_user.id)
    await message.answer(
        _("Here is your test subscription <a href=\"{link}\">link</a>").format(
            link=glv.config['PANEL_GLOBAL'] + result.subscription_url
        ),
        reply_markup=get_main_menu_keyboard()
    )
    
@router.message(F.text == __("🔙Back"))
async def start_text(message: Message):
    await start(message)

def register_messages(dp: Dispatcher):
    dp.include_router(router)