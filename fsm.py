from aiogram.dispatcher.filters.state import State, StatesGroup



class Auth(StatesGroup):
    code = State()


class InfoTrainingFSM(StatesGroup):
    task1 = State()
    task2 = State()
    task3 = State()
    task4 = State()