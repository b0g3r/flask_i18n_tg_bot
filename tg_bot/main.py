import os
import uuid

import telepot
from flask import Flask, request, g
from flask_babel import Babel
from flask_babel import gettext as _

token = os.environ['BOT_TOKEN']
secret = uuid.uuid1().hex
host = 'https://b319542c.ngrok.io'

app = Flask('flask_i18n_tg_bot')
app.config['BABEL_DEFAULT_LOCALE'] = 'ru'

babel = Babel(app)
bot = telepot.Bot(token)

users = {}

@babel.localeselector
def get_locale():
    user_lang_code = telegram_lang_code = None
    if g.get('update'):
        user_lang_code = users.get(g.update['message']['from']['id'], {}).get(
            'lang_code')
        telegram_lang_code = g.update['message']['from'].get(
            'language_code').split('-', 1)[0]
    lang_code = user_lang_code or telegram_lang_code or None
    print(lang_code)
    return lang_code


@app.route('/{}'.format(secret), methods=['POST', 'GET'])
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

bot.setWebhook('{0}/{1}'.format(host, secret))
app.run()
