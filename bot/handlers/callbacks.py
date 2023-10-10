from datetime import datetime, timedelta

from aiogram import Router, F
from aiogram import Dispatcher
from aiogram.types import CallbackQuery, LabeledPrice
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __

from keyboards import get_payment_keyboard, get_crypto_keyboard
from utils import goods
from services import create_payment
import glv

router = Router(name="callbacks-router") 

@router.callback_query(F.data.startswith("pay_kassa_"))
async def callback_payment_method_select(callback: CallbackQuery):
    await callback.message.delete()
    data = callback.data.replace("pay_kassa_", "")
    if data not in goods.get_callbacks():
        await callback.answer()
        return
    good = goods.get(data)
    if glv.config['KASSA_TOKEN'].split(':')[1] == 'TEST':
        await glv.bot.send_message(callback.message.chat.id, "Test payment!")
    PRICE = LabeledPrice(label="VPN Subscription", amount=good['price']['ru'] * 100)

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
                            start_parameter="vpn-subscription",
                            payload=good['callback'])
    await callback.answer()

@router.callback_query(F.data.startswith("pay_crypto_"))
async def callback_payment_method_select(callback: CallbackQuery):
    await callback.message.delete()
    data = callback.data.replace("pay_crypto_", "")
    if data not in goods.get_callbacks():
        await callback.answer()
        return
    result = await create_payment(callback.from_user.id, data)
    now = datetime.now()
    expire_date = (now + timedelta(minutes=10)).strftime("%d/%m/%Y, %H:%M")
    await callback.message.answer(
        _("An invoice has been issued in the amount of {amount}$. Pay it by {date}. After payment, wait until the payment is approved and you receive a confirmation message").format(
            amount=result['amount'],
            date=expire_date
        ),
        reply_markup=get_crypto_keyboard(result['url']))
    await callback.answer()

@router.callback_query(lambda c: c.data in goods.get_callbacks())
async def callback_payment_method_select(callback: CallbackQuery):
    await callback.message.delete()
    good = goods.get(callback.data)
    await callback.message.answer(text=_("Select a payment method"), reply_markup=get_payment_keyboard(good))
    await callback.answer()

def register_callbacks(dp: Dispatcher):
    dp.include_router(router)