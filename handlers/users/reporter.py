from aiogram import types
from aiogram.dispatcher.filters import Command

from keyboards.inline.buttons import report_btn, report_button
from loader import bot, dp
from utils.db_api.database import Groups, Payments

payments = Payments()
groups = Groups()


@dp.message_handler(Command('report'))
async def reporter(msg: types.Message):
    await msg.answer(
        text="🖥Hisobotlarni ko'rish uchun bosing.\n"
             "⏰<b>Oylik</b> - Sizning oy davomida qilgan umumiy foydangiz\n"
             "🗓<b>Yillik</b> - Sizning yil davomida qilgan umumiy foydangiz\n",
        reply_markup=await report_btn()
    )


@dp.callback_query_handler(report_button.filter(plan='monthly'))
async def report(call: types.CallbackQuery):
    ans_text = "<b>🗓Sizning oylik hisobotlaringiz.</b>\n\n"

    for chat_id in groups.get_all_chat_ids(call.from_user.id):
        group_name = await bot.get_chat(chat_id)
        amount = await payments.get_monthly_amount(chat_id)

        ans_text += f"<b>🤖Bot:</b> {group_name.title}\n" \
                    f"<b>💰Summa:</b> {amount} so'm\n\n"

    await call.message.answer(ans_text)


@dp.callback_query_handler(report_button.filter(plan='yearly'))
async def report(call: types.CallbackQuery):
    ans_text = "<b>🗓Sizning yillik hisobotlaringiz.</b>\n\n"

    for chat_id in groups.get_all_chat_ids(call.from_user.id):
        group_name = await bot.get_chat(chat_id)
        amount = await payments.get_yearly_amount(chat_id)

        ans_text += f"<b>🤖Bot:</b> {group_name.title}\n" \
                    f"<b>💰Summa:</b> {amount} so'm\n\n"

    await call.message.answer(ans_text)
