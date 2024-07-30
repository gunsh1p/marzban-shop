import os

from aiogram import Bot, Dispatcher

config = {
    'BOT_TOKEN': os.environ.get('BOT_TOKEN'),
    'SHOP_NAME': os.environ.get('SHOP_NAME'),
    'PROTOCOLS': os.environ.get('PROTOCOLS', 'vless').split(),
    'TEST_PERIOD': os.environ.get('TEST_PERIOD', False) == 'true',
    'PERIOD_LIMIT': int(os.environ.get('PERIOD_LIMIT', 72)),
    'ABOUT': os.environ.get('ABOUT'),
    'RULES_LINK': os.environ.get('RULES_LINK'),
    'SUPPORT_LINK': os.environ.get('SUPPORT_LINK'),
    'DB_URL': f"mysql+asyncmy://{os.environ.get('DB_USER')}:{os.environ.get('DB_PASS')}@{os.environ.get('DB_ADDRESS')}:3306/{os.environ.get('DB_NAME')}",
    'YOOKASSA_TOKEN': os.environ.get('YOOKASSA_TOKEN'),
    'YOOKASSA_SHOPID': os.environ.get('YOOKASSA_SHOPID'),
    'EMAIL': os.environ.get('EMAIL'),
    'CRYPTO_TOKEN': os.environ.get('CRYPTO_TOKEN'),
    'MERCHANT_UUID': os.environ.get('MERCHANT_UUID'),
    'PANEL_HOST': os.environ.get('PANEL_HOST'),
    'PANEL_GLOBAL': os.environ.get('PANEL_GLOBAL'),
    'PANEL_USER': os.environ.get('PANEL_USER'),
    'PANEL_PASS': os.environ.get('PANEL_PASS'),
    'WEBHOOK_URL': os.environ.get('WEBHOOK_URL'),
    'WEBHOOK_PORT': int(os.environ.get('WEBHOOK_PORT')),
    'RENEW_NOTIFICATION_TIME': str(os.environ.get('RENEW_NOTIFICATION_TIME'))
}

bot: Bot = None
storage = None
dp: Dispatcher = None