from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

def current_date():
    return datetime.datetime.now(datetime.timezone.utc).date()

class Mood(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mood = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False, default=current_date)

    def __repr__(self):
        return f'<Mood(id={self.id}, mood={self.mood}, user_id={self.user_id}, date={self.date})>'
