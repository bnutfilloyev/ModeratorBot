from loader import bot
from utils.db_api.database import Users, Groups, Payments


async def check_user_exists():
    users = Users()
    for user in users.get_users():
        if user.get('days') is None:
            continue
        if user.get('days') <= 0:
            await users.update_status(user.get('user_id'), 'inactive')
            continue
        await users.update_user(user.get('user_id'), user.get('method'), -1)
        print(f'{user.get("user_id")} - {user.get("method")} - {user.get("days")}')


async def send_total_amount_to_admins():
    groups = Groups()
    payments = Payments()
    for group in groups.get_groups():
        admin_id = group.get('admin_id')
        chat_id = group.get('chat_id')
        amount = await payments.get_daily_amount(chat_id)
        group_name = await bot.get_chat(chat_id)
        await bot.send_message(admin_id,
                               "<b>{}</b> guruh bo'yicha 1 kunlik umumiy summa: {}".format(group_name.title, amount),
                               parse_mode='HTML')
