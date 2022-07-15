from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from data.texts import texts
from filters import IsPrivate
from keyboards.inline.payment_method import pamment_button
from loader import dp
from middlewares import i18n

_ = i18n.lazy_gettext


@dp.message_handler(IsPrivate(), CommandStart())
async def bot_start(message: types.Message):
    await message.answer(_(texts['welcome']))
    await message.answer(_(texts['payment_method']), reply_markup=await pamment_button())
