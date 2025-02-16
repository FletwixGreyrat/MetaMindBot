from aiogram.dispatcher.filters.state import State, StatesGroup



class Auth(StatesGroup):
    code = State()


class InfoTrainingFSM(StatesGroup):
    task1 = State()
    task2 = State()
    task3 = State()
    task4 = State()



class NeuroChat(StatesGroup):
    is_chat = State()


class Reflect(StatesGroup):
    qiestions = State()