#!/usr/bin/env python3
"""
Flask application with Babel internationalization and translation support.

This module creates a Flask web application with Babel integration
for internationalization features including automatic locale detection
and message translation using gettext.
"""

from flask import Flask, render_template, request
from flask_babel import Babel, gettext


class Config:
    """
    Configuration class for Flask application.
    
    This class contains configuration settings for the Flask app
    including supported languages, default locale, and timezone.
    """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)

babel = Babel(app)


@babel.localeselector
def get_locale() -> str:
    """
    Select the best matching locale for the user.
    
    This function uses the request's Accept-Language header to determine
    the best matching language from the supported languages list.
    
    Returns:
        str: The best matching locale code (e.g., 'en' or 'fr').
    """
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/')
def index() -> str:
    """
    Handle the root route and render the index template.
    
    Returns:
        str: Rendered HTML template for the index page with translations.
    """
    return render_template('3-index.html')


if __name__ == '__main__':
    app.run(debug=True)