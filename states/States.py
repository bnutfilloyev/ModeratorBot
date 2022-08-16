from aiogram.dispatcher.filters.state import StatesGroup, State


class AddGroup(StatesGroup):
    GetGroupName = State()
    GetGroupId = State()
    GetAdminIds = State()


class RemoveGroup(StatesGroup):
    GetGroupName = State()
