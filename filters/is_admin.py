import os
import json
from typing import Optional

from aiogram.filters import BaseFilter
from aiogram.types import Message


class IsAdminFilter(BaseFilter):
    def __init__(self, is_admin: Optional[bool] = None):
        self.is_admin = is_admin

    async def __call__(self, message: Message) -> bool:
        if self.is_admin is None:
            return False
        admins = json.loads(os.environ.get("ADMINS"))
        return (message.from_user.id in admins) == self.is_admin