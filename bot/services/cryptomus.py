import asyncio
import hashlib
import time

from pyCryptomusAPI import pyCryptomusAPI, Invoice
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import insert

from db.models import CPayments
from utils import goods
import glv

client = pyCryptomusAPI(
    glv.config['MERCHANT_UUID'],
    payment_api_key=glv.config['CRYPTO_TOKEN'])

async def listen_to_payments() -> None:
    pass

async def create_payment(tg_id: int, callback: str) -> dict:
    good = goods.get(callback)
    prepared_str = str(tg_id) + str(time.time()) + callback
    o_id = hashlib.md5(prepared_str.encode()).hexdigest()
    response: Invoice = client.create_invoice(
        amount=good['price']['en'],
        currency="USD",
        order_id=o_id,
        lifetime=600,
        is_payment_multiple=False)
    engine = create_async_engine(url=glv.config['DB_URL'], echo=True)
    async with engine.connect() as conn:
        sql_q = insert(CPayments).values(tg_id=tg_id, payment_uuid=response.uuid, order_id=response.order_id)
        await conn.execute(sql_q)
    await engine.dispose()
    return {
        "url": response.url,
        "price": response.amount
        }