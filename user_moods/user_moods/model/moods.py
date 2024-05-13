import datetime as dt

class Mood(object):
  def __init__(self, mood, user_id, date=None):
    self.mood = mood
    self.user_id = user_id
    if date is None:
      self.date = dt.date.today()
    else:
      self.date = dt.datetime.strptime(date, "%Y-%m-%d").date()

  def __repr__(self):
    return '<Mood(mood={self.mood}, user_id={self.user_id}, date={self.date})>'.format(self=self)
  