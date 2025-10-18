from aiogram.fsm.state import StatesGroup, State


class RegistrationStates(StatesGroup):
    personal_data = State
    fio = State
    phone = State
