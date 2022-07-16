from aiogram import Dispatcher

from data import config
from loader import dp
from .throttling import ThrottlingMiddleware
from .language import Localization
from .checker import Checker

if __name__ == "middlewares":
    dp.middleware.setup(ThrottlingMiddleware())
    i18n = Localization(config.I18N_DOMAIN, config.LOCALES_DIR)
    dp.middleware.setup(i18n)
    checker = Checker()
    dp.middleware.setup(checker)
