import asyncio
import logging
import sys
from pathlib import Path

from aiogram import Bot, Dispatcher, enums
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.i18n import I18n, SimpleI18nMiddleware

from handlers.commands import register_commands
from handlers.messages import register_messages
from handlers.callbacks import register_callbacks
import glv

glv.bot = Bot(glv.config['BOT_TOKEN'], parse_mode=enums.ParseMode.HTML)
glv.storage = MemoryStorage()
glv.dp = Dispatcher(storage=glv.storage)
logging.basicConfig(level=logging.INFO)

def setup_routers():
    register_commands(glv.dp)
    register_messages(glv.dp)
    register_callbacks(glv.dp)

def setup_middlewares():
    i18n = I18n(path=Path(__file__).parent / 'locales', default_locale='en', domain='bot')
    i18n_middleware = SimpleI18nMiddleware(i18n=i18n)
    i18n_middleware.setup(glv.dp)

def main():
    setup_routers()
    setup_middlewares()
    
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(glv.dp.start_polling(glv.bot))

if __name__ == "__main__":
    main()