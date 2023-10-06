import os

config = {
    "BOT_TOKEN": os.environ.get('BOT_TOKEN'),
    'DB_URL': os.environ.get('DB_URL')
}

bot = None
storage = None
dp = None