from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


async def get_main_menu():
    kb = [
        [KeyboardButton(text="Сгенерировать айпи")],
        [KeyboardButton(text="Загрузить файл")],
    ]

    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

    return keyboard
