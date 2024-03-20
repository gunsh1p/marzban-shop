import time
import hashlib
import aiohttp

from db.methods import add_cryptomus_payment
from utils import goods
from utils.webhook_data import get_sign
import glv

async def create_payment(tg_id: int, callback: str, chat_id: int, lang_code: str) -> dict:
    good = goods.get(callback)
    prepared_str = str(tg_id) + str(time.time()) + callback
    o_id = hashlib.md5(prepared_str.encode()).hexdigest()
    data = {
        "amount": str(good['price']['en']),
        "currency": "USD",
        "order_id": o_id,
        "lifetime": 1800,
        "url_callback": glv.config['WEBHOOK_URL'] + "/cryptomus_payment",
        "is_payment_multiple": False
    }
    headers = {
        'merchant': glv.config['MERCHANT_UUID'],
        'sign': get_sign(data, glv.config['CRYPTO_TOKEN']),
        'Content-Type': 'application/json'
    }
    response = None
    async with aiohttp.ClientSession() as session:
        async with session.post("https://api.cryptomus.com/v1/payment", json=data, headers=headers) as resp:
            if 200 <= resp.status < 300:
                response = (await resp.json())['result']
            else:
                raise Exception(f"Error: {resp.status}; Body: {await resp.text()}; Data: {data}")
    await add_cryptomus_payment(tg_id, callback, chat_id, lang_code, response)
    return {
        "url": response['url'],
        "amount": response['amount']
    }