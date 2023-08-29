#!/usr/bin/env python3
""" Simple flask app."""

from flask import Flask, render_template, request, g
from flask_babel import Babel
from config import Config
from pytz import timezone, exceptions, utc
from datetime import datetime
import locale

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
    g.user = user
    tz = timezone(get_timezone())
    current_time: datetime = tz.localize(datetime.utcnow())
    fmt: str = "%b %d, %Y %I:%M:%S %p"
    g.current_time: datetime = current_time.strftime(fmt)


@babel.localeselector
def get_locale() -> str:
    """ Determine the best match with our supported languages.
    """
    locale: str = request.args.get('locale')
    if locale in app.config['LANGUAGES']:
        return locale
    if g.user:
        locale = g.user.get('locale')
        if locale and locale in app.config['LANGUAGES']:
            return locale
    # get locale from request headers
    locale = request.headers.get('locale')
    if locale in app.config['LANGUAGES']:
        return locale
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@babel.timezoneselector
def get_timezone() -> str:
    """ get time zone
    """
    tz: str = request.args.get('timezone', None)
    if tz:
        try:
            return timezone(tz).zone
        except exceptions.UnknownTimeZoneError:
            pass
    if g.user:
        try:
            tz = g.user.get('timezone')
            return timezone(tz).zone
        except exceptions.UnknownTimeZoneError:
            pass
    default_tz: str = app.config['BABEL_DEFAULT_TIMEZONE']
    return default_tz


@app.route('/', methods=['GET'], strict_slashes=False)
def index() -> str:
    """ GET /
        Return: 0-index.html
    """
    return render_template('index.html')


if __name__ == "__main__":
    app.run(host="localhost", port=5001)
