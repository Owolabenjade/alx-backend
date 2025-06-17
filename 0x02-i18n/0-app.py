#!/usr/bin/env python3
"""
Basic Flask application module.

This module creates a simple Flask web application with a single route
that renders a welcome page using a template.
"""

from flask import Flask, render_template


app = Flask(__name__)


@app.route('/')
def index() -> str:
    """
    Handle the root route and render the index template.
    
    Returns:
        str: Rendered HTML template for the index page.
    """
    return render_template('0-index.html')


if __name__ == '__main__':
    app.run(debug=True)