from aiogram import types
from aiogram.dispatcher.filters import Command

from keyboards.inline.buttons import report_btn, report_button
from loader import dp


@dp.message_handler(Command('report'))
async def reporter(msg: types.Message):
    await msg.answer("Hisobotlarni ko'rish uchun bosing.", reply_markup=await report_btn())


@dp.callback_query_handler(report_button.filter())
async def report(call: types.CallbackQuery, callback_data: dict):
    if callback_data['plan'] == 'monthly':
        await call.message.answer("Oylik hisobotlar")
    if callback_data['plan'] == 'yearly':
        await call.message.answer("Yillik hisobotlar")
