from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from loader import bot


class Checker(BaseMiddleware):
    """if USER['user_id'] is not active, then user Readonly mode"""

    async def readonly_mode(self):
        """if USER['user_id'] is not active, then user Readonly mode"""
        user: types.User = types.User.get_current()
        chat: types.Chat = types.Chat.get_current()
        await bot.restrict_chat_member(chat.id, user.id, can_send_messages=False)

    async def disable_readonly_mode(self):
        """if USER['user_id'] is not active, then user Readonly mode"""
        user: types.User = types.User.get_current()
        chat: types.Chat = types.Chat.get_current()
        await bot.restrict_chat_member(chat.id, user.id, can_send_messages=True)
