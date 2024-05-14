import json
import pytest
import requests_mock
from user_moods.index import app

# Fixture to create a test client for the Flask app
@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

# Test case for GET /moods endpoint with valid user_id
def test_get_moods_valid_user_id(client):
    with requests_mock.Mocker() as m:
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

        m.get('http://localhost:5000/moods?user_id=1', json=expected_response)

        response = client.get('/moods?user_id=1')

        assert response.status_code == 200
        assert response.data.decode('utf-8') == json.dumps(expected_response)


# Test case for GET /moods endpoint with invalid user_id
def test_get_moods_invalid_user_id(client):
    with requests_mock.Mocker() as m:
        expected_response = {"error": {"detail": "No moods found for user_id 999"}}
        m.get('http://localhost:5000/moods?user_id=999', json=expected_response, status_code=404)

        response = client.get('/moods?user_id=999')

        assert response.status_code == 404
        assert response.json == expected_response

# Test case for POST /moods endpoint
import json

# Test case for POST /moods endpoint
def test_add_mood(client):
    with requests_mock.Mocker() as m:
        # Mock the response from the server
        m.post('http://localhost:5000/moods', status_code=201)
        
        # Define the request data
        request_data = {
            "user_id": 1,
            "mood": 3,
            "date": "2024-05-05"
        }

        # Make the request to the Flask app with the request body
        response = client.post('/moods', json=request_data)
        
        # Verify the response
        assert response.status_code == 201
        assert response.data == b''

if __name__ == "__main__":
    pytest.main()
