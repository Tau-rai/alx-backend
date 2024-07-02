#!/usr/bin/env python3
"""Module has a flask app"""


from flask import Flask, render_template, request
from flask_babel import Babel, _

app = Flask(__name__)
babel = Babel(app)


class Config:
    """Config class"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app.config.from_object(Config)


@babel.localeselector
def get_locale():
    """Get locale"""
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/')
def index():
    """Index page"""
    home_title = _('Welcome to Holberton')
    home_header = _('Hello world')
    return render_template(
        '1-index.html', title=home_title, header=home_header)


if __name__ == '__main__':
    app.run()
