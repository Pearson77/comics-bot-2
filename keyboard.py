from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database import DB


def create_comics_keyboard():
    names_list = DB.get_comics_all_names()
    keyboard = []

    for name in names_list:
        comics_len = DB.get_comics_len(name)
        keyboard.append([InlineKeyboardButton(
            text=name,
            callback_data=F"to-comics:{name}:{comics_len}"
        )])
    return InlineKeyboardMarkup(inline_keyboard=keyboard) if names_list else None


def create_delete_keyboard():
    names_list = DB.get_comics_all_names()
    keyboard = []

    for name in names_list:
        keyboard.append([InlineKeyboardButton(
            text=name,
            callback_data=F"delete:{name}"
        )])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def create_page_keyboard(comics_name: str, page: int, pages_count: int):
    keyboard = [[]]

    if page != 1:
        keyboard[0].append(InlineKeyboardButton(
            text="Назад",
            callback_data=F"to-page:{comics_name}:{page - 1}:{pages_count}"
        ))

    keyboard[0].append(InlineKeyboardButton(text=F"{page}/{pages_count}", callback_data="empty"))

    if page != pages_count:
        keyboard[0].append(InlineKeyboardButton(
            text="Вперед",
            callback_data=F"to-page:{comics_name}:{page + 1}:{pages_count}"
        ))

    keyboard.append([InlineKeyboardButton(
        text="В меню",
        callback_data="to-home"
    )])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)
