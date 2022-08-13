from aiogram import types
from aiogram.utils.callback_data import CallbackData

from data.config import METHODS
from middlewares import i18n

_ = i18n.lazy_gettext
plan_button = CallbackData('plan', 'method', 'days')
pay_button = CallbackData('payment', 'method')
group_name_button = CallbackData('group_name', 'chat_id')
report_button = CallbackData('report', 'plan')


async def plans_button():
    return types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(text=_("7 kun"), callback_data=plan_button.new(method='weekly', days=7)),
                types.InlineKeyboardButton(text=_("30 kun"), callback_data=plan_button.new(method='monthly', days=30))
            ]
        ]
    )


async def pamment_button(method_list=METHODS):
    markup = types.InlineKeyboardMarkup()
    for method in method_list:
        markup.insert(types.InlineKeyboardButton(text=method_list[method], callback_data=pay_button.new(method=method)))
    return markup


async def group_button(group_list):
    markup = types.InlineKeyboardMarkup()
    for group in group_list:
        markup.add(types.InlineKeyboardButton(text=group['group_name'],
                                              callback_data=group_name_button.new(chat_id=group['chat_id'])))
    return markup


async def report_btn():
    return types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(text="Oylik", callback_data=report_button.new(plan='monthly')),
                types.InlineKeyboardButton(text="Yillik", callback_data=report_button.new(plan='yearly'))
            ]
        ]
    )
