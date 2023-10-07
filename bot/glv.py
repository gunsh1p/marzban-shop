import os

from aiogram import Bot, Dispatcher

config = {
    "BOT_TOKEN": os.environ.get('BOT_TOKEN'),
    'DB_URL': os.environ.get('DB_URL'),
    'KASSA_TOKEN': os.environ.get('KASSA_TOKEN'),
    'CRYPTO_TOKEN': os.environ.get('CRYPTO_TOKEN')
}

bot: Bot = None
storage = None
dp: Dispatcher = None