import aioschedule
import asyncio

from .update_token import update_token

async def register():
    aioschedule.every(5).minutes.do(update_token)
    while True:
        aioschedule.run_pending()
        await asyncio.sleep(1)