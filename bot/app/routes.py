from aiohttp.web_fileresponse import FileResponse
from aiohttp.web_request import Request
from aiohttp.web_response import json_response
from aiohttp import web

from aiogram import Bot
from aiogram.types import Update

import glv

async def check_crypto_payment(request: Request):
    bot: Bot = request.app["bot"]
    # data = await request.post()
    data = {"status": "ok", "work?": "yes"}
    return web.json_response(data)

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
        return web.Response(status=403) # if our TOKEN is not authenticated