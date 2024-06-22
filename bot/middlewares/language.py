from typing import Any, Awaitable, Callable, Dict
from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import CallbackQuery, Message

from db.models import Language
from config import config

class DetectLanguageMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message| CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:
        lang_code = event.from_user.language_code
        language = await Language.get_or_none(code=lang_code)
        if language is None:
            language = await Language.get(code=config.DEFAULT_LANG)
        data['language'] = language
        result = await handler(event, data)
        return result