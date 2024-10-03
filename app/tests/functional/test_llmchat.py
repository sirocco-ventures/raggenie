# import pytest
# from unittest.mock import patch
# from fastapi.testclient import TestClient

# @pytest.mark.usefixtures("client")
# class TestLLMChat:

#     @pytest.fixture
#     def chat_payload(self):
#         return {
#             "chat_context_id": "context_1",
#             "chat_query": "What is AI?",
#             "chat_answer": {"response": "Artificial Intelligence"},
#             "chat_summary": "Summary",
#             "user_id": 123,
#             "primary_chat": True
#         }

#     @pytest.fixture
#     def feedback_payload(self):
#         return {
#             "chat_context_id": "context_1",
#             "chat_id": 1,
#             "feedback_status": 1,
#             "feedback_json": {"feedback": "Good"}
#         }

#     @pytest.mark.parametrize(
#         "mock_return_value, error, expected_response, expected_status_code",
#         [
#             ({"chat_id": 1}, None, {
#                 "status": True,
#                 "status_code": 201,
#                 "message": "Chat created successfully",
#                 "data": {"chat": {"chat_id": 1}},
#                 "error": None
#             }, 200),
#             ("DB Error", "DB Error", {
#                 "status": False,
#                 "status_code": 422,
#                 "message": "DB Error",
#                 "data": {"chat": {}},
#                 "error": "DB Error"
#             }, 200)
#         ]
#     )
#     @patch('app.services.llmchat.create_chat')
#     def test_create_chat(self, mock_create_chat, client: TestClient, chat_payload, mock_return_value, error, expected_response, expected_status_code):
#         mock_create_chat.return_value = (mock_return_value, error)

#         response = client.post("/api/v1/chat/create", json=chat_payload)

#         assert response.status_code == expected_status_code
#         assert response.json() == expected_response

#     @pytest.mark.parametrize(
#         "mock_return_value, error, expected_response, expected_status_code",
#         [
#             ({"chat_id": 1}, None, {
#                 "status": True,
#                 "status_code": 200,
#                 "message": "Feedback updated successfully",
#                 "data": {"chat": {"chat_id": 1}},
#                 "error": None
#             }, 200),
#             ("DB Error", "DB Error", {
#                 "status": False,
#                 "status_code": 422,
#                 "message": "DB Error",
#                 "data": {"chat": {}},
#                 "error": "DB Error"
#             }, 200),
#             (None, None, {
#                 "status": True,
#                 "status_code": 200,
#                 "message": "Chat Not Found",
#                 "data": {"chat": {}},
#                 "error": "Not Found"
#             }, 200)
#         ]
#     )
#     @patch('app.services.llmchat.create_feedback')
#     def test_create_feedback(self, mock_create_feedback, client: TestClient, feedback_payload, mock_return_value, error, expected_response, expected_status_code):
#         mock_create_feedback.return_value = (mock_return_value, error)

#         response = client.post("/api/v1/chat/feedback/create", json=feedback_payload)

#         assert response.status_code == expected_status_code
#         assert response.json() == expected_response

#     @pytest.mark.parametrize(
#         "mock_return_value, error, expected_response, expected_status_code",
#         [
#             ([{"key": "value"}], None, {
#                 "status": True,
#                 "status_code": 200,
#                 "message": "Primary chats found",
#                 "data": {"chats": [{"key": "value"}]},
#                 "error": None
#             }, 200),
#             ([], None, {
#                 "status": True,
#                 "status_code": 200,
#                 "message": "Context Not found",
#                 "data": {"chats": []},
#                 "error": "Not Found"
#             }, 200),
#             ("DB Error", "DB Error", {
#                 "status": False,
#                 "status_code": 422,
#                 "message": "DB Error",
#                 "data": {"chats": []},
#                 "error": "DB Error"
#             }, 200)
#         ]
#     )
#     @patch('app.services.llmchat.list_chats_by_context')
#     def test_list_chats_by_context(self, mock_list_chats_by_context, client: TestClient, mock_return_value, error, expected_response, expected_status_code):
#         mock_list_chats_by_context.return_value = (mock_return_value, error)

#         response = client.get("/api/v1/chat/list/context/all")

#         assert response.status_code == expected_status_code
#         assert response.json() == expected_response

#     @pytest.mark.parametrize(
#         "mock_return_value, error, expected_response, expected_status_code",
#         [
#             ([{"key": "value"}], None, {
#                 "status": True,
#                 "status_code": 200,
#                 "message": "Chat found",
#                 "data": {"chats": [{"key": "value"}]},
#                 "error": None
#             }, 200),
#             ([], None, {
#                 "status": True,
#                 "status_code": 200,
#                 "message": "Chat not found",
#                 "data": {"chats": []},
#                 "error": "Not Found"
#             }, 200),
#             ("DB Error", "DB Error", {
#                 "status": False,
#                 "status_code": 422,
#                 "message": "DB Error",
#                 "data": {"chats": []},
#                 "error": "DB Error"
#             }, 200)
#         ]
#     )
#     @patch('app.services.llmchat.list_all_chats_by_context_id')
#     def test_get_chat_by_context(self, mock_list_all_chats_by_context_id, client: TestClient, mock_return_value, error, expected_response, expected_status_code):
#         mock_list_all_chats_by_context_id.return_value = (mock_return_value, error)

#         response = client.get("/api/v1/chat/get/context_1")

#         assert response.status_code == expected_status_code
#         assert response.json() == expected_response
