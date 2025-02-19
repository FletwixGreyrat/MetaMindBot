from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def start_keyboard():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(text="Помощь⁉️", callback_data="s:help"))
    kb.insert(InlineKeyboardButton(text="Pomodoro-таймер🍅", callback_data="s:pomodoro"))
    kb.insert(InlineKeyboardButton(text="Метаког-ый тренинг", callback_data="s:metakog"))
    kb.add(InlineKeyboardButton(text="Тренинг с информацией", callback_data="s:info"))
    kb.insert(InlineKeyboardButton(text="Рефлексия", callback_data="s:reflect"))
    kb.add(InlineKeyboardButton(text="Чат с психологом", callback_data="s:psycho"))
    kb.add(InlineKeyboardButton(text="Пройти тест заново", callback_data="s:retest"))
    kb.add(InlineKeyboardButton(text="Профиль", callback_data="s:profile"))


    return kb


def main_menu_keyboard():
    kb = InlineKeyboardMarkup()

    kb.add(InlineKeyboardButton(text="В главное меню", callback_data="main_menu"))

    return kb