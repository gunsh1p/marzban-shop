from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.i18n import gettext as _

def get_back_keyboard() -> ReplyKeyboardMarkup:
    kb = [
        [
            KeyboardButton(text=_("🔙Back")),
        ]
    ]
    
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)