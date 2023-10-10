import asyncio

from pyCryptomusAPI import pyCryptomusAPI

import glv

client = pyCryptomusAPI(
    glv.config['MERCHANT_UUID'],
    payment_api_key=glv.config['CRYPTO_TOKEN'])   # Payment API key (for payment methods)

async def listen_to_payments() -> None:
    pass