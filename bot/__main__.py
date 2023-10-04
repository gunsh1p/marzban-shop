import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, enums
from aiogram.fsm.storage.memory import MemoryStorage

from handlers.commands import register_start
from bot.config_reader import config
import glv

glv.bot = Bot(config.bot_token.get_secret_value(), parse_mode=enums.ParseMode.HTML)
glv.storage = MemoryStorage()
glv.dp = Dispatcher(storage=glv.storage)
logging.basicConfig(level=logging.INFO)

def setup_routers():
    register_start(glv.dp)

def main():
    setup_routers()
    
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(glv.dp.start_polling(glv.bot))

if __name__ == "__main__":
    main()