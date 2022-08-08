from aiogram import types
from aiogram.dispatcher.filters import CommandStart

from data.texts import texts
from filters import IsGroup
from loader import dp


@dp.message_handler(IsGroup(), CommandStart())
async def bot_start(msg: types.Message):
    await msg.reply(texts['start_group'])

