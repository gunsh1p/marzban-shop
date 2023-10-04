from aiogram.fsm.state import State, StatesGroup

class SetDayWord(StatesGroup):
    channel = State()
    word = State()
    all = State()

class Play(StatesGroup):
    running = State()