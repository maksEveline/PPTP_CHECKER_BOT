from aiogram import Router, F
from aiogram.types import Message

from data.database import add_user_if_not_exists
from keyboards.user import get_main_menu
from config import DB_PATH, ADMIN_ID

router = Router()


@router.message(F.text == "/start")
async def start_func(msg: Message):
    user_id = msg.from_user.id

    if user_id in ADMIN_ID:
        await add_user_if_not_exists(DB_PATH, user_id)

        await msg.answer(
            text=f"Привет, <b>{msg.from_user.full_name}</b>",
            parse_mode="html",
            reply_markup=await get_main_menu(),
        )
