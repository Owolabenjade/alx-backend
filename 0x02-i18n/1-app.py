#!/usr/bin/env python3
"""
Flask application with Babel internationalization support.

This module creates a Flask web application with Babel integration
for internationalization and localization features.
"""

from flask import Flask, render_template
from flask_babel import Babel


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


@app.route('/')
def index() -> str:
    """
    Handle the root route and render the index template.
    
    Returns:
        str: Rendered HTML template for the index page.
    """
    return render_template('1-index.html')


if __name__ == '__main__':
    app.run(debug=True)