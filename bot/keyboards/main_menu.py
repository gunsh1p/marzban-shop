from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.i18n import gettext as _

from utils import get_i18n_string
import glv

def get_main_menu_keyboard(lang=None) -> ReplyKeyboardMarkup:
    if lang is None:
        kb = [
            [
                KeyboardButton(text=_("Join 🏄🏻‍♂️")),
            ],
            [
                KeyboardButton(text=_("My subscription 👤")),
                KeyboardButton(text=_("Frequent questions ℹ️"))
            ],
            [
                KeyboardButton(text=_("Support ❤️"))
            ]
        ]
        
        if glv.config['TEST_PERIOD']:
            kb.insert(0, [KeyboardButton(text=_("5 days free 🆓")),])
        
        return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    kb = [
        [
            KeyboardButton(text=get_i18n_string("Join 🏄🏻‍♂️", lang)),
        ],
        [
            KeyboardButton(text=get_i18n_string("My subscription 👤", lang)),
            KeyboardButton(text=get_i18n_string("Frequent questions ℹ️", lang))
        ],
        [
            KeyboardButton(text=get_i18n_string("Support ❤️", lang))
        ]
    ]
        
    if glv.config['TEST_PERIOD']:
        kb.insert(0, [KeyboardButton(text=get_i18n_string("5 days free 🆓", lang)),])

    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)   
