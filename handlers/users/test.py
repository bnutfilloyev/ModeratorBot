from aiogram import types

from loader import dp


@dp.callback_query_handler()
async def callback_query(call: types.CallbackQuery):
    print(call.data)


@dp.message_handler()
async def message(message: types.Message):
    print(message.text)
