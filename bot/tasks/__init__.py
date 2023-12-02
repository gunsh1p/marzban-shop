import aioschedule
import asyncio
import logging

from .update_token import update_token

async def register():
    aioschedule.every(5).minutes.do(update_token)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)