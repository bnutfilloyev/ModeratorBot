from aiogram import types
from data.config import ADMINS
from filters import AdminFilter
from loader import dp, bot


@dp.message_handler(AdminFilter(), commands=['info'])
async def add_groups(message: types.Message):
    await message.delete()
    for admin in ADMINS:
        await bot.send_message(admin,
                               f"Yangi guruh qo'shish uchun so'rov yuborildi.\n\n"
                               f"Guruh nomi: <code>{message.chat.title}</code>\n"
                               f"Guruh ID: <code>{message.chat.id}</code>")
