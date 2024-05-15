from user_moods.database import db
import datetime

def current_date():
    return datetime.datetime.now(datetime.timezone.utc).date()

class Mood(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    mood = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False, default=current_date)

    def __repr__(self):
        return f'<Mood(id={self.id}, mood={self.mood}, user_id={self.user_id}, date={self.date})>'
