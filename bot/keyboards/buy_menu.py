from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.i18n import gettext as _

from utils import goods

def get_buy_menu_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for good in goods.get():
        builder.row(InlineKeyboardButton(
            text=_("{title} - {price_en}$/{price_ru}rub").format(
                title=good['title'],
                price_en=good['price']['en'],
                price_ru=good['price']['ru']
                ), 
            callback_data=good['callback'])
        )
    return builder.as_markup()