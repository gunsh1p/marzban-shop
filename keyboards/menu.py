from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_menu_keyboard() -> ReplyKeyboardMarkup:
    kb = [
        [
            KeyboardButton("🛍️Buy"),
        ],
        [
            KeyboardButton("👤Profile"),
            KeyboardButton("ℹ️Information")
        ],
        [
            KeyboardButton("☎️Support")
        ]
    ]
    
    return ReplyKeyboardMarkup(kb)