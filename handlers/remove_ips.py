import re
import requests

from aiogram import Router, F, Bot
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from keyboards.user import get_main_menu
from utils.files_utils import clean_checked, get_unique_lines
from utils.pptp_checker import process_pptp_list, is_port_open
from utils.generator import generate_and_save_ips

from config import ADMIN_ID

router = Router()


class RemoveIpsState(StatesGroup):
    waiting_for_ips = State()


def remove_ip_req(ip):
    r = requests.get(
        "http://77.105.143.180:8000//remove_ip", params={"ip": "123.123.123.123"}
    )

    status = r.status_code
    if status == 200:
        return True
    else:
        return False


@router.message(F.text == "Удалить айпи")
async def start_get_ips(msg: Message, bot: Bot, state: FSMContext):
    user_id = msg.from_user.id
    if user_id in ADMIN_ID:
        await msg.answer(
            text="Введите IP-адреса для удаления (через запятую):",
        )
        await state.set_state(RemoveIpsState.waiting_for_ips)


@router.message(RemoveIpsState.waiting_for_ips)
async def get_ips(msg: Message, bot: Bot, state: FSMContext):
    ips = msg.text.split("\n")
    ips = [ip.strip() for ip in ips]

    removed = 0
    errors = 0

    if len(ips) > 0:
        for ip in ips:
            is_removed = remove_ip_req(ip)
            if is_removed:
                removed += 1
            else:
                errors += 1

    await msg.answer(
        text=f"IP-адреса успешно удалены.\n{removed} IP-адресов удалено.\n{errors} IP-адресов не удалось удалить.",
        reply_markup=await get_main_menu(),
    )
    await state.clear()
