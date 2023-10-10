import asyncio
import logging
import sys
from pathlib import Path

from aiogram import Bot, Dispatcher, enums
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.i18n import I18n, SimpleI18nMiddleware
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from handlers.commands import register_commands
from handlers.messages import register_messages
from handlers.callbacks import register_callbacks
from middlewares import DbSessionMiddleware
from db.base import Base
from services import listen_to_payments
import glv

glv.bot = Bot(glv.config['BOT_TOKEN'], parse_mode=enums.ParseMode.HTML)
glv.storage = MemoryStorage()
glv.dp = Dispatcher(storage=glv.storage)
logging.basicConfig(level=logging.INFO, stream=sys.stdout)

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
    
    asyncio.create_task(listen_to_payments())
    asyncio.run(glv.dp.start_polling(glv.bot))

if __name__ == "__main__":
    main()