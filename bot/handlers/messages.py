from aiogram import Router, F
from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __

from .commands import start
from keyboards import get_buy_menu_keyboard, get_back_keyboard, get_main_menu_keyboard, get_subscription_keyboard
from db.methods import can_get_test_sub, update_test_subscription_state, get_marzban_profile_db
from utils import marzban_api
import glv

router = Router(name="messages-router") 

@router.message(F.text == __("Join 🏄🏻‍♂️"))
async def buy(message: Message):
    await message.answer(_("Choose the appropriate tariff ⬇️"), reply_markup=get_buy_menu_keyboard())

@router.message(F.text == __("My subscription 👤"))
async def profile(message: Message):
    user = await marzban_api.get_marzban_profile(message.from_user.id)
    if user is None:
        await message.answer(_("Your profile is not active at the moment.\n️\nYou can choose \"5 days free 🆓\" or \"Join 🏄🏻‍♂️\"."), reply_markup=get_main_menu_keyboard())
        return
    await message.answer(_("Subscription page ⬇️"), reply_markup=get_subscription_keyboard(glv.config['PANEL_GLOBAL'] + user['subscription_url']))

@router.message(F.text == __("Frequent questions ℹ️"))
async def information(message: Message):
    await message.answer(
        _("Follow the <a href=\"{link}\">link</a> 🔗").format(
            link=glv.config['ABOUT']),
        reply_markup=get_back_keyboard())

@router.message(F.text == __("Support ❤️"))
async def support(message: Message):
    await message.answer(
        _("Follow the <a href=\"{link}\">link</a> and ask us a question. We are always happy to help 🤗").format(
            link=glv.config['SUPPORT_LINK']),
        reply_markup=get_back_keyboard())

@router.message(F.text == __("5 days free 🆓"))
async def test_subscription(message: Message):
    result = await can_get_test_sub(message.from_user.id)
    if result:
        await message.answer(
            _("Your subscription is available in the \"My subscription 👤\" section."),
            reply_markup=get_main_menu_keyboard())
        return
    result = await get_marzban_profile_db(message.from_user.id)
    result = await marzban_api.generate_test_subscription(result.vpn_id)
    await update_test_subscription_state(message.from_user.id)
    await message.answer(
        _("Thank you for choice ❤️\n️\n<a href=\"https://t.me/...\">Subscribe</a> so you don't miss any announcements ✅\n️\nYour subscription is purchased and available in \"My subscription 👤\".").format(
            link=glv.config['PANEL_GLOBAL'] + result['subscription_url']
        ),
        reply_markup=get_main_menu_keyboard()
    )
    
@router.message(F.text == __("⏪ Back"))
async def start_text(message: Message):
    await start(message)

def register_messages(dp: Dispatcher):
    dp.include_router(router)
