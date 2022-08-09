from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.deep_linking import get_start_link

from data.texts import texts
from filters import IsGroup
from loader import dp, bot

from utils.db_api.database import Users
from utils.db_api.mongo import MESSAGE


@dp.message_handler(IsGroup())
async def checker_handler(message: types.Message):
    user = Users()
    if await user.get_user_status(message.from_user.id, str(message.chat.id)) == 'active':
        return

    for user in await bot.get_chat_administrators(message.chat.id):
        if user.user.id == message.from_user.id:
            return

    await message.delete()
    msg = MESSAGE.find_one({'chat_id': str(message.chat.id)})
    print(msg)
    if msg is not None:
        await bot.delete_message(msg['chat_id'], msg['message_id'])
        MESSAGE.delete_one({'chat_id': str(message.chat.id)})

    deep_link = await get_start_link(message.chat.id, encode=True)
    join_btn = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="TO'LOV QILISH", url=deep_link)]])

    msg = await message.answer(texts['hello_group'], reply_markup=join_btn)
    MESSAGE.insert_one({'chat_id': str(message.chat.id), 'message_id': str(msg.message_id)})
    await bot.restrict_chat_member(message.chat.id, message.from_user.id, can_send_messages=False)
