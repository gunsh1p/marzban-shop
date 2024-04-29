import asyncio
import logging
import sys

from aiogram import Dispatcher, Bot
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from aiohttp import web 
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from tortoise import Tortoise

from config import config
from db.setup import CONFIG_ORM
from db.models import Admin
from utils.get_password_hash import get_password_hash
from handlers.user import (
    start
)

bot: Bot = Bot(config.BOT_TOKEN, parse_mode=ParseMode.HTML)
storage = RedisStorage.from_url('redis://redis:6379/0')
dp: Dispatcher = Dispatcher(
    storage=storage
)

def setup_logger():
    logging.basicConfig(
        level=logging.INFO, 
        stream=sys.stdout,
        format='[%(asctime)s] %(levelname)s:%(name)s: %(message)s'
    )

    logger = logging.getLogger("marzban-shop")
    logger.setLevel(logging.INFO)

async def setup_db():
    await Tortoise.init(
        CONFIG_ORM
    )

async def add_admin():
    if config.WEB_LOGIN == None or config.WEB_PASS == None:
        return
    is_existed: bool = (await Admin.get_or_none(username=config.WEB_LOGIN)) is not None
    if is_existed:
        return
    await Admin.create(
        username=config.WEB_LOGIN,
        password=get_password_hash(config.WEB_PASS)
    )


async def on_startup(bot: Bot):
    # delete old webhook
    await bot.delete_webhook()
    # setup new webhook
    await bot.set_webhook(f"{config.WEBHOOK_URL}/webhook")

def setup_middlewares():
    ...

def setup_handlers():
    start.register_router(dp)

async def main():
    setup_logger()
    await setup_db()
    await add_admin()
    dp.startup.register(on_startup)
    setup_handlers()
    setup_middlewares()

    app = web.Application()
    # app.router.add_post(
    #     "/payment", 
    #     check_payment
    # )
    
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
    )
    webhook_requests_handler.register(app, path="/webhook")

    setup_application(app, dp, bot=bot)
    await web._run_app(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())