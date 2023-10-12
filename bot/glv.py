import os

from aiogram import Bot, Dispatcher

config = {
    'BOT_TOKEN': os.environ.get('BOT_TOKEN'),
    'SHOP_NAME': os.environ.get('SHOP_NAME'),
    'ABOUT': os.environ.get('ABOUT'),
    'RULES_LINK': os.environ.get('RULES_LINK'),
    'SUPPORT_LINK': os.environ.get('SUPPORT_LINK'),
    'DB_URL': os.environ.get('DB_URL'),
    'KASSA_TOKEN': os.environ.get('KASSA_TOKEN'),
    'CRYPTO_TOKEN': os.environ.get('CRYPTO_TOKEN'),
    'MERCHANT_UUID': os.environ.get('MERCHANT_UUID'),
    'PANEL_HOST': os.environ.get('PANEL_HOST'),
    'PANEL_GLOBAL': os.environ.get('PANEL_GLOBAL'),
    'PANEL_USER': os.environ.get('PANEL_USER'),
    'PANEL_PASS': os.environ.get('PANEL_PASS'),
    'WEBHOOK_URL': os.environ.get('WEBHOOK_URL'),
}

bot: Bot = None
storage = None
dp: Dispatcher = None