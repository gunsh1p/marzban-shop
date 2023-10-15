import uuid
import logging

from aiohttp.web_request import Request
from aiohttp import web
from marzpy import Marzban
from marzpy.api.user import User
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import select, delete
from aiogram.types import Update

from db.models import CPayments, VPNUsers
from keyboards import get_main_menu_keyboard
from utils import webhook_data, goods, marzban_api
from services import get_i18n_string
import glv

async def check_crypto_payment(request: Request):
    if request.remote not in ["127.0.0.1", "91.227.144.54"]:
        return web.Response(status=403)
    data = await request.json()
    if not webhook_data.check(data, glv.config['CRYPTO_TOKEN']):
        return web.Response(status=403)
    engine = create_async_engine(url=glv.config['DB_URL'], echo=True)
    async with engine.connect() as conn:
        sql_q = select(CPayments).where(CPayments.order_id == data['order_id'])
        payment: CPayments = (await conn.execute(sql_q)).fetchone()
        if payment == None:
            return web.Response()
        if data['status'] in ['paid', 'paid_over']:
            good = goods.get(payment.callback)
            panel = Marzban(glv.config['PANEL_USER'], glv.config['PANEL_PASS'], glv.config['PANEL_HOST'])
            mytoken = panel.get_token()
            sql_query = select(VPNUsers).where(VPNUsers.tg_id == payment.tg_id)
            user_row = (await conn.execute(sql_query)).fetchone()
            if marzban_api.check_if_exists(user_row.vpn_id, panel):
                user = panel.get_user(user_row.vpn_id, mytoken)
                user.expire += marzban_api.get_subscription_end_date(good['months'], True)
                result = panel.modify_user(user_row.vpn_id, mytoken, user)
            else:
                user = User(
                    username=user_row.vpn_id,
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
            text = get_i18n_string("Thank you for your purchase. For instructions on how to connect, please follow this <a href=\"{link}\">link</a>", payment.lang)
            await glv.bot.send_message(payment.chat_id,
                text.format(
                    link=glv.config['PANEL_GLOBAL'] + result.subscription_url
                ),
                reply_markup=get_main_menu_keyboard(payment.lang)
            )
            sql_q = delete(CPayments).where(CPayments.payment_uuid == payment.payment_uuid)
            await conn.execute(sql_q)
            await conn.commit()
        if data['status'] == 'cancel':
            sql_q = delete(CPayments).where(CPayments.payment_uuid == payment.payment_uuid)
            await conn.execute(sql_q)
            await conn.commit()
    await engine.dispose()
    return web.Response()