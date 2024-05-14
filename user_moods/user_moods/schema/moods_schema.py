from marshmallow import Schema, fields, ValidationError
import datetime as dt

class MoodSchema(Schema):
    user_id = fields.Int(required=True)
    mood = fields.Int(
        required=True,
        validate=lambda x: x > 0 and x <= 5,
        error_messages={
            "required": "Mood is required.",
            "validator_failed": "Mood must be an integer between 1 and 5."
        }
    )
    date = fields.Date(format="%Y-%m-%d")

    def validate_date(self, data, **kwargs):
        if data["date"] > dt.date.today():
            raise ValidationError("Date cannot be in the future.")
