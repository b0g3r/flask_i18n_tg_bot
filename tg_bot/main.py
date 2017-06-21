from flask import Flask, request, g
from tg_bot.subapp import subapp

from flask_babel import Babel

app = Flask('flask_i18n_tg_bot')
app.register_blueprint(subapp)

babel = Babel(app)
app.config['BABEL_DEFAULT_LOCALE'] = 'en'


@babel.localeselector
def selector():
    if g.get('locale'):
        return g.locale

app.run()
