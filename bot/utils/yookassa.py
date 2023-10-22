from yookassa import Configuration
from yookassa import Payment
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import insert

from db.models import YPayments
from utils import goods
import glv

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
        "reciept": {
            "customer": {
                "email": glv.config['EMAIL']
            },
            "items": [
                {
                    "description": "Подписка на VPN сервис",
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
    engine = create_async_engine(url=glv.config['DB_URL'], echo=True)
    async with engine.connect() as conn:
        sql_q = insert(YPayments).values(tg_id=tg_id, payment_id=resp.id, chat_id=chat_id, callback=callback, lang=lang_code)
        await conn.execute(sql_q)
        await conn.commit()
    await engine.dispose()
    return {
        "url": resp.confirmation.confirmation_url,
        "amount": resp.amount.value
    }