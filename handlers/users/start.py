from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.utils.deep_linking import decode_payload

from data.texts import texts
from filters import IsPrivate
from keyboards.inline.buttons import plans_button, group_button, group_name_button
from loader import dp
from middlewares import i18n
from utils.db_api.database import Groups, Users

_ = i18n.lazy_gettext

groups = Groups()
users = Users()


@dp.message_handler(IsPrivate(), CommandStart(), state="*")
async def bot_start(message: types.Message, state: FSMContext):
    args = message.get_args()
    await message.answer(_(texts['welcome']))

    if not args:
        await message.answer(texts['choose_group'], reply_markup=await group_button(groups.get_groups()))
        return

    payload = decode_payload(args)
    group_name = await groups.get_group_name(payload)

    async with state.proxy() as data:
        data['chat_id'] = payload

    if group_name is None:
        await message.reply(texts['group_not_found'])
        return

    if await users.get_user(user_id=message.from_user.id, chat_id=payload) is None:
        await users.set_base_info(user_id=message.from_user.id, chat_id=payload, name=message.from_user.full_name)

    free_plan = await users.use_free_plan(user_id=message.from_user.id, chat_id=payload)
    plan_text = texts['choose_plan']
    if free_plan:
        plan_text += "<i>-</i>" * 50
        plan_text += "\n\n<b>🚀 Bepul </b>- botdan test sifatida foydalanib ko'ring"
    await message.answer(plan_text, reply_markup=await plans_button(free_plan))


@dp.callback_query_handler(group_name_button.filter())
async def group_name_button_callback(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    async with state.proxy() as data:
        data['chat_id'] = callback_data['chat_id']

    if await users.get_user(user_id=call.from_user.id, chat_id=callback_data['chat_id']) is None:
        await users.set_base_info(user_id=call.from_user.id,
                                  chat_id=callback_data['chat_id'],
                                  name=call.from_user.full_name)

    free_plan = await users.use_free_plan(user_id=call.from_user.id, chat_id=callback_data['chat_id'])
    plan_text = texts['choose_plan']
    if free_plan:
        plan_text += "<i>-</i>" * 50
        plan_text += "\n\n🚀 Bepul - botdan test sifatida foydalanib ko'ring"
    await call.message.edit_text(plan_text, reply_markup=await plans_button(free_plan))
