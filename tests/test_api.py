import json
import pytest
import datetime
from app import app, db

@pytest.fixture
def client():
    app.config['TESTING'] = True
    # comment this out for testing
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()  # Create tables
        yield client
        with app.app_context():
            db.drop_all()  # Drop tables after tests

def test_get_moods_valid_user_id(client):
    with app.app_context():
        from user_moods.model import Mood
        db.session.add(Mood(user_id=1, date=datetime.date(2024, 5, 1), mood=4))
        db.session.add(Mood(user_id=1, date=datetime.date(2024, 5, 2), mood=3))
        db.session.commit()

    response = client.get('/moods?user_id=1')

    expected_response = {
        "data": {
            "id": 1,
            "type": "moods",
            "attributes": {
                "avg_mood": 3.5,
                "user_moods": [
                    {"date": "2024-05-01", "mood": 4},
                    {"date": "2024-05-02", "mood": 3}
                ]
            }
        }
    }

    response_data = json.loads(response.data.decode('utf-8'))
    assert response.status_code == 200
    assert response_data == expected_response

def test_get_moods_invalid_user_id(client):
    response = client.get('/moods?user_id=999')

    expected_response = {"error": {"detail": "No moods found for user_id 999"}}
    assert response.status_code == 404
    assert response.json == expected_response

def test_add_mood(client):
    request_data = {
        "user_id": 1,
        "mood": 3,
        "date": "2024-05-05"
    }

    response = client.post('/moods', json=request_data)
    assert response.status_code == 201

    with app.app_context():
        mood = Mood.query.filter_by(user_id=1, date=datetime.date(2024, 5, 5)).first()
        assert mood is not None
        assert mood.mood == 3

if __name__ == "__main__":
    pytest.main()
