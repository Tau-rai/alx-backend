#!/usr/bin/env python3
"""Module has a flask app"""


from flask import Flask, render_template, request, g
from flask_babel import Babel, _
import pytz

app = Flask(__name__)
babel = Babel(app)


class Config:
    """Config class"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app.config.from_object(Config)

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}

@babel.localeselector
def get_locale():
    """Get locale"""
    user = getattr(g, 'user', None)

    # Locale from URL parameters
    if request.args.get('locale'):
        return request.args.get('locale')

    # Locale from user settings
    if user is not None and user.locale:
        return user.locale

    # Locale from request header
    return request.accept_languages.best_match(app.config['LANGUAGES'])


def get_user(user_id):
    """Get user"""
    try:
        return users.get(user_id)
    except Exception:
        return None


@babel.timezoneselector
def get_timezone():
    user = getattr(g, 'user', None)
    if user is not None and user.get('timezone'):
        try:
            pytz.timezone(user['timezone'])  # Validate timezone
            return user['timezone']
        except pytz.UnknownTimeZoneError:
            pass  # Invalid timezone, fall back to default
    return 'UTC'  # Default to UTC

@app.before_request
def set_global_user():
    """Set global user"""
    user_id = request.args.get('login_as')
    if user_id:
        user = get_user(int(user_id))
    else:
        user = None
    g.user = user


@app.route('/')
def index():
    """Index page"""
    home_title = _('Welcome to Holberton')
    home_header = _('Hello world!')
    return render_template(
        '7-index.html', title=home_title, header=home_header)


if __name__ == "__main__":
    app.run()