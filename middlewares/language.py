from typing import Any, Tuple

from aiogram import types
from aiogram.contrib.middlewares.i18n import I18nMiddleware

from utils.db_api.mongo import LANG_STORAGE


class Localization(I18nMiddleware):
    async def get_user_locale(self, action: str, args: Tuple[Any]) -> str:
        """
        User locale getter
        You can override the method if you want to use different way of getting user language.
        :param action: event name
        :param args: event arguments
        :return: locale name
        """
        user: types.User = types.User.get_current()

        if LANG_STORAGE.find_one({"user_id": user.id}) is None:
            LANG_STORAGE.insert_one({"user_id": user.id, "lang": "uz"})

        *_, data = args
        language = data['locale'] = LANG_STORAGE.find_one({"user_id": user.id}).get('lang', 'uz')
        return language
