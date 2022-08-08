from urllib.parse import quote_plus

from pymongo import MongoClient
from aiogram.contrib.fsm_storage.mongo import MongoStorage
from data.config import MONGODB_HOSTNAME, MONGO_INITDB_ROOT_USERNAME, MONGO_INITDB_ROOT_PASSWORD, MONGODB_PORT

uri = "mongodb://{}:{}@{}:{}".format(
    quote_plus(MONGO_INITDB_ROOT_USERNAME),
    quote_plus(MONGO_INITDB_ROOT_PASSWORD),
    MONGODB_HOSTNAME,
    MONGODB_PORT
)

client = MongoClient(uri)
storage = MongoStorage()

database = client.moderator

LANG_STORAGE = database['lang_storage']
USERS = database['users']
GROUPS = database['groups']
PAYMENTS = database['payments']
