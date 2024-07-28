from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup,  WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.i18n import gettext as _

import glv

def get_subscription_keyboard(subscription_url) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text=_("Follow 🔗"),
            web_app=WebAppInfo(url=subscription_url)
        )
    )
    return builder.as_markup()