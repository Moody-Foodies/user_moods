#!/bin/sh

# Set the FLASK_APP environment variable to point to your Flask application
export FLASK_APP=app.py

# Run the Flask server with debugging enabled
pipenv run flask run -h 0.0.0.0 --reload
