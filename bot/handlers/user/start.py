from aiogram import Dispatcher, F, Router
from aiogram.types import Message
from aiogram.filters import Command, CommandObject

router = Router(name="user-start")

@router.message(
    Command("start")
)
async def start_command(message: Message, command: CommandObject):
    await message.answer('Hi!')

def register_router(dp: Dispatcher) -> None:
    dp.include_router(router)