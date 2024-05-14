# Import necessary modules
import datetime as dt
from marshmallow import ValidationError
from user_moods.schema import MoodSchema
from user_moods.model import Mood
from app import db

# Test the MoodSchema class
def test_mood_schema():
    # Create an instance of MoodSchema
    schema = MoodSchema()

    # Test valid data
    valid_data = {"user_id": 1, "mood": 3, "date": "2024-05-13"}
    result = schema.load(valid_data)
    assert result == {"user_id": 1, "mood": 3, "date": dt.date(2024, 5, 13)}

    # Test invalid data (missing user_id)
    invalid_data = {"mood": 3, "date": "2024-05-13"}
    try:
        schema.load(invalid_data)
    except ValidationError as err:
        assert "'user_id': ['Missing data for required field.']" in str(err)

    # Test invalid data (invalid mood)
    invalid_data = {"user_id": 1, "mood": 6, "date": "2024-05-13"}
    try:
        schema.load(invalid_data)
    except ValidationError as err:
        assert "Mood must be an integer between 1 and 5." in str(err)

    # Test invalid data (future date)
    invalid_data = {"user_id": 1, "mood": 3, "date": "2025-05-13"}
    try:
        schema.load(invalid_data)
    except ValidationError as err:
        assert "Date cannot be in the future." in str(err)

# Test the Mood class
def test_mood_class():
    today = dt.date.today()
    mood = Mood(mood=3, user_id=1, date=today)
    assert mood.date == today

    specified_date = dt.date(2024, 5, 13)
    mood = Mood(mood=3, user_id=1, date=specified_date)
    assert mood.date == specified_date


# Run the tests
test_mood_schema()
test_mood_class()
