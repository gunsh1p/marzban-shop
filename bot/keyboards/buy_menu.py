from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from utils import goods

def get_buy_menu_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for good in goods.get():
        builder.row(InlineKeyboardButton(
            text=f"{good['title']} - {good['price']['en']}$/{good['price']['ru']}руб.", callback_data=good['callback'])
        )
    return builder.as_markup()