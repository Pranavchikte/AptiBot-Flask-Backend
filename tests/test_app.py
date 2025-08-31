import pytest
from app import create_app
from unittest.mock import patch

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app = create_app()
    yield app

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

def test_index_route(client):
    """Tests the health check route."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"AptiBot server is up and running" in response.data

def test_create_session_endpoint(client):
    """Tests the session creation endpoint."""
    response = client.post('/api/sessions')
    assert response.status_code == 200
    json_data = response.get_json()
    assert 'session_id' in json_data

@patch('app.solve_problem')
def test_chat_message_endpoint(mock_solve_problem, client):
    """
    GIVEN a session and a mocked AI
    WHEN a message is sent to the chat endpoint
    THEN check that the response is valid and the AI was called correctly
    """
    mock_solve_problem.return_value = "This is a mocked AI solution."

    session_response = client.post('/api/sessions')
    session_id = session_response.get_json()['session_id']

    chat_response = client.post(
        f'/api/sessions/{session_id}/messages',
        json={'query': 'What is 2+2?'}
    )
    
    assert chat_response.status_code == 200
    json_data = chat_response.get_json()
    assert json_data['solution'] == "This is a mocked AI solution."
    
    mock_solve_problem.assert_called_once()