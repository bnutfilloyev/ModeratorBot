import asyncio

from aiogram import types

from filters import IsGroup
from loader import dp, bot

from middlewares import checker
from utils.db_api.database import Users


@dp.message_handler(IsGroup())
async def checker_handler(message: types.Message):
    user = Users()
    if not (user.have_chat_id(message.from_user.id) and user.have_chat_in_db(message.from_user.id, message.chat.id)):
        await user.add_chat_id(message.from_user.id, message.chat.id)

    if await user.get_user_status(message.from_user.id) == 'active':
        return

    await bot.restrict_chat_member(message.chat.id, message.from_user.id, can_send_messages=False)
    await bot.send_message(types.User.get_current().id, "Siz pul to'lamagansiz!")
