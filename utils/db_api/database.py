from utils.db_api.mongo import USERS, GROUPS


class Users:
    def get_users(self):
        """
        Return users list
        """
        for user in USERS.find():
            yield user

    def update_user(self, user_id, pay_method, days):
        """
        Update user status
        """
        if USERS.find_one({'user_id': user_id}).get('days') is None:
            USERS.update_one({'user_id': user_id},
                             {'$set': {'days': int(days), 'method': pay_method, 'status': 'active'}})
            return

        old_days = USERS.find_one({'user_id': user_id}).get('days')
        USERS.update_one({'user_id': user_id},
                         {'$set': {'days': int(days) + int(old_days), 'method': pay_method, 'status': 'active'}})
        return

    def get_chat_id(self, user_id):
        """
        Return chat id
        """
        for chat_id in USERS.find_one({'user_id': user_id}).get('chat_id'):
            yield chat_id

    def have_chat_id(self, user_id):
        """
        Return True if user have chat id
        """
        if USERS.find_one({'user_id': user_id}) is None:
            return False
        if USERS.find_one({'user_id': user_id}).get('chat_id') is None:
            return False
        return True

    def have_chat_in_db(self, user_id, chat_id):
        """
        Return True if chat in user
        """
        if USERS.find_one({'user_id': user_id}).get('chat_id') is None:
            return False
        if chat_id in USERS.find_one({'user_id': user_id}).get('chat_id'):
            return True
        return False

    async def add_chat_id(self, user_id, chat_id):
        """
        Add chat id to user
        """
        USERS.update_one({'user_id': user_id},
                         {'$push': {'chat_id': chat_id}}, upsert=True)

    async def get_user_status(self, user_id):
        """
        Return user status
        """
        if USERS.find_one({'user_id': user_id}) is None:
            return

        return USERS.find_one({'user_id': user_id}).get('status')

    async def update_status(self, user_id, status):
        """
        Update user status
        """
        USERS.update_one({'user_id': user_id},
                         {'$set': {'status': status}})


class Groups:
    def get_groups(self):
        """
        Return groups list
        """
        for group in GROUPS.find():
            yield group

    async def set_groups(self, chat_id, group_name):
        """
        Set groups for user
        """
        GROUPS.update_one({'chat_id': chat_id},
                          {'$set': {'group_name': group_name}}, upsert=True)

    async def get_group_name(self, chat_id):
        """
        Return group name
        """
        if GROUPS.find_one({'chat_id': chat_id}) is None:
            return

        return GROUPS.find_one({'chat_id': chat_id}).get('group_name')
