import re

from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from utils.pptp_checker import process_pptp_list, is_port_open

from config import ADMIN_ID

router = Router()


class ForceCheckState(StatesGroup):
    waiting_for_ips = State()


@router.message(F.text == "Принудительно проверить")
async def force_check_start(message: Message, state: FSMContext):
    if message.from_user.id not in ADMIN_ID:
        await message.answer("У вас нет прав для выполнения этой команды.")
        return

    await message.answer("Отправьте айпи адреса для проверки.\n\nКаждый с новой строки")
    await state.set_state(ForceCheckState.waiting_for_ips)


@router.message(ForceCheckState.waiting_for_ips)
async def force_check_process(message: Message, state: FSMContext):
    ips = message.text.splitlines()

    invalid_ips = [
        ip for ip in ips if not re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", ip)
    ]

    if invalid_ips:
        await message.answer(f"Некорректные айпи адреса:\n{', '.join(invalid_ips)}")
        return

    all_opened_ips = []
    all_counter = 0
    opened_counter = 0

    for ip in ips:
        if opened_counter == 10:
            await message.answer(
                f"Пройдено {all_counter} IP-адресов\nАйдпи с открытым портом:{len(all_opened_ips)}"
            )
            opened_counter = 0

        if is_port_open(ip, 1723):
            all_counter += 1
            opened_counter += 1
            all_opened_ips.append(ip)
        else:
            all_counter += 1

    if len(all_opened_ips) == 0:
        await message.answer("Нет доступных PPTP серверов.")
        await state.clear()

        return

    await message.answer(
        f"Проверка на открытость портов закона.\nПроверено:{all_counter}\nОткрытых:{len(all_opened_ips)}\n\n"
    )

    process_pptp_list(ips)

    await message.answer("Проверка завершена. Результаты отправлены админу.")

    await state.clear()
    return
