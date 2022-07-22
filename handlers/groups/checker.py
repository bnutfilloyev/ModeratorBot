import asyncio

from aiogram import types
from aiogram.utils.deep_linking import get_start_link

from data.texts import texts
from filters import IsGroup
from loader import dp, bot

from middlewares import checker
from utils.db_api.database import Users


@dp.message_handler(IsGroup())
async def checker_handler(message: types.Message):
    user = Users()

    deep_link = await get_start_link(message.chat.id, encode=True)
    await message.reply(texts['hello_group'].format(link=deep_link), parse_mode=types.ParseMode.MARKDOWN)

    if not (user.have_chat_id(message.from_user.id) and user.have_chat_in_db(message.from_user.id, message.chat.id)):
        await user.add_chat_id(message.from_user.id, message.chat.id)

    if await user.get_user_status(message.from_user.id) == 'active':
        return

    await bot.restrict_chat_member(message.chat.id, message.from_user.id, can_send_messages=False)

    await bot.send_message(types.User.get_current().id, "Siz pul to'lamagansiz!")
