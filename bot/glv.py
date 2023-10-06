import os

from aiogram import Bot, Dispatcher

config = {
    "BOT_TOKEN": os.environ.get('BOT_TOKEN'),
    'DB_URL': os.environ.get('DB_URL')
}

bot: Bot = None
storage = None
dp: Dispatcher = None