# README

Welcome to the Flask Localization Guide! This README will walk you through the steps needed to:

1. Parametrize Flask templates to display different languages.
2. Infer the correct locale based on URL parameters, user settings, or request headers.
3. Localize timestamps.

## Introduction

Localization is crucial for creating applications that cater to a global audience. This guide will help you configure your Flask application to support multiple languages and locales, making your app more user-friendly and accessible.

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.x
- Flask
- Flask-Babel (or any other localization library)
- Babel (for translations)

You can install Flask and Flask-Babel using pip:

```bash
pip install Flask Flask-Babel
```

## Parametrize Flask Templates

To display different languages in your Flask templates, follow these steps:

1. **Set up Flask-Babel in your Flask app**:

    ```python
    from flask import Flask
    from flask_babel import Babel

    app = Flask(__name__)
    babel = Babel(app)
    ```

2. **Configure the available languages**:

    ```python
    app.config['BABEL_DEFAULT_LOCALE'] = 'en'
    app.config['BABEL_SUPPORTED_LOCALES'] = ['en', 'es', 'fr']
    ```

3. **Create translation files** using Babel commands:

    ```bash
    pybabel extract -F babel.cfg -o messages.pot .
    pybabel init -i messages.pot -d translations -l es
    pybabel init -i messages.pot -d translations -l fr
    ```

4. **Translate the messages** in the `.po` files located in the `translations` directory.

5. **Compile the translations**:

    ```bash
    pybabel compile -d translations
    ```

6. **Use the `trans` function in your templates**:

    ```html
    <h1>{{ _('Hello, World!') }}</h1>
    ```

## Infer Locale

To infer the correct locale based on URL parameters, user settings, or request headers:

1. **Create a locale selector function**:

    ```python
    @babel.localeselector
    def get_locale():
        # You can replace this with logic to determine the locale
        # For example, from URL parameters:
        return request.args.get('lang', 'en')
    ```

2. **Use the locale in your application**. Flask-Babel will automatically use the selected locale for translations.

## Localize Timestamps

To localize timestamps, you can use Flask-Babel's `format_datetime` function:

1. **Import and use `format_datetime` in your views**:

    ```python
    from flask_babel import format_datetime
    from datetime import datetime

    @app.route('/')
    def index():
        now = datetime.utcnow()
        formatted_time = format_datetime(now)
        return f"<p>{formatted_time}</p>"
    ```

2. **Configure the time formats** in your Flask app configuration if needed:

    ```python
    app.config['BABEL_DEFAULT_TIMEZONE'] = 'UTC'
    app.config['BABEL_DATETIME_FORMATS'] = {
        'datetime': 'medium',
        'date': 'short',
        'time': 'short'
    }
    ```

## Conclusion

By following this guide, you can add robust localization support to your Flask application. Users will appreciate an interface that speaks their language and displays dates and times in their preferred format. Happy coding!

For more information, refer to the [Flask-Babel documentation](https://python-babel.github.io/flask-babel/).
---
