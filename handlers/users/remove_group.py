from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from filters import AdminFilter
from keyboards.inline.buttons import group_button, group_name_button
from loader import dp
from states.States import RemoveGroup
from utils.db_api.database import Groups

groups = Groups()


@dp.message_handler(AdminFilter(), Command('removegroup'))
async def add_group(message: types.Message):
    await message.answer("O'chirmoqchi bo'lgan guruhni tanlang.", reply_markup=await group_button(groups.get_groups()))
    await RemoveGroup.GetGroupName.set()


@dp.callback_query_handler(group_name_button.filter(), state=RemoveGroup.GetGroupName)
async def group_name_button_callback(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await groups.remove_group(chat_id=callback_data['chat_id'])
    await call.message.edit_text(text="Guruh o'chirildi. Botni qayta ishga tushirish uchun /start bosing")
    await state.finish()
