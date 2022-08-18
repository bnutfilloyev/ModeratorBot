from aiogram import types
from filters import AdminFilter
from loader import dp, bot


@dp.message_handler(AdminFilter(), commands=['info'], state='*')
async def add_groups(message: types.Message):
    await message.delete()
    await bot.send_message(message.from_user.id,
                           f"Yangi guruh qo'shish uchun so'rov yuborildi.\n\n"
                           f"Guruh nomi: <code>{message.chat.title}</code>\n"
                           f"Guruh ID: <code>{message.chat.id}</code>")
