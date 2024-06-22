from aiogram import Dispatcher, Router
from aiogram.types import Message
from aiogram.filters import Command, CommandObject

from db.models import Language, Scene

router = Router(name="user-start")

@router.message(
    Command("start")
)
async def start_command(message: Message, command: CommandObject, language: Language):
    scene = await Scene.get(language=language, title='start', action='greetings')
    await message.answer(scene.text)

def register_router(dp: Dispatcher) -> None:
    dp.include_router(router)