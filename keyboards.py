from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def start_keyboard():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(text="📝 Пройти входной тест", callback_data="start_test"))
    return kb


def auth_code():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(text="Ввести код", callback_data="auth_code"))
    return kb


def train_tasks_keyboard():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(text="Экзамен через 3 дня"))
    kb.add()