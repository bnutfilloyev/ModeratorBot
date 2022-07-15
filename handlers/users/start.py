from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from data.texts import texts
from filters import IsPrivate
from keyboards.inline.buttons import plans_button
from loader import dp
from middlewares import i18n
from utils.db_api.mongo import USERS

_ = i18n.lazy_gettext


@dp.message_handler(IsPrivate(), CommandStart())
async def bot_start(message: types.Message):
    await message.answer(_(texts['welcome']))
    if USERS.find_one({'user_id': message.from_user.id}) is None:
        USERS.insert_one({'user_id': message.from_user.id})
    await message.answer(_(texts['choose_plan']), reply_markup=await plans_button())
