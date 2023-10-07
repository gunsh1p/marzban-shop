from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.i18n import gettext as _

def get_payment_keyboard(good) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text=_("ЮKassa - {price}rub").format(
                price=good['price']['ru']
            ),
            callback_data=f"pay_kassa_{good['callback']}"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=f"Cryptomus - {good['price']['en']}$",
            callback_data=f"pay_crypto_{good['callback']}"
        )
    )
    return builder.as_markup()