from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.i18n import gettext as _

def get_main_menu_keyboard() -> ReplyKeyboardMarkup:
    kb = [
        [
            KeyboardButton(text=_("🛍️Buy")),
        ],
        [
            KeyboardButton(text=_("👤Profile")),
            KeyboardButton(text=_("ℹ️Information"))
        ],
        [
            KeyboardButton(text=_("☎️Support"))
        ]
    ]
    
    return ReplyKeyboardMarkup(keyboard=kb)