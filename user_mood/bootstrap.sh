
#!/bin/sh

# Set the FLASK_APP environment variable to point to your Flask application
export FLASK_APP=app.py

# Run the Flask server with Gunicorn
pipenv run gunicorn -w 4 -b 0.0.0.0:5000 app:app

