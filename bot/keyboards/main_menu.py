from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.i18n import gettext as _

from services import get_i18n_string

def get_main_menu_keyboard(lang=None) -> ReplyKeyboardMarkup:
    if lang is None:
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
        
        return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    kb = [
        [
            KeyboardButton(text=get_i18n_string("🛍️Buy", lang)),
        ],
        [
            KeyboardButton(text=get_i18n_string("👤Profile", lang)),
            KeyboardButton(text=get_i18n_string("ℹ️Information", lang))
        ],
        [
            KeyboardButton(text=get_i18n_string("☎️Support", lang))
        ]
    ]

    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)   