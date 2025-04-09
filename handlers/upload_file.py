import os
import re
import requests

from aiogram import Router, F, Bot
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from utils.files_utils import clean_checked, get_unique_lines
from utils.pptp_checker import process_pptp_file, is_port_open
from utils.generator import generate_and_save_ips

from config import ADMIN_ID, BACKEND_URL

router = Router()


class UploadFileState(StatesGroup):
    waiting_for_file = State()
    is_start = State()


@router.message(F.text == "Загрузить файл")
async def upload_file(message: Message, state: FSMContext):
    await message.answer(
        "Отправьте файл с айпи адресами.(каждый с новой строки)\nИли напишите /cancel, чтобы отменить загрузку."
    )
    await state.set_state(UploadFileState.waiting_for_file)


@router.message(UploadFileState.waiting_for_file)
async def get_file(msg: Message, state: FSMContext, bot: Bot):
    if msg.document:
        dirs = os.listdir()
        if "ips.txt" in dirs:
            os.remove("ips.txt")

        file_id = msg.document.file_id
        file = await bot.get_file(file_id)
        file_path = file.file_path
        await bot.download_file(file_path, "ips.txt")

        with open("ips.txt", "r") as f:
            lines = f.readlines()
            linues_count = len(lines)

        kb_btns = [
            [KeyboardButton(text="✅Запустить чек")],
            [KeyboardButton(text="❌Отменить чек")],
        ]
        keyboard = ReplyKeyboardMarkup(
            keyboard=kb_btns,
            resize_keyboard=True,
            one_time_keyboard=True,
        )

        await msg.answer(
            f"Файл получен.\nНайдено <code>{linues_count}</code> строк.\n\n",
            reply_markup=keyboard,
            parse_mode="html",
        )
        await state.set_state(UploadFileState.is_start)
    elif msg.text == "/cancel":
        await msg.answer("Загрузка файла отменена.")
        await state.clear()
    else:
        await msg.answer("Пожалуйста, отправьте txt файл.")


@router.message(UploadFileState.is_start)
async def start_check_upld_file(msg: Message, bot: Bot, state: FSMContext):
    if msg.text == "✅Запустить чек":
        await msg.answer(
            text="Чек запущен. Ждите уведомлений...",
        )

        clean_checked()
        r = requests.get(
            f"{BACKEND_URL}/get_db",
        )
        with open("main_db.txt", "wb") as f:
            f.write(r.content)

        unique_lines = get_unique_lines("main_db.txt", "ips.txt")

        with open("ips.txt", "w") as f:
            for line in unique_lines:
                f.write(line + "\n")

        opened_ips = []

        with open("ips.txt", "r") as f:
            lines = f.readlines()
            lines = [line.strip() for line in lines if line.strip()]
            for line in lines:
                is_open = is_port_open(line.strip(), 1723)
                if is_open:
                    print(f"{line.strip()} 1723 is open")
                    opened_ips.append(line.strip())
                else:
                    print(f"{line.strip()} 1723 is closed")

        with open("ips.txt", "w") as f:
            for line in opened_ips:
                f.write(line + "\n")

        # process_pptp_file("ips.txt")

        await msg.answer(
            text="Проверка завершена.",
        )
    elif msg.text == "❌Отменить чек":
        await msg.answer(
            text="Чек отменен.",
        )
        await state.clear()
        return
    else:
        await msg.answer(
            text="Некорректный выбор. Пожалуйста, выберите действие из меню.",
        )
