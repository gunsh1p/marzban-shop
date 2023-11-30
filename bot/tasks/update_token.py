import asyncio

from utils import marzban_api

async def update_token():
    marzban_api.panel.get_token()