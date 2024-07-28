import aioschedule
import asyncio
import logging

from .update_token import update_token
from.notify_renew_subscription import notify_users_to_renew_sub

import glv

async def register():
    aioschedule.every(5).minutes.do(update_token)
    aioschedule.every().day.at(glv.config['RENEW_NOTIFICATION_TIME']).do(notify_users_to_renew_sub)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)