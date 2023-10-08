from aiogram import Router, F
from aiogram import Dispatcher
from aiogram.types import CallbackQuery, LabeledPrice
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __

from keyboards import get_payment_keyboard
from utils import goods
import glv

router = Router(name="callbacks-router") 

@router.callback_query(F.data.startswith("pay_kassa_"))
async def callback_payment_method_select(callback: CallbackQuery):
    await callback.message.delete()
    if callback.data.replace("pay_kassa_", "") not in goods.get_callbacks():
        return
    data = callback.data.replace("pay_kassa_", "")
    good = goods.get(data)
    if glv.config['KASSA_TOKEN'].split(':')[1] == 'TEST':
        await glv.bot.send_message(callback.message.chat.id, "Тестовый платеж!!!")
    PRICE = LabeledPrice(label="One month subscription", amount=good['price']['ru'] * 100)

    await glv.bot.send_invoice(callback.message.chat.id,
                            title=_("VPN Subscription"),
                            description=_("Tariff - {title}").format(
                                title=good['title']
                                ),
                            provider_token=glv.config['KASSA_TOKEN'],
                            currency="rub",
                            photo_url=good['image'],
                            photo_width=256,
                            photo_height=256,
                            photo_size=256,
                            is_flexible=False,
                            prices=[PRICE],
                            start_parameter="one-month-subscription",
                            payload=good['callback'])
    await callback.answer()

@router.callback_query(F.data.startswith("pay_crypto_"))
async def callback_payment_method_select(callback: CallbackQuery):
    await callback.message.delete()
    if callback.data.replace("pay_crypto_", "") not in goods.get_callbacks():
        return
    data = callback.data.replace("pay_crypto_", "")
    good = goods.get(data)
    await callback.message.answer(f"Not available now!")
    await callback.answer()

@router.callback_query(lambda c: c.data in goods.get_callbacks())
async def callback_payment_method_select(callback: CallbackQuery):
    await callback.message.delete()
    good = goods.get(callback.data)
    await callback.message.answer(text=_("Select a payment method"), reply_markup=get_payment_keyboard(good))
    await callback.answer()

def register_callbacks(dp: Dispatcher):
    dp.include_router(router)