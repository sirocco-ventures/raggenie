# import pytest
# from unittest.mock import patch
# from fastapi.testclient import TestClient
# from app.schemas.provider import CredentialsHelper


# @pytest.mark.usefixtures("client")
# class TestProviderAPI:

#     @pytest.mark.parametrize(
#         "mock_return_value, error, expected_response, expected_status_code",
#         [
#             # Success case
#             ([{"id": 1, "name": "Provider A"}], None, {
#                 "status": True,
#                 "status_code": 200,
#                 "data": {"providers": [{"id": 1, "name": "Provider A"}]},
#                 "message": "Providers Found",
#                 "error": None
#             }, 200),
#             # Empty provider case
#             ([], None, {
#                 "status": True,
#                 "status_code": 200,
#                 "data": {"providers": []},
#                 "message": "Providers Not Found",
#                 "error": "Not Found"
#             }, 200),
#             # Database error case
#             ("SQL Error", "DB error", {
#                 "status": False,
#                 "status_code": 422,
#                 "data": {"providers": []},
#                 "message": "DB error",
#                 "error": "SQL Error"
#             }, 200)
#         ]
#     )
#     @patch('app.services.provider.list_providers')
#     def test_list_providers(self, mock_list_providers, client: TestClient, mock_return_value, error, expected_response, expected_status_code):
#         mock_list_providers.return_value = (mock_return_value, error)

#         response = client.get("/api/v1/provider/list")

#         assert response.status_code == expected_status_code
#         assert response.json() == expected_response

#     @pytest.mark.parametrize(
#         "mock_return_value, error, expected_response, expected_status_code",
#         [
#             # Success case
#             ({"id": 1, "name": "Provider A"}, None, {
#                 "status": True,
#                 "status_code": 200,
#                 "data": {"provider": {"id": 1, "name": "Provider A"}},
#                 "message": "Provider Found",
#                 "error": None
#             }, 200),
#             # Provider not found case
#             ({}, None, {
#                 "status": True,
#                 "status_code": 200,
#                 "data": {"provider": {}},
#                 "message": "Providers Not Found",
#                 "error": "Not Found"
#             }, 200),
#             # Database error case
#             ("DB Error", "DB Error", {
#                 "status": False,
#                 "status_code": 422,
#                 "data": {"provider": {}},
#                 "message": "DB error",
#                 "error": "DB Error"
#             }, 200)
#         ]
#     )
#     @patch('app.services.provider.get_provider')
#     def test_get_provider(self, mock_get_provider, client: TestClient, mock_return_value, error, expected_response, expected_status_code):
#         mock_get_provider.return_value = (mock_return_value, error)

#         response = client.get("/api/v1/provider/get/1")

#         assert response.status_code == expected_status_code
#         assert response.json() == expected_response

#     @pytest.mark.parametrize(
#         "mock_return_value, error, expected_response, expected_status_code",
#         [
#             # Success case
#             (True, "Test Credentials successfully completed", {
#                 "status": True,
#                 "status_code": 200,
#                 "message": "Test Credentials successfully completed",
#                 "error": None,
#                 "data": None,
#             }, 200),
#             # Provider not found case
#             (None, "Provider Not Found", {
#                 "status": False,
#                 "status_code": 422,
#                 "message": "Provider Not Found",
#                 "error": "Provider Not Found",
#                 "data": None,
#             }, 200),
#             # Failed to get provider configurations case
#             (None, "Failed to get provider configurations", {
#                 "status": False,
#                 "status_code": 422,
#                 "message": "Failed to get provider configurations",
#                 "error": "Failed to get provider configurations",
#                 "data": None,
#             }, 200),
#             # Unsupported provider case
#             (None, "Unsupported Provider", {
#                 "status": False,
#                 "status_code": 422,
#                 "message": "Unsupported Provider",
#                 "error": "Unsupported Provider",
#                 "data": None,
#             }, 200),
#             # Missing required key case
#             (None, "Missing required config key: key", {
#                 "status": False,
#                 "status_code": 422,
#                 "message": "Missing required config key: key",
#                 "error": "Missing required config key: key",
#                 "data": None,
#             }, 200),
#             # Failed to connect case
#             (None, "Test Credentials Failed: Connection error", {
#                 "status": False,
#                 "status_code": 422,
#                 "message": "Test Credentials Failed: Connection error",
#                 "error": "Test Credentials Failed: Connection error",
#                 "data": None,
#             }, 200),
#         ]
#     )
#     @patch('app.services.provider.test_credentials')
#     def test_test_connections(self, mock_test_credentials, client: TestClient, mock_return_value, error, expected_response, expected_status_code):
#         mock_test_credentials.return_value = (mock_return_value, error)

#         credentials = CredentialsHelper(provider_config={"key": "value"})
#         response = client.post("/api/v1/provider/1/test-credentials", json=credentials.model_dump())

#         assert response.status_code == expected_status_code
#         assert response.json() == expected_response

#     @pytest.mark.parametrize(
#         "mock_return_value, is_error, expected_response, expected_status_code",
#         [
#             # Success case
#             ({"llm_providers": ["Provider A"]}, False, {
#                 "status": True,
#                 "status_code": 200,
#                 "message": "LLM providers found",
#                 "data": {"llm_providers": ["Provider A"]},
#                 "error": None
#             }, 200),
#             # Not found case
#             (None, True, {
#                 "status": False,
#                 "status_code": 422,
#                 "message": "LLM providers not found",
#                 "data": None,
#                 "error": None
#             }, 200),
#         ]
#     )
#     @patch('app.services.provider.getllmproviders')
#     def test_getllmproviders(self, mock_getllmproviders, client: TestClient, mock_return_value, is_error, expected_response, expected_status_code):
#         mock_getllmproviders.return_value = (mock_return_value, is_error)

#         response = client.get("/api/v1/provider/llmproviders")

#         assert response.status_code == expected_status_code
#         assert response.json() == expected_response
