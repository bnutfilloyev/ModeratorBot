from utils.db_api.database import Users


async def check_user_exists():
    users = Users()
    for user in users.get_users():
        if user.get('days') is None:
            continue
        if user.get('days') <= 0:
            await users.update_status(user.get('user_id'), 'inactive')
            continue
        users.update_user(user.get('user_id'), user.get('method'), -1)
        print(f'{user.get("user_id")} - {user.get("method")} - {user.get("days")}')
