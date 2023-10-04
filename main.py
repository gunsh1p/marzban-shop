import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, enums
from aiogram.fsm.storage.memory import MemoryStorage

from handlers.start import register_start
import glv
from utils import cfg_claim

glv.token, = cfg_claim()

print(glv.token)

glv.bot = Bot(glv.token, parse_mode=enums.ParseMode.HTML)
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