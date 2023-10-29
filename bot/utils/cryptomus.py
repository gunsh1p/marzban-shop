import time
import hashlib

from pyCryptomusAPI import pyCryptomusAPI, Invoice

from db.methods import add_cryptomus_payment
from utils import goods
import glv

async def create_payment(tg_id: int, callback: str, chat_id: int, lang_code: str) -> dict:
    client = pyCryptomusAPI(
        glv.config['MERCHANT_UUID'],
        payment_api_key=glv.config['CRYPTO_TOKEN'])
    good = goods.get(callback)
    prepared_str = str(tg_id) + str(time.time()) + callback
    o_id = hashlib.md5(prepared_str.encode()).hexdigest()
    response: Invoice = client.create_invoice(
        amount=good['price']['en'],
        currency="USD",
        order_id=o_id,
        lifetime=1800,
        url_callback=glv.config['WEBHOOK_URL'] + "/cryptomus_payment",
        is_payment_multiple=False)
    await add_cryptomus_payment(tg_id, callback, chat_id, lang_code, response)
    return {
        "url": response.url,
        "amount": response.amount
        }