#!/usr/bin/env python3
""" Simple flask app."""

from flask import Flask, render_template, request, g
from flask_babel import Babel
from config import Config


app: Flask = Flask(__name__)
app.config.from_object(Config)
babel: Babel = Babel(app)

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user() -> dict:
    """ Returns a user dictionary or
        None if the ID cannot be found.
    """
    try:
        return users.get(int(request.args.get('login_as')))
    except Exception:
        return None


@app.before_request
def before_request() -> None:
    """ Find a user if any, and set it as a flask.global
    """
    user: dict = get_user()
    g.user: g = user


@babel.localeselector
def get_locale() -> str:
    """ Determine the best match with our supported languages.
    """
    locale: str = request.args.get('locale')
    if locale in app.config['LANGUAGES']:
        return locale
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/', methods=['GET'], strict_slashes=False)
def index() -> str:
    """ GET /
        Return: 0-index.html
    """
    return render_template('5-index.html')


if __name__ == "__main__":
    app.run(host="localhost", port=5001)
