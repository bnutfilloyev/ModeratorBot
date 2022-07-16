from pathlib import Path

from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
ADMINS = env.list("ADMINS")
IP = env.str("IP")
CLICK_PROVIDER_TOKEN = env.str("CLICK_PROVIDER_TOKEN")
PAYME_PROVIDER_TOKEN = env.str("PAYME_PROVIDER_TOKEN")

I18N_DOMAIN = 'moderatorbot'

BASE_DIR = Path(__file__).parent
LOCALES_DIR = BASE_DIR / 'locales'

LANGUAGES = ['uz', 'ru']

METHODS = {
    "click": "🇺🇿 Click",
    "payme": "🇺🇿 Payme",
}
