import asyncio
import uuid
import hashlib
import time

from pyCryptomusAPI import pyCryptomusAPI, Invoice
from marzpy import Marzban
from marzpy.api.user import User
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import insert, select, delete
from aiogram.utils.i18n import gettext as _

from db.models import CPayments, VPNUsers
from keyboards import get_main_menu_keyboard
from utils import goods, marzban_api
from handlers.commands import start
import glv

client = pyCryptomusAPI(
    glv.config['MERCHANT_UUID'],
    payment_api_key=glv.config['CRYPTO_TOKEN'])

async def listen_to_payments() -> None:
    await asyncio.sleep(30)
    engine = create_async_engine(url=glv.config['DB_URL'], echo=True)
    while True:
        async with engine.connect() as conn:
            async_result = await conn.stream(select(CPayments))
            async for row in async_result:
                response: Invoice = client.payment_information(
                    invoice_uuid=row.payment_uuid,
                    order_id=row.order_id
                )
                if response.payment_status in ['paid', 'paid_over']:
                    good = goods.get(row.callback)
                    panel = Marzban(glv.config['PANEL_USER'], glv.config['PANEL_PASS'], glv.config['PANEL_HOST'])
                    mytoken = panel.get_token()
                    sql_query = select(VPNUsers).where(VPNUsers.tg_id == row.tg_id)
                    result = (await conn.execute(sql_query)).fetchone()[0]
                    if marzban_api.check_if_exists(result.vpn_id, panel):
                        user = panel.get_user(result.vpn_id, mytoken)
                        user.expire += marzban_api.get_subscription_end_date(good['months'], True)
                        result = panel.modify_user(result.vpn_id, mytoken, user)
                    else:
                        user = User(
                            username=result.vpn_id,
                            proxies={
                                "vless": {
                                    "id": str(uuid.uuid4()),
                                    "flow": "xtls-rprx-vision"
                                },
                            },
                            inbounds={
                                "vless": ["VLESS TCP REALITY"]
                            },
                            expire=marzban_api.get_subscription_end_date(good['months']),
                            data_limit=0,
                            data_limit_reset_strategy="no_reset",
                        )
                        result = panel.add_user(user=user, token=mytoken)
                    message = await glv.bot.send_message(row.chat_id,
                           _("Thank you for your purchase. For instructions on how to connect, please follow this <a href=\"{link}\">link</a>").format(
                               link=glv.config['PANEL_GLOBAL'] + result.subscription_url
                           ),
                           reply_markup=get_main_menu_keyboard()
                        )
                    await start(message, conn)
                    sql_q = delete(CPayments).where(CPayments.payment_uuid == row.payment_uuid)
                    await conn.execute(sql_q)
                if response.payment_status in ['cancel', 'locked', 'refund_paid']:
                    sql_q = delete(CPayments).where(CPayments.payment_uuid == row.payment_uuid)
                    await conn.execute(sql_q)
        await asyncio.sleep(45)

async def create_payment(tg_id: int, callback: str, chat_id: int) -> dict:
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
        sql_q = insert(CPayments).values(tg_id=tg_id, payment_uuid=response.uuid, order_id=response.order_id, chat_id=chat_id, callback=callback)
        await conn.execute(sql_q)
    await engine.dispose()
    return {
        "url": response.url,
        "amount": response.amount
        }