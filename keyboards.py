from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def start_keyboard():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(text="📝 Пройти входной тест", callback_data="start_test"))
    return kb