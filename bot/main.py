import asyncio
import logging
import sys
from pathlib import Path

from aiogram import Bot, Dispatcher, enums
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.i18n import I18n, SimpleI18nMiddleware
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from aiohttp import web 
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from handlers.commands import register_commands
from handlers.messages import register_messages
from handlers.callbacks import register_callbacks
from app.routes import check_crypto_payment, handle_webhook
from middlewares import DbSessionMiddleware
from db.base import Base
import glv

glv.bot = Bot(glv.config['BOT_TOKEN'], parse_mode=enums.ParseMode.HTML)
glv.storage = MemoryStorage()
glv.dp = Dispatcher(storage=glv.storage)
app = web.Application()
logging.basicConfig(level=logging.INFO, stream=sys.stdout)

async def on_startup(bot: Bot):
    await bot.set_webhook(f"{glv.config['WEBHOOK_URL']}/webhook")

def setup_routers():
    register_commands(glv.dp)
    register_messages(glv.dp)
    register_callbacks(glv.dp)

def setup_middlewares():
    i18n = I18n(path=Path(__file__).parent / 'locales', default_locale='en', domain='bot')
    i18n_middleware = SimpleI18nMiddleware(i18n=i18n)
    i18n_middleware.setup(glv.dp)

async def init_models(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

def setup_database():
    engine = create_async_engine(url=glv.config['DB_URL'], echo=True)
    asyncio.run(init_models(engine))
    sessionmaker = async_sessionmaker(engine, expire_on_commit=False)
    glv.dp.update.middleware(DbSessionMiddleware(session_pool=sessionmaker))
    glv.dp.callback_query.middleware(CallbackAnswerMiddleware())

def main():
    setup_routers()
    setup_middlewares()
    setup_database()
    glv.dp.startup.register(on_startup)

    app.router.add_post("/crypto_status", check_crypto_payment)
    
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=glv.dp,
        bot=glv.bot,
    )
    webhook_requests_handler.register(app, path="/webhook")

    setup_application(app, glv.dp, bot=glv.bot)

    web.run_app(app, host="0.0.0.0", port=8081)

if __name__ == "__main__":
    main()