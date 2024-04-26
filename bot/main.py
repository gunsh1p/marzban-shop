import asyncio
import logging
import sys

from aiogram import Dispatcher, Bot
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from aiohttp import web 
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from tortoise import Tortoise

from config import load_config, config

bot: Bot = Bot(config.TOKEN, parse_mode=ParseMode.HTML)
storage = RedisStorage.from_url(config.REDIS_URL)
dp: Dispatcher = Dispatcher(
    storage=storage
)

async def setup_db():
    CONFIG_ORM = {
        "connections": {
            "postgre": {
                "engine": "tortoise.backends.asyncmy",
                "credentials": {
                    "host": config.DB_HOST,
                    "port": config.DB_PORT,
                    "database": config.DB_NAME,
                    "user": config.DB_USER,
                    "password": config.DB_PASS,
                }
            }
        },
        "apps": {
            "default": {"models": ["db.models"], "default_connection": "postgre"}
        }
    }
    await Tortoise.init(
        CONFIG_ORM
    )
    # await Tortoise.generate_schemas(safe=True)

async def add_admin():
    

async def on_startup(bot: Bot):
    # delete old webhook
    await bot.delete_webhook()
    # set new webhook if MODE == 'WEBHOOK'
    if config.MODE == 'WEBHOOK':
        await bot.set_webhook(f"{config.WEBHOOK_URL}/webhook")

def setup_middlewares():
    ...

def setup_handlers():
    ...

async def main():
    load_config()
    asyncio.gather(setup_db())
    dp.startup.register(on_startup)
    setup_handlers()
    setup_middlewares()
    
    if config.MODE == 'POLLING':
        await dp.start_polling(bot)
        return
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