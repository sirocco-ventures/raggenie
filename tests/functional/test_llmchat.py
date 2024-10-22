import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient

@pytest.mark.usefixtures("client")
class TestLLMChat:

    # Fixture to provide a sample chat payload for tests
    @pytest.fixture
    def chat_payload(self):
        return {
            "chat_context_id": "context_1",
            "chat_query": "What is AI?",
            "chat_answer": {"response": "Artificial Intelligence"},
            "chat_summary": "Summary",
            "user_id": 123,
            "primary_chat": True
        }

    # Fixture to provide a sample feedback payload for tests
    @pytest.fixture
    def feedback_payload(self):
        return {
            "chat_context_id": "context_1",
            "chat_id": 1,
            "feedback_status": 1,
            "feedback_json": {"feedback": "Good"}
        }

    # Test case for creating a chat
    @pytest.mark.parametrize(
        "mock_return_value, error, expected_response, expected_status_code",
        [
            ({"chat_id": 1}, None, {
                "status": True,
                "status_code": 201,
                "message": "Chat created successfully",
                "data": {"chat": {"chat_id": 1}},
                "error": None
            }, 200),
            ("DB Error", "DB Error", {
                "status": False,
                "status_code": 422,
                "message": "DB Error",
                "data": {"chat": {}},
                "error": "DB Error"
            }, 200)
        ]
    )
    @patch('app.services.llmchat.create_chat')  # Mock the create_chat function
    def test_create_chat(self, mock_create_chat, client: TestClient, chat_payload, mock_return_value, error, expected_response, expected_status_code):
        mock_create_chat.return_value = (mock_return_value, error)  # Set mock return values

        response = client.post("/api/v1/chat/create", json=chat_payload)  # Make POST request

        # Assertions to verify the response status code and body
        assert response.status_code == expected_status_code
        assert response.json() == expected_response

    # Test case for creating feedback
    @pytest.mark.parametrize(
        "mock_return_value, error, expected_response, expected_status_code",
        [
            ({"chat_id": 1}, None, {
                "status": True,
                "status_code": 200,
                "message": "Feedback updated successfully",
                "data": {"chat": {"chat_id": 1}},
                "error": None
            }, 200),
            ("DB Error", "DB Error", {
                "status": False,
                "status_code": 422,
                "message": "DB Error",
                "data": {"chat": {}},
                "error": "DB Error"
            }, 200),
            (None, None, {
                "status": True,
                "status_code": 200,
                "message": "Chat Not Found",
                "data": {"chat": {}},
                "error": "Not Found"
            }, 200)
        ]
    )
    @patch('app.services.llmchat.create_feedback')  # Mock the create_feedback function
    def test_create_feedback(self, mock_create_feedback, client: TestClient, feedback_payload, mock_return_value, error, expected_response, expected_status_code):
        mock_create_feedback.return_value = (mock_return_value, error)  # Set mock return values

        response = client.post("/api/v1/chat/feedback/create", json=feedback_payload)  # Make POST request

        # Assertions to verify the response status code and body
        assert response.status_code == expected_status_code
        assert response.json() == expected_response

    # Test case for listing chats by context
    @pytest.mark.parametrize(
        "mock_return_value, error, expected_response, expected_status_code",
        [
            ([{"key": "value"}], None, {
                "status": True,
                "status_code": 200,
                "message": "Primary chats found",
                "data": {"chats": [{"key": "value"}]},
                "error": None
            }, 200),
            ([], None, {
                "status": True,
                "status_code": 200,
                "message": "Context Not found",
                "data": {"chats": []},
                "error": "Not Found"
            }, 200),
            ("DB Error", "DB Error", {
                "status": False,
                "status_code": 422,
                "message": "DB Error",
                "data": {"chats": []},
                "error": "DB Error"
            }, 200)
        ]
    )
    @patch('app.services.llmchat.list_chats_by_context')  # Mock the list_chats_by_context function
    def test_list_chats_by_context(self, mock_list_chats_by_context, client: TestClient, mock_return_value, error, expected_response, expected_status_code):
        mock_list_chats_by_context.return_value = (mock_return_value, error)  # Set mock return values

        response = client.get("/api/v1/chat/list/context/all")  # Make GET request

        # Assertions to verify the response status code and body
        assert response.status_code == expected_status_code
        assert response.json() == expected_response

    # Test case for getting chat by context ID
    @pytest.mark.parametrize(
        "mock_return_value, error, expected_response, expected_status_code",
        [
            ([{"key": "value"}], None, {
                "status": True,
                "status_code": 200,
                "message": "Chat found",
                "data": {"chats": [{"key": "value"}]},
                "error": None
            }, 200),
            ([], None, {
                "status": True,
                "status_code": 200,
                "message": "Chat not found",
                "data": {"chats": []},
                "error": "Not Found"
            }, 200),
            ("DB Error", "DB Error", {
                "status": False,
                "status_code": 422,
                "message": "DB Error",
                "data": {"chats": []},
                "error": "DB Error"
            }, 200)
        ]
    )
    @patch('app.services.llmchat.list_all_chats_by_context_id')  # Mock the list_all_chats_by_context_id function
    def test_get_chat_by_context(self, mock_list_all_chats_by_context_id, client: TestClient, mock_return_value, error, expected_response, expected_status_code):
        mock_list_all_chats_by_context_id.return_value = (mock_return_value, error)  # Set mock return values

        response = client.get("/api/v1/chat/get/context_1")  # Make GET request

        # Assertions to verify the response status code and body
        assert response.status_code == expected_status_code
        assert response.json() == expected_response
