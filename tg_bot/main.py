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
    # language_code = update['message']['from']['language_code']
    return 'ru'


@app.route('/{}'.format(secret), methods=['POST', 'GET'])
def handler():
    update = request.get_json()

    bot.sendMessage(update['message']['chat']['id'], _('test'))

    return 'ok'

bot.setWebhook('{0}/{1}'.format(host, secret))
app.run()
