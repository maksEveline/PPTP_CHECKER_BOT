from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


async def get_main_menu():
    kb = [
        [
            KeyboardButton(text="Сгенерировать айпи"),
            KeyboardButton(text="Загрузить файл"),
        ],
        [
            KeyboardButton(text="Принудительно проверить"),
            KeyboardButton(text="Удалить айпи"),
        ],
    ]

    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

    return keyboard
