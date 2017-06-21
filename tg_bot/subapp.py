import os
import uuid

import telepot
from flask import Blueprint, request, g
from flask_babel import Babel
from flask_babel import gettext as _


subapp = Blueprint('subapp', __name__)

token = os.environ['BOT_TOKEN']
secret = uuid.uuid1().hex
host = 'https://b319542c.ngrok.io'

bot = telepot.Bot(token)

users = {}


@subapp.before_request
def set_locale():
    user_lang_code = telegram_lang_code = None
    update = request.get_json()
    if update:
        user_lang_code = users.get(update['message']['from']['id'], {}).get(
            'lang_code')
        telegram_lang_code = update['message']['from'].get(
            'language_code').split('-', 1)[0]
    lang_code = user_lang_code or telegram_lang_code or 'en'
    g.locale = lang_code


@subapp.route('/{}'.format(secret), methods=['POST', 'GET'])
def handler():
    g.update = request.get_json()
    text = g.update['message']['text']
    id = g.update['message']['from']['id']

    if text.startswith('/lang'):
        lang_code = text.split()[1]
        users[id] = {'lang_code': lang_code}
    else:
        bot.sendMessage(id, _('test'))

    return 'ok'


@subapp.before_app_first_request
def init():
    bot.setWebhook('{0}/{1}'.format(host, secret))
