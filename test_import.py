from flask import current_app, request
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

print(current_app)