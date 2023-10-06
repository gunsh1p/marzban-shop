import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, enums
from aiogram.fsm.storage.memory import MemoryStorage

from handlers.commands import register_commands
import glv

glv.bot = Bot(glv.config['BOT_TOKEN'], parse_mode=enums.ParseMode.HTML)
glv.storage = MemoryStorage()
glv.dp = Dispatcher(storage=glv.storage)
logging.basicConfig(level=logging.INFO)

def setup_routers():
    register_commands(glv.dp)

def main():
    setup_routers()
    
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(glv.dp.start_polling(glv.bot))

if __name__ == "__main__":
    main()