import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from app.schemas.provider import CredentialsHelper

# Use fixtures for client management in tests
@pytest.mark.usefixtures("client")
class TestProviderAPI:

    @pytest.mark.parametrize(
        "mock_return_value, error, expected_response, expected_status_code",
        [
            # Success case: provider found
            ([{"id": 1, "name": "Provider A"}], None, {
                "status": True,
                "status_code": 200,
                "data": {"providers": [{"id": 1, "name": "Provider A"}]},
                "message": "Providers Found",
                "error": None
            }, 200),
            # Empty provider case: no providers found
            ([], None, {
                "status": True,
                "status_code": 200,
                "data": {"providers": []},
                "message": "Providers Not Found",
                "error": "Not Found"
            }, 200),
            # Database error case: simulates a database error
            ("SQL Error", "DB error", {
                "status": False,
                "status_code": 422,
                "data": {"providers": []},
                "message": "DB error",
                "error": "SQL Error"
            }, 200)
        ]
    )
    @patch('app.services.provider.list_providers')  # Mock the list_providers function
    def test_list_providers(self, mock_list_providers, client: TestClient, mock_return_value, error, expected_response, expected_status_code):
        # Set the mock return value for list_providers
        mock_list_providers.return_value = (mock_return_value, error)

        # Send a GET request to the endpoint
        response = client.get("/api/v1/provider/list")

        # Assert the status code and response data match expected values
        assert response.status_code == expected_status_code
        assert response.json() == expected_response

    @pytest.mark.parametrize(
        "mock_return_value, error, expected_response, expected_status_code",
        [
            # Success case: specific provider found
            ({"id": 1, "name": "Provider A"}, None, {
                "status": True,
                "status_code": 200,
                "data": {"provider": {"id": 1, "name": "Provider A"}},
                "message": "Provider Found",
                "error": None
            }, 200),
            # Provider not found case: no provider data returned
            ({}, None, {
                "status": True,
                "status_code": 200,
                "data": {"provider": {}},
                "message": "Providers Not Found",
                "error": "Not Found"
            }, 200),
            # Database error case: simulates a database error
            ("DB Error", "DB Error", {
                "status": False,
                "status_code": 422,
                "data": {"provider": {}},
                "message": "DB error",
                "error": "DB Error"
            }, 200)
        ]
    )
    @patch('app.services.provider.get_provider')  # Mock the get_provider function
    def test_get_provider(self, mock_get_provider, client: TestClient, mock_return_value, error, expected_response, expected_status_code):
        # Set the mock return value for get_provider
        mock_get_provider.return_value = (mock_return_value, error)

        # Send a GET request to the endpoint for a specific provider
        response = client.get("/api/v1/provider/get/1")

        # Assert the status code and response data match expected values
        assert response.status_code == expected_status_code
        assert response.json() == expected_response

    @pytest.mark.parametrize(
        "mock_return_value, error, expected_response, expected_status_code",
        [
            # Success case: credentials test passes
            (True, "Test Credentials successfully completed", {
                "status": True,
                "status_code": 200,
                "message": "Test Credentials successfully completed",
                "error": None,
                "data": None,
            }, 200),
            # Provider not found case: simulates provider not found
            (None, "Provider Not Found", {
                "status": False,
                "status_code": 422,
                "message": "Provider Not Found",
                "error": "Provider Not Found",
                "data": None,
            }, 200),
            # Failed to get provider configurations case
            (None, "Failed to get provider configurations", {
                "status": False,
                "status_code": 422,
                "message": "Failed to get provider configurations",
                "error": "Failed to get provider configurations",
                "data": None,
            }, 200),
            # Unsupported provider case: tests for unsupported provider response
            (None, "Unsupported Provider", {
                "status": False,
                "status_code": 422,
                "message": "Unsupported Provider",
                "error": "Unsupported Provider",
                "data": None,
            }, 200),
            # Missing required key case: checks for missing config key
            (None, "Missing required config key: key", {
                "status": False,
                "status_code": 422,
                "message": "Missing required config key: key",
                "error": "Missing required config key: key",
                "data": None,
            }, 200),
            # Failed to connect case: simulates a connection error during credentials testing
            (None, "Test Credentials Failed: Connection error", {
                "status": False,
                "status_code": 422,
                "message": "Test Credentials Failed: Connection error",
                "error": "Test Credentials Failed: Connection error",
                "data": None,
            }, 200),
        ]
    )
    @patch('app.services.provider.test_credentials')  # Mock the test_credentials function
    def test_test_connections(self, mock_test_credentials, client: TestClient, mock_return_value, error, expected_response, expected_status_code):
        # Set the mock return value for test_credentials
        mock_test_credentials.return_value = (mock_return_value, error)

        # Create credentials data using the CredentialsHelper
        credentials = CredentialsHelper(provider_config={"key": "value"})
        # Send a POST request to test credentials
        response = client.post("/api/v1/provider/1/test-credentials", json=credentials.model_dump())

        # Assert the status code and response data match expected values
        assert response.status_code == expected_status_code
        assert response.json() == expected_response

    @pytest.mark.parametrize(
        "mock_return_value, is_error, expected_response, expected_status_code",
        [
            # Success case: LLM providers found
            ({"llm_providers": ["Provider A"]}, False, {
                "status": True,
                "status_code": 200,
                "message": "LLM providers found",
                "data": {"llm_providers": ["Provider A"]},
                "error": None
            }, 200),
            # Not found case: no LLM providers returned
            (None, True, {
                "status": False,
                "status_code": 422,
                "message": "LLM providers not found",
                "data": None,
                "error": None
            }, 200),
        ]
    )
    @patch('app.services.provider.getllmproviders')  # Mock the getllmproviders function
    def test_getllmproviders(self, mock_getllmproviders, client: TestClient, mock_return_value, is_error, expected_response, expected_status_code):
        # Set the mock return value for getllmproviders
        mock_getllmproviders.return_value = (mock_return_value, is_error)

        # Send a GET request to fetch LLM providers
        response = client.get("/api/v1/provider/llmproviders")

        # Assert the status code and response data match expected values
        assert response.status_code == expected_status_code
        assert response.json() == expected_response
