from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.utils.deep_linking import decode_payload

from data.texts import texts
from filters import IsPrivate
from keyboards.inline.buttons import plans_button, group_button
from loader import dp
from middlewares import i18n
from utils.db_api.database import Groups
from utils.db_api.mongo import USERS

_ = i18n.lazy_gettext


@dp.message_handler(IsPrivate(), CommandStart())
async def bot_start(message: types.Message):
    groups = Groups()
    args = message.get_args()
    await message.answer(_(texts['welcome']))

    if not args:
        await message.reply(texts['choose_group'], reply_markup=await group_button(groups.get_groups()))
        return

    payload = decode_payload(args)
    group_name = await groups.get_group_name(payload)
    if group_name is not None:
        if USERS.find_one({'user_id': message.from_user.id}) is None:
            USERS.insert_one({'user_id': message.from_user.id})
        await message.answer(_(texts['choose_plan']), reply_markup=await plans_button())
