import json
import datetime
import os
from flask import Flask, jsonify, request
from flask.views import MethodView
from flasgger import Swagger
from marshmallow import ValidationError
from user_mood.user_moods.schema import MoodSchema
from user_mood.user_moods.model import Mood
from user_mood.user_moods import db
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db.init_app(app)

migrate = Migrate(app, db)
swagger = Swagger(app, template_file='swagger.yaml')

# Utility functions
def format_date(date_value):
    if isinstance(date_value, datetime.date):
        return date_value.strftime("%Y-%m-%d")
    else:
        return date_value

# API class for /moods endpoint
class MoodAPI(MethodView):
    # GET method for retrieving mood data
    def get(self):
        user_id = request.args.get("user_id")
        if user_id is None:
            return jsonify({"error": {"detail": "user_id parameter is required"}}), 400

        try:
            user_id = int(user_id)
        except ValueError:
            return jsonify({"error": {"detail": "user_id must be an integer"}}), 400

        user_moods = Mood.query.filter_by(user_id=user_id).all()

        if not user_moods:
            return jsonify({"error": {"detail": f"No moods found for user_id {user_id}"}}), 404

        avg_mood = sum(mood.mood for mood in user_moods) / len(user_moods) if user_moods else None

        user_moods_response = [
            {"date": format_date(mood.date), "mood": mood.mood} for mood in user_moods
        ]

        response_data = {
            "data": {
                "id": user_id,
                "type": "moods",
                "attributes": {
                    "avg_mood": avg_mood,
                    "user_moods": user_moods_response
                }
            }
        }

        json_response = json.dumps(response_data, ensure_ascii=False)

        return json_response

    # POST method for adding a new mood entry
    def post(self):
        request_data = request.get_json()

        if 'user_id' not in request_data:
            return jsonify({"error": {"detail": "user_id is missing"}}), 400

        try:
            mood_data = MoodSchema().load(request_data)
        except ValidationError as err:
            return jsonify({"error": {"detail": err.messages}}), 400

        user_id = mood_data["user_id"]
        date = mood_data["date"]
        mood = mood_data["mood"]

        new_mood = Mood(user_id=user_id, date=date, mood=mood)
        db.session.add(new_mood)
        db.session.commit()

        return "", 201

# Add URL rules for /moods endpoint
app.add_url_rule('/moods', view_func=MoodAPI.as_view('mood_api'))

if __name__ == "__main__":
    app.run(debug=False)
