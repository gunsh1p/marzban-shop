import uuid

from aiohttp.web_fileresponse import FileResponse
from aiohttp.web_request import Request
from aiohttp.web_response import json_response
from aiohttp import web
from marzpy import Marzban
from marzpy.api.user import User
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import insert, select, delete
from aiogram.types import Update
from aiogram.utils.i18n import gettext as _

from db.models import CPayments, VPNUsers
from keyboards import get_main_menu_keyboard
from utils import webhook_data, goods, marzban_api
from handlers.commands import start
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
        res = (await conn.execute(sql_q)).fetchone()
        if res == None:
            return web.Response()
        res: CPayments = res[0]
        if data['status'] in ['paid', 'paid_over']:
            good = goods.get(res.callback)
            panel = Marzban(glv.config['PANEL_USER'], glv.config['PANEL_PASS'], glv.config['PANEL_HOST'])
            mytoken = panel.get_token()
            sql_query = select(VPNUsers).where(VPNUsers.tg_id == res.tg_id)
            result = (await conn.execute(sql_query)).fetchone()[0]
            if marzban_api.check_if_exists(res.vpn_id, panel):
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
            message = await glv.bot.send_message(res.chat_id,
                _("Thank you for your purchase. For instructions on how to connect, please follow this <a href=\"{link}\">link</a>").format(
                    link=glv.config['PANEL_GLOBAL'] + result.subscription_url
                ),
                reply_markup=get_main_menu_keyboard()
            )
            await start(message, conn)
            sql_q = delete(CPayments).where(CPayments.payment_uuid == res.payment_uuid)
            await conn.execute(sql_q)
        if data['status'] == 'cancel':
            sql_q = delete(CPayments).where(CPayments.payment_uuid == res.payment_uuid)
            await conn.execute(sql_q)
    await engine.dispose()
    return web.Response()

async def handle_webhook(request):
    url = str(request.url)
    index = url.rfind('/')
    token = url[index+1:]
    print(token)
    if token == glv.config['BOT_TOKEN']:
        update = Update(**await request.json())
        await glv.dp.process_update(update)
        return web.Response()
    else:
        return web.Response(status=403)