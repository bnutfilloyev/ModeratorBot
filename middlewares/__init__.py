from aiogram import Dispatcher

from data import config
from loader import dp
from .throttling import ThrottlingMiddleware
from .language import Localization


if __name__ == "middlewares":
    dp.middleware.setup(ThrottlingMiddleware())
    i18n = Localization(config.I18N_DOMAIN, config.LOCALES_DIR)
    dp.middleware.setup(i18n)