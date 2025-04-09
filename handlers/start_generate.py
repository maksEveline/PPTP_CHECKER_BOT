import re

from aiogram import Router, F, Bot
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from utils.files_utils import clean_checked
from utils.pptp_checker import process_pptp_file
from utils.generator import generate_and_save_ips

from config import ADMIN_ID

router = Router()


class GenerateStates(StatesGroup):
    generate = State()
    start_ip = State()
    end_ip = State()
    is_start = State()


@router.message(F.text == "Сгенерировать айпи")
async def start_generate(msg: Message, bot: Bot, state: FSMContext):
    user_id = msg.from_user.id
    if user_id in ADMIN_ID:
        await msg.answer(
            text="Введите начальный IP-адрес в формате x.x.x.x\n\nНапример: <code>192.165.1.1</code>",
            parse_mode="html",
        )

        await state.set_state(GenerateStates.start_ip)


@router.message(GenerateStates.start_ip)
async def get_end_ip(msg: Message, bot: Bot, state: FSMContext):
    start_ip = msg.text

    if not re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", start_ip):
        await msg.answer(
            text="Некорректный IP-адрес. Введите снова.",
        )
        return

    await state.update_data({"start_ip": start_ip})

    await msg.answer(
        "Введите конечный IP-адрес в формате x.x.x.x\n\nНапример: <code>192.168.1.10</code>",
        parse_mode="html",
    )
    await state.set_state(GenerateStates.end_ip)


@router.message(GenerateStates.end_ip)
async def generate_ips(msg: Message, bot: Bot, state: FSMContext):
    end_ip = msg.text
    data = await state.get_data()
    start_ip = data.get("start_ip")

    if not re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", end_ip):
        await msg.answer(
            text="Некорректный IP-адрес. Введите снова.",
        )
        return

    msgg = await msg.answer(
        text="Генерация IP-адресов начата. Пожалуйста, подождите...",
    )

    gen_count = generate_and_save_ips(
        start_ip=start_ip, end_ip=end_ip, filename="ips.txt"
    )

    kb_btns = [
        [KeyboardButton(text="✅Запустить чек")],
        [KeyboardButton(text="❌Отменить чек")],
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb_btns,
        resize_keyboard=True,
        one_time_keyboard=True,
    )

    await bot.edit_message_text(
        chat_id=msg.chat.id,
        message_id=msgg.message_id,
        text=f"Генерация завершена. Сгенерировано <code>{gen_count}</code> IP-адресов.",
        parse_mode="html",
    )

    await msg.answer(
        text="Выберите действие:",
        reply_markup=keyboard,
    )

    await state.set_state(GenerateStates.is_start)


@router.message(GenerateStates.is_start)
async def start_check(msg: Message, bot: Bot, state: FSMContext):
    if msg.text == "✅Запустить чек":
        await msg.answer(
            text="Чек запущен. Ждите уведомлений...",
        )

        clean_checked()
        process_pptp_file("ips.txt")

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
