from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.deep_linking import get_start_link

from data.texts import texts
from filters import IsGroup
from loader import dp, bot

from middlewares import i18n
from utils.db_api.database import Users

_ = i18n.lazy_gettext


@dp.message_handler(IsGroup())
async def checker_handler(message: types.Message):
    user = Users()
    if await user.get_user_status(message.from_user.id, str(message.chat.id)) == 'active':
        return
    await message.delete()

    deep_link = await get_start_link(message.chat.id, encode=True)
    join_btn = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="TO'LOV QILISH", url=deep_link)]])

    msg = await message.answer(texts['hello_group'], reply_markup=join_btn)
    await bot.restrict_chat_member(message.chat.id, message.from_user.id, can_send_messages=False)
