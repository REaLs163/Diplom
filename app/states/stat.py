from aiogram.fsm.state import State, StatesGroup

class ReviewState(StatesGroup):
    waiting_for_url = State()
    waiting_for_count = State()
    active_session = State()