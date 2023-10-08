import os

from aiogram import Bot, Dispatcher

config = {
    'BOT_TOKEN': os.environ.get('BOT_TOKEN'),
    'SHOP_NAME': os.environ.get('SHOP_NAME'),
    'DB_URL': os.environ.get('DB_URL'),
    'KASSA_TOKEN': os.environ.get('KASSA_TOKEN'),
    'CRYPTO_TOKEN': os.environ.get('CRYPTO_TOKEN'),
    'PANEL_HOST': os.environ.get('PANEL_HOST'),
    'PANEL_USER': os.environ.get('PANEL_USER'),
    'PANEL_PASS': os.environ.get('PANEL_PASS'),
}

bot: Bot = None
storage = None
dp: Dispatcher = None