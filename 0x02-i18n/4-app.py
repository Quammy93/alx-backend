#!/usr/bin/env python3
"""Flask app for i18n and l10n."""

from flask import Flask, render_template, request
from flask_babel import Babel


app = Flask(__name__)
application = app
babel = Babel(app)


class Config(object):
    """Accepted languages."""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app.config.from_object(Config)


@babel.localeselector
def get_locale():
    """Get the locale that is best matched."""
    locale = request.values.get("locale")
    if locale and locale in app.config["LANGUAGES"]:
        return locale
    return request.accept_languages.best_match(
        app.config["LANGUAGES"]
    )


@app.route("/", methods=["GET"])
def index():
    """Entry route."""
    return render_template("4-index.html")


if __name__ == "__main__":
    application.run(debug=True)
