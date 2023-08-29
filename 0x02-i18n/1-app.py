#!/usr/bin/env python3
""" Simple flask app."""

from flask import Flask, render_template
from flask_babel import Babel
from config import Config


app: Flask = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)


@app.route('/', methods=['GET'], strict_slashes=False)
def index() -> str:
    """ GET /
        Return: 0-index.html
    """
    return render_template('1-index.html')


if __name__ == "__main__":
    app.run(host="localhost", port=5001)
