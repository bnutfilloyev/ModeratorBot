from datetime import datetime

from utils.db_api.mongo import GROUPS, PAYMENTS, USERS


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
        if pay_method == 'free':
            USERS.update_one({'user_id': user_id, 'chat_id': chat_id},
                             {'$set': {'use_free_plan': False, 'days': int(days)}})
            return

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

    async def use_free_plan(self, user_id, chat_id):
        """
        Use free plan
        """
        if USERS.find_one({'user_id': user_id, 'chat_id': chat_id}) is None:
            return True
        return USERS.find_one({'user_id': user_id, 'chat_id': chat_id}).get('use_free_plan', True)


class Groups:
    def get_groups(self):
        """
        Return groups list
        """
        for group in GROUPS.find():
            yield group

    async def set_groups(self, chat_id, group_name, admin_ids) -> None:
        """
        Set groups for user
        """
        GROUPS.update_one({'chat_id': chat_id},
                          {'$set': {'group_name': group_name, 'admin_id': admin_ids}}, upsert=True)

    async def remove_group(self, chat_id) -> None:
        """
        Remove group
        """
        GROUPS.delete_one({'chat_id': chat_id})

    async def get_group_name(self, chat_id):
        """
        Return group name
        """
        if GROUPS.find_one({'chat_id': chat_id}) is None:
            return

        return GROUPS.find_one({'chat_id': chat_id}).get('group_name')

    @staticmethod
    def get_all_chat_ids(admin_id):
        """
        Return all chat ids for admin
        """
        for group in GROUPS.find({'admin_id': str(admin_id)}):
            print(group)
            yield group.get('chat_id')


class Payments:
    async def add_payment(self, user_id, chat_id, pay_method, amount) -> None:
        """
        Add payment
        """
        PAYMENTS.insert_one({'user_id': user_id,
                             'chat_id': chat_id,
                             'method': pay_method,
                             'amount': amount,
                             'date': datetime.now()})

    async def get_daily_amount(self, chat_id: str) -> float:
        """
        Return yesterday amount
        """
        amount = 0
        if PAYMENTS.find_one({'chat_id': chat_id}) is None:
            return amount
        for payment in PAYMENTS.find({'chat_id': chat_id}):
            print(payment.get('date'))
            # if payment.get('date').split('-')[2] == str(timedelta(days=1))[:2]:
            #     amount += int(payment.get('amount'))
        return amount / 2

    @staticmethod
    async def get_monthly_amount(chat_id: str) -> float:
        """
        Return monthly amount
        """
        amount = 0
        if PAYMENTS.find_one({'chat_id': chat_id}) is None:
            return amount
        for payment in PAYMENTS.find({'chat_id': chat_id}):
            if payment.get('date').split('-')[1] == datetime.now().strftime('%m'):
                amount += int(payment.get('amount'))
        return amount / 2

    async def get_daily_amount(self, chat_id: str) -> float:
        """
        Return yesterday amount
        """
        amount = 0
        if PAYMENTS.find_one({'chat_id': chat_id}) is None:
            return amount
        for payment in PAYMENTS.find({'chat_id': chat_id}):
            print(payment.get('date'))
            # if payment.get('date').split('-')[2] == str(timedelta(days=1))[:2]:
            #     amount += int(payment.get('amount'))
        return amount * 0.7

    @staticmethod
    async def get_monthly_amount(chat_id: str) -> float:
        """
        Return monthly amount
        """
        amount = 0
        if PAYMENTS.find_one({'chat_id': chat_id}) is None:
            return amount
        for payment in PAYMENTS.find({'chat_id': chat_id}):
            if payment.get('date').split('-')[1] == datetime.now().strftime('%m'):
                amount += int(payment.get('amount'))
        return amount * 0.7

    @staticmethod
    async def get_yearly_amount(chat_id: str) -> float:
        """
        Return yearly amount
        """
        amount = 0
        if PAYMENTS.find_one({'chat_id': chat_id}) is None:
            return amount
        for payment in PAYMENTS.find({'chat_id': chat_id}):
            if payment.get('date').split('-')[0] == datetime.now().strftime('%Y'):
                amount += int(payment.get('amount'))
        return amount * 0.7
