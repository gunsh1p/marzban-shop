import json

from yookassa import Configuration
from yookassa import Payment
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import insert

from db.models import CPayments
from utils import goods
import glv

Configuration.configure(glv.config['YOOKASSA_SHOPID'], glv.config['YOOKASSA_TOKEN'])
    
async def create_payment(tg_id: int, callback: str, chat_id: int, lang_code: str) -> dict:
    good = goods.get(callback)
    payment = Payment.create({
        "amount": {
            "value": good['price']['ru'],
            "currency": "RUB"
        },
        "payment_method_data": {
            "type": "bank_card"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "Ссылка, куда перенаправить после совершения платежа"
        },
        "capture": True,
        "description": ""
        })
    resp = json.loads(payment)
    # engine = create_async_engine(url=glv.config['DB_URL'], echo=True)
    # async with engine.connect() as conn:
    #     sql_q = insert(CPayments).values(tg_id=tg_id, payment_uuid=resp['id'], order_id=response.order_id, chat_id=chat_id, callback=callback, lang=lang_code)
    #     await conn.execute(sql_q)
    #     await conn.commit()
    # await engine.dispose()
    # return {
    #     "url": response.url,
    #     "amount": response.amount
    #     }