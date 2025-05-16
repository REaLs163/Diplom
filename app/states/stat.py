from aiogram.fsm.state import State, StatesGroup

# Определяем состояния для бота
class ReviewState(StatesGroup):
    waiting_for_url = State()
    waiting_for_count = State()