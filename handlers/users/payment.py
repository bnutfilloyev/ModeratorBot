from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentTypes

from data.config import CLICK_PROVIDER_TOKEN, PAYME_PROVIDER_TOKEN
from keyboards.inline.buttons import pay_button
from loader import dp, bot

from utils.db_api.database import Users


async def payment(pay_method, plan_method):
    token = CLICK_PROVIDER_TOKEN
    prices = [types.LabeledPrice(label='7 kunlik', amount=5000000)]
    if pay_method == 'payme':
        token = PAYME_PROVIDER_TOKEN

    if plan_method == 'monthly':
        prices = [types.LabeledPrice(label='30 kunlik', amount=50000000)]

    return token, prices


@dp.callback_query_handler(pay_button.filter())
async def pamment_button_callback(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    async with state.proxy() as data:
        data['pay_method'] = callback_data['method']
        token, prices = await payment(data['pay_method'], data['method'])
    print(token, prices, sep='\n')
    await bot.send_invoice(
        call.message.chat.id,
        title="Bot bilan pul to'lash uchun",
        description='Bu yerda botni descriptioni bo\'lishi mumkin edi',
        provider_token=token,
        currency='uzs',
        prices=prices,
        is_flexible=False,  # True If you need to set up Shipping Fee
        start_parameter='time-machine-example',
        payload="TARIF UCHUN TOLOVLAR",
    )


@dp.pre_checkout_query_handler(lambda query: True)
async def checkout(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(
        pre_checkout_query.id,
        ok=True,
        error_message="Nimadir xato ketdi, iltimos qayta urinib ko'ring."
    )


@dp.message_handler(content_types=ContentTypes.SUCCESSFUL_PAYMENT)
async def got_payment(message: types.Message, state: FSMContext):
    user = Users()

    async with state.proxy() as data:
        user.update_user(message.chat.id, data['pay_method'], data['days'])

    await bot.send_message(
        message.chat.id,
        'Sizdan {} {} olib qolindi) Xaridingiz uchun rahmat'.format(
            message.successful_payment.total_amount / 100, message.successful_payment.currency),
        parse_mode='Markdown'
    )

    if user.have_chat_id(message.chat.id):
        for chat_id in user.get_chat_id(message.chat.id):
            await bot.restrict_chat_member(chat_id, message.chat.id, can_send_messages=True)
