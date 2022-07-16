from aiogram import types
from aiogram.utils.callback_data import CallbackData

from data.config import METHODS
from middlewares import i18n

_ = i18n.lazy_gettext
plan_button = CallbackData('plan', 'method', 'days')
pay_button = CallbackData('payment', 'method')


async def plans_button():
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(text=_("7 kun"), callback_data=plan_button.new(method='weekly', days=7)),
                types.InlineKeyboardButton(text=_("30 kun"), callback_data=plan_button.new(method='monthly', days=30))
            ],
        ]
    )
    return keyboard


async def pamment_button(method_list=METHODS):
    markup = types.InlineKeyboardMarkup()
    for method in method_list:
        markup.add(types.InlineKeyboardButton(text=method_list[method], callback_data=pay_button.new(method=method)))
    return markup
