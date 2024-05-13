import json
import datetime
from flask import Flask, jsonify, request
from marshmallow import ValidationError, Schema, fields, validates_schema
from user_moods.model.moods import Mood
from user_moods.schema.moods_schema import MoodSchema

app = Flask(__name__)

# Sample dummy data for moods
moods = {
    1: [
        {"date": "2024-05-01", "mood": 4},
        {"date": "2024-05-02", "mood": 3},
    ],
    2: [{"date": "2024-05-03", "mood": 5}],
}


@app.route("/moods")
def get_moods():
    # get user_id from query parameters
    user_id = request.args.get("user_id")
    if user_id is None:
        return jsonify({"error": {"detail": "user_id parameter is required"}}), 400
    
    # Ensure user_id is an integer
    try:
        user_id = int(user_id)
    except ValueError:
        return jsonify({"error": {"detail": "user_id must be an integer"}}), 400

    # Check if user_id exists in moods dictionary
    if user_id not in moods:
        return jsonify({"error": {"detail": "No moods found for user_id {}".format(user_id)}}), 404

    user_moods = moods[user_id]

    # Calculate average mood (handle division by zero)
    if len(user_moods) > 0:
        avg_mood = sum(mood["mood"] for mood in user_moods) / len(user_moods)
    else:
        avg_mood = None

    # Serialize moods
    user_moods_response = [
        {"date": format_date(mood["date"]), "mood": mood["mood"]} for mood in user_moods
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

    return json.dumps(response_data, sort_keys=False)


@app.route("/moods", methods=["POST"])
def add_mood():
    # Extract JSON data from request body
    request_data = request.get_json()

    # Check if 'user_id' is present in the request data
    if 'user_id' not in request_data:
        return jsonify({"error": {"detail": "user_id is missing"}}), 400

    # Load the JSON data into MoodSchema
    try:
        mood_data = MoodSchema().load(request_data)
    except ValidationError as err:
        return jsonify({"error": {"detail": err.messages}}), 400

    # Get the user_id from the validated data
    user_id = mood_data["user_id"]

    # Check if user_id exists in moods dictionary (create an empty list if not)
    if user_id not in moods:
        moods[user_id] = []

    # Create a new Mood object (optional, can modify based on your model)
    new_mood = {"date": mood_data["date"], "mood": mood_data["mood"]}

    # Add the new mood to the user's mood list
    moods[user_id].append(new_mood)

    return "", 201  # Created (empty response)

def format_date(date_value):
    if isinstance(date_value, datetime.date):
        return date_value.strftime("%Y-%m-%d")  
    else:
        return date_value


if __name__ == "__main__":
    app.run()