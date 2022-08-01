from utils.db_api.mongo import USERS, GROUPS


class Users:
    def get_users(self):
        """
        Return users list
        """
        for user in USERS.find():
            yield user

    async def get_user(self, **kwargs):
        """
        Return user
        """
        return USERS.find_one(kwargs)

    async def set_base_info(self, **kwargs):
        """
        Set base info
        """
        USERS.update_one({'user_id': kwargs.get('user_id'), 'chat_id': kwargs.get('chat_id')},
                         {'$set': {'fullName': kwargs.get('name'),
                                   'status': 'deactive',
                                   'days': 0}}, upsert=True)

    async def update_user(self, user_id, pay_method, days, chat_id):
        """
        Update user status
        """
        if USERS.find_one({'user_id': user_id, 'chat_id': chat_id}).get('days') is None:
            USERS.update_one({'user_id': user_id},
                             {'$set': {'days': int(days),
                                       'method': pay_method,
                                       'status': 'active'}}, upsert=True)
            return

        old_days = USERS.find_one({'user_id': user_id, 'chat_id': chat_id}).get('days')
        USERS.update_one({'user_id': user_id},
                         {'$set': {'days': int(days) + int(old_days),
                                   'method': pay_method,
                                   'status': 'active',
                                   'chat_id': chat_id}})
        return

    async def add_chat_id(self, user_id, chat_id):
        """
        Add chat id to user
        """
        USERS.update_one({'user_id': user_id},
                         {'$push': {'chat_id': chat_id}}, upsert=True)

    async def get_user_status(self, user_id, chat_id):
        """
        Return user status
        """
        if USERS.find_one({'user_id': user_id, 'chat_id': chat_id}) is None:
            return
        return USERS.find_one({'user_id': user_id, 'chat_id': chat_id}).get('status')

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
