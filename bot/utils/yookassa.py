from yookassa import Configuration
from yookassa import Payment

from db.methods import add_yookassa_payment
from utils import goods
import glv

if glv.config['YOOKASSA_SHOPID'] and glv.config['YOOKASSA_TOKEN']:
    Configuration.configure(glv.config['YOOKASSA_SHOPID'], glv.config['YOOKASSA_TOKEN'])

async def create_payment(tg_id: int, callback: str, chat_id: int, lang_code: str) -> dict:
    good = goods.get(callback)
    resp = Payment.create({
        "amount": {
            "value": good['price']['ru'],
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": f"https://t.me/{(await glv.bot.get_me()).username}"
        },
        "capture": True,
        "description": f"Подписка на VPN {glv.config['SHOP_NAME']}",
        "save_payment_method": False,
        "receipt": {
            "customer": {
                "email": glv.config['EMAIL']
            },
            "items": [
                {
                    "description": f"Подписка на VPN сервис: кол-во месяцев - {good['months']}",
                    "quantity": "1",
                    "amount": {
                        "value": good['price']['ru'],
                        "currency": "RUB"
                    },
                    "vat_code": "1"
                },
            ]
        }
        })
    await add_yookassa_payment(tg_id, callback, chat_id, lang_code, resp.id)
    return {
        "url": resp.confirmation.confirmation_url,
        "amount": resp.amount.value
    }