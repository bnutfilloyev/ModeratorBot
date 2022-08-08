import typing

from aiogram.dispatcher.filters import BoundFilter

from data import config


class AdminFilter(BoundFilter):
    async def check(self, obj):
        return str(obj.from_user.id) in config.ADMINS
