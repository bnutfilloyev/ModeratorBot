from pymongo import MongoClient
from aiogram.contrib.fsm_storage.mongo import MongoStorage
from data.config import IP

client = MongoClient(IP)
storage = MongoStorage()

database = client.moderator

LANG_STORAGE = database['lang_storage']
USERS = database['users']
GROUPS = database['groups']
PAYMENTS = database['payments']