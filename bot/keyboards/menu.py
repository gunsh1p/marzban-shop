from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_menu_keyboard() -> ReplyKeyboardMarkup:
    kb = [
        [
            KeyboardButton(text="🛍️Buy"),
        ],
        [
            KeyboardButton(text="👤Profile"),
            KeyboardButton(text="ℹ️Information")
        ],
        [
            KeyboardButton(text="☎️Support")
        ]
    ]
    
    return ReplyKeyboardMarkup(keyboard=kb)