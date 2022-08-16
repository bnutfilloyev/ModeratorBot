from aiogram import types
from aiogram.dispatcher import FSMContext

from data.texts import texts
from keyboards.inline.buttons import plan_button, pamment_button
from loader import dp
from middlewares import i18n

_ = i18n.lazy_gettext


@dp.callback_query_handler(plan_button.filter(method='free'))
async def free_plan_button(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    async with state.proxy() as data:
        data['method'] = callback_data['method']
        data['days'] = callback_data['days']
    await call.message.edit_text(text=texts['free_plan'])
    await call.message.edit_reply_markup(reply_markup=await pamment_button({'verify': 'Tasdiqlash✅'}))


@dp.callback_query_handler(plan_button.filter())
async def plan_button_callback(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    async with state.proxy() as data:
        data['method'] = callback_data['method']
        data['days'] = callback_data['days']
    await call.message.edit_text(text=_(texts['payment_method']).format(day=callback_data.get('days')))
    await call.message.edit_reply_markup(reply_markup=await pamment_button())
