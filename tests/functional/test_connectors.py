import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient

# Use the pytest fixture for the FastAPI test client
@pytest.mark.usefixtures("client")
class TestConnectorAPI:

    # Parameterized test for listing connectors
    @pytest.mark.parametrize(
        "mock_return_value, error, expected_response, expected_status_code",
        [
            # Success case: valid connector data returned
            ([{"id": 1, "name": "Connector A"}], None, {
                "status": True,
                "status_code": 200,
                "data": {"connectors": [{"id": 1, "name": "Connector A"}]},
                "message": "Connectors Found",
                "error": None
            }, 200),
            # Empty connector case: no connectors found
            ([], None, {
                "status": True,
                "status_code": 200,
                "data": {"connectors": []},
                "message": "Connector Not Found",
                "error": "Not Found"
            }, 200),
            # Database error case: simulate a database error
            ("DB Error", "DB Error", {
                "status": False,
                "status_code": 422,
                "data": {"connectors": []},
                "message": "DB Error",
                "error": "DB Error"
            }, 200)
        ]
    )
    @patch('app.services.connector.list_connectors')
    def test_list_connectors(self, mock_list_connectors, client: TestClient, mock_return_value, error, expected_response, expected_status_code):
        # Mock the list_connectors service to return the specified value and error
        mock_list_connectors.return_value = (mock_return_value, error)

        # Make a GET request to the list connectors endpoint
        response = client.get("/api/v1/connector/list")

        # Assert the response status code and content
        assert response.status_code == expected_status_code
        assert response.json() == expected_response

    # Parameterized test for getting a specific connector
    @pytest.mark.parametrize(
        "mock_return_value, error, expected_response, expected_status_code",
        [
            # Success case: valid connector data returned
            ({"id": 1, "name": "Connector A"}, None, {
                "status": True,
                "status_code": 200,
                "data": {"connector": {"id": 1, "name": "Connector A"}},
                "message": "Connector Found",
                "error": None
            }, 200),
            # Connector not found case: empty response
            ({}, None, {
                "status": True,
                "status_code": 200,
                "data": {"connector": {}},
                "message": "Connector Not Found",
                "error": "Not Found"
            }, 200),
            # Database error case: simulate a database error
            ("DB Error", "DB Error", {
                "status": False,
                "status_code": 422,
                "data": {"connector": {}},
                "message": "DB Error",
                "error": "DB Error"
            }, 200)
        ]
    )
    @patch('app.services.connector.get_connector')
    def test_get_connector(self, mock_get_connector, client: TestClient, mock_return_value, error, expected_response, expected_status_code):
        # Mock the get_connector service to return the specified value and error
        mock_get_connector.return_value = (mock_return_value, error)

        # Make a GET request to the get connector endpoint
        response = client.get("/api/v1/connector/get/1")

        # Assert the response status code and content
        assert response.status_code == expected_status_code
        assert response.json() == expected_response

    # Parameterized test for creating a new connector
    @pytest.mark.parametrize(
        "mock_return_value, error, expected_response, expected_status_code",
        [
            # Success case: valid connector creation
            ({"id": 1, "name": "Connector A", "type": 1, "config": {"type": "Config A"}}, None, {
                "status": True,
                "status_code": 201,
                "data": {"connector": {"id": 1, "name": "Connector A", "type": 1, "config": {"type": "Config A"}}},
                "message": "Connector Created",
                "error": None
            }, 200),
            # Database error case: simulate a database error
            ("DB Error", "DB Error", {
                "status": False,
                "status_code": 422,
                "data": {"connector": {}},
                "message": "Connector Not Created",
                "error": "DB Error"
            }, 200)
        ]
    )
    @patch('app.services.connector.create_connector')
    def test_create_connector(self, mock_create_connector, client: TestClient, mock_return_value, error, expected_response, expected_status_code):
        # Mock the create_connector service to return the specified value and error
        mock_create_connector.return_value = (mock_return_value, error)

        # Make a POST request to the create connector endpoint with the connector data
        response = client.post("/api/v1/connector/create", json={
            "name": "Connector A",
            "connector_type": 1,
            "connector_name": "Connector A",
            "connector_config": {"type": "Config A"}
        })

        # Assert the response status code and content
        assert response.status_code == expected_status_code
        assert response.json() == expected_response

    # Parameterized test for updating an existing connector
    @pytest.mark.parametrize(
        "mock_return_value, error, expected_response, expected_status_code",
        [
            # Success case: valid connector updated
            ({"id": 1, "name": "Connector A"}, None, {
                "status": True,
                "status_code": 200,
                "data": {"connector": {"id": 1, "name": "Connector A"}},
                "message": "Connector Updated",
                "error": None
            }, 200),
            # Connector not found case: no connector returned
            (None, None, {
                "status": True,
                "status_code": 200,
                "data": {"connector": {}},
                "message": "Connector Not Found",
                "error": "Not Found"
            }, 200),
            # Database error case: simulate a database error
            ("DB Error", "DB Error", {
                "status": False,
                "status_code": 422,
                "data": {"connector": {}},
                "message": "DB Error",
                "error": "DB Error"
            }, 200)
        ]
    )
    @patch('app.services.connector.update_connector')
    def test_update_connector(self, mock_update_connector, client: TestClient, mock_return_value, error, expected_response, expected_status_code):
        # Mock the update_connector service to return the specified value and error
        mock_update_connector.return_value = (mock_return_value, error)

        # Make a POST request to the update connector endpoint with the updated data
        response = client.post("/api/v1/connector/update/1", json={"name": "Connector A"})

        # Assert the response status code and content
        assert response.status_code == expected_status_code
        assert response.json() == expected_response

    # Parameterized test for deleting a connector
    @pytest.mark.parametrize(
        "mock_return_value, error, expected_response, expected_status_code",
        [
            # Success case: valid connector deleted
            ({"id": 1, "name": "Connector A"}, None, {
                "status": True,
                "status_code": 200,
                "data": {"connector": {"id": 1, "name": "Connector A"}},
                "message": "Connector Deleted",
                "error": None
            }, 200),
            # Connector not found case: no connector returned
            (None, None, {
                "status": True,
                "status_code": 200,
                "data": {"connector": {}},
                "message": "Connector Not Found",
                "error": "Not Found"
            }, 200),
            # Database error case: simulate a database error
            ("DB Error", "DB Error", {
                "status": False,
                "status_code": 422,
                "data": {"connector": {}},
                "message": "DB Error",
                "error": "DB Error"
            }, 200)
        ]
    )
    @patch('app.services.connector.delete_connector')
    def test_delete_connector(self, mock_delete_connector, client: TestClient, mock_return_value, error, expected_response, expected_status_code):
        # Mock the delete_connector service to return the specified value and error
        mock_delete_connector.return_value = (mock_return_value, error)

        # Make a DELETE request to the delete connector endpoint
        response = client.delete("/api/v1/connector/delete/1")

        # Assert the response status code and content
        assert response.status_code == expected_status_code
        assert response.json() == expected_response

    # Parameterized test for the update_schemas function
    @pytest.mark.parametrize(
        "mock_return_value, error, expected_response, expected_status_code",
        [
            # Success case
            ({"id": 1, "schema_config": [{"key": "value"}]}, None, {
                "status": True,
                "status_code": 200,
                "data": {"schemas": {"id": 1, "schema_config": [{"key": "value"}]}},
                "message": "Schema Updated",
                "error": None
            }, 200),
            # Connector not found case
            (None, None, {
                "status": True,
                "status_code": 200,
                "data": {"schemas": {}},
                "message": "Connector Not Found",
                "error": "Not Found"
            }, 200),
            # Database error case
            ("DB Error", "DB Error", {
                "status": False,
                "status_code": 422,
                "data": {"schemas": {}},
                "message": "DB Error",
                "error": "DB Error"
            }, 200)
        ]
    )
    @patch('app.services.connector.updateschemas')  # Mock the updateschemas function
    def test_update_schemas(self, mock_updateschemas, client: TestClient, mock_return_value, error, expected_response, expected_status_code):
        mock_updateschemas.return_value = (mock_return_value, error)  # Set mock return value

        # Make a POST request to update schemas
        response = client.post("/api/v1/connector/schema/update/1", json={
            "schema_config": [{"key": "value"}]
        })

        # Assert the status code and response JSON
        assert response.status_code == expected_status_code
        assert response.json() == expected_response

    # Parameterized test for the list_configurations function
    @pytest.mark.parametrize(
        "mock_return_value, error, expected_response, expected_status_code",
        [
            # Success case
            ([{"id": 1, "name": "Config A"}], None, {
                "status": True,
                "status_code": 200,
                "message": "Configurations retrieved successfully",
                "error": None,
                "data": {"configurations": [{"id": 1, "name": "Config A"}]}
            }, 200),
            # No configurations found case
            ([], None, {
                "status": True,
                "status_code": 200,
                "message": "Configurations Not Found",
                "error": "Not Found",
                "data": {"configurations": []}
            }, 200),
            # Database error case
            ("DB error", "DB error", {
                "status": False,
                "status_code": 422,
                "message": "DB error",
                "error": "DB error",
                "data": {"configurations": []}
            }, 200)
        ]
    )
    @patch('app.services.connector.list_configurations')  # Mock the list_configurations function
    def test_list_configurations(self, mock_list_configurations, client: TestClient, mock_return_value, error, expected_response, expected_status_code):
        mock_list_configurations.return_value = (mock_return_value, error)  # Set mock return value

        # Make a GET request to list configurations
        response = client.get("/api/v1/connector/configuration/list")

        # Assert the status code and response JSON
        assert response.status_code == expected_status_code
        assert response.json() == expected_response

    # Parameterized test for the create_configuration function
    @pytest.mark.parametrize(
        "mock_return_value, error, expected_response, expected_status_code",
        [
            # Success case
            ({"id": 1, "name": "Config A"}, None, {
                "status": True,
                "status_code": 201,
                "message": "Configuration created successfully",
                "error": None,
                "data": {"configuration": {"id": 1, "name": "Config A"}}
            }, 200),
            # Database error case
            ("DB error", "DB error", {
                "status": False,
                "status_code": 422,
                "message": "DB error",
                "error": "DB error",
                "data": {"configuration": []}
            }, 200)
        ]
    )
    @patch('app.services.connector.create_configuration')  # Mock the create_configuration function
    def test_create_configuration(self, mock_create_configuration, client: TestClient, mock_return_value, error, expected_response, expected_status_code):
        mock_create_configuration.return_value = (mock_return_value, error)  # Set mock return value

        # Make a POST request to create a new configuration
        response = client.post("/api/v1/connector/configuration/create", json={
            "name": "Config A",
            "short_description": "Short description",
            "long_description": "Long description",
            "status": 1,
            "capabilities": [1, 2]
        })

        # Assert the status code and response JSON
        assert response.status_code == expected_status_code
        assert response.json() == expected_response

    # Parameterized test for the update_configuration function
    @pytest.mark.parametrize(
        "mock_return_value, error, expected_response, expected_status_code",
        [
            # Success case
            ({"id": 1, "name": "Config A"}, None, {
                "status": True,
                "status_code": 200,
                "message": "Configuration updated successfully",
                "error": None,
                "data": {"configuration": {"id": 1, "name": "Config A"}}
            }, 200),
            # Database error case
            ("DB error", "DB error", {
                "status": False,
                "status_code": 422,
                "message": "DB error",
                "error": "DB error",
                "data": {"configuration": []}
            }, 200)
        ]
    )
    @patch('app.services.connector.update_configuration')  # Mock the update_configuration function
    def test_update_configuration(self, mock_update_configuration, client: TestClient, mock_return_value, error, expected_response, expected_status_code):
        mock_update_configuration.return_value = (mock_return_value, error)  # Set mock return value

        # Make a POST request to update a configuration
        response = client.post("/api/v1/connector/configuration/update/1", json={
            "name": "Config A Updated",
            "short_description": "Updated short description",
            "long_description": "Updated long description",
            "status": 1
        })

        # Assert the status code and response JSON
        assert response.status_code == expected_status_code
        assert response.json() == expected_response

    @pytest.mark.parametrize(
        "mock_return_value, error, expected_response, expected_status_code",
        [
            # Success case: A capability is created successfully
            ({"id": 1, "name": "Capability A"}, None, {
                "status": True,
                "status_code": 201,
                "message": "Capabilities created successfully",
                "error": None,
                "data": {"capability": {"id": 1, "name": "Capability A"}}
            }, 200),
            # Database error case: Simulating a database error during capability creation
            ("DB error", "DB error", {
                "status": False,
                "status_code": 422,
                "message": "DB error",
                "error": "DB error",
                "data": {"capability": {}}
            }, 200)
        ]
    )
    @patch('app.services.connector.create_capabilities')
    def test_create_capability(self, mock_create_capabilities, client: TestClient, mock_return_value, error, expected_response, expected_status_code):
        # Mock the create_capabilities function to return the specified mock_return_value and error
        mock_create_capabilities.return_value = (mock_return_value, error)

        # Send a POST request to create a new capability
        response = client.post("/api/v1/capability/create", json={
            "name": "Capability A",
            "description": "Description for Capability A",
            "requirements": [{"key": "value"}]
        })

        # Assert that the response status code and JSON match the expected values
        assert response.status_code == expected_status_code
        assert response.json() == expected_response

    @pytest.mark.parametrize(
        "mock_return_value, error, expected_response, expected_status_code",
        [
            # Success case: List of capabilities is retrieved successfully
            ([{"id": 1, "name": "Capability A"}], None, {
                "status": True,
                "status_code": 200,
                "message": "Capabilities retrieved successfully",
                "error": None,
                "data": {"capabilities": [{"id": 1, "name": "Capability A"}]}
            }, 200),
            # Database error case: Simulating a database error while retrieving capabilities
            ("DB error", "DB error", {
                "status": False,
                "status_code": 422,
                "message": "DB error",
                "error": "DB error",
                "data": {"capabilities": []}
            }, 200),
            # Not found case: No capabilities are found
            ([], None, {
                "status": True,
                "status_code": 200,
                "message": "Capabilities Not Found",
                "error": "Not Found",
                "data": {"capabilities": []}
            }, 200)
        ]
    )
    @patch('app.services.connector.get_all_capabilities')
    def test_list_capabilities(self, mock_get_all_capabilities, client: TestClient, mock_return_value, error, expected_response, expected_status_code):
        # Mock the get_all_capabilities function to return the specified mock_return_value and error
        mock_get_all_capabilities.return_value = (mock_return_value, error)

        # Send a GET request to retrieve all capabilities
        response = client.get("/api/v1/capability/all")

        # Assert that the response status code and JSON match the expected values
        assert response.status_code == expected_status_code
        assert response.json() == expected_response

    @pytest.mark.parametrize(
        "mock_return_value, error, expected_response, expected_status_code",
        [
            # Success case: A capability is updated successfully
            ({"id": 1, "name": "Capability A Updated"}, None, {
                "status": True,
                "status_code": 200,
                "message": "Capability updated successfully",
                "error": None,
                "data": {"capability": {"id": 1, "name": "Capability A Updated"}}
            }, 200),
            # Database error case: Simulating a database error during capability update
            ("DB error", "DB error", {
                "status": False,
                "status_code": 422,
                "message": "DB error",
                "error": "DB error",
                "data": {"capability": {}}
            }, 200),
            # Not found case: Capability not found during update
            (None, None, {
                "status": True,
                "status_code": 200,
                "message": "Capability Not Found",
                "error": "Not Found",
                "data": {"capability": {}}
            }, 200)
        ]
    )
    @patch('app.services.connector.update_capability')
    def test_update_capability(self, mock_update_capability, client: TestClient, mock_return_value, error, expected_response, expected_status_code):
        # Mock the update_capability function to return the specified mock_return_value and error
        mock_update_capability.return_value = (mock_return_value, error)

        # Send a POST request to update a capability
        response = client.post("/api/v1/capability/update/1", json={
            "name": "Capability A Updated",
            "description": "Updated description",
            "requirements": [{"key": "new_value"}]
        })

        # Assert that the response status code and JSON match the expected values
        assert response.status_code == expected_status_code
        assert response.json() == expected_response

    @pytest.mark.parametrize(
        "mock_return_value, error, expected_response, expected_status_code",
        [
            # Success case: A capability is deleted successfully
            ({"id": 1, "name": "Capability"}, None, {
                "status": True,
                "status_code": 200,
                "message": "Capability deleted successfully",
                "error": None,
                "data": {"capability": {}}
            }, 200),
            # Database error case: Simulating a database error during capability deletion
            ("DB error", "DB error", {
                "status": False,
                "status_code": 422,
                "message": "DB error",
                "error": "DB error",
                "data": {"capability": {}}
            }, 200),
            # Not found case: Capability not found during deletion
            (None, None, {
                "status": True,
                "status_code": 200,
                "message": "Capability Not Found",
                "error": "Not Found",
                "data": {"capability": {}}
            }, 200)
        ]
    )
    @patch('app.services.connector.delete_capability')
    def test_delete_capability(self, mock_delete_capability, client: TestClient, mock_return_value, error, expected_response, expected_status_code):
        # Mock the delete_capability function to return the specified mock_return_value and error
        mock_delete_capability.return_value = (mock_return_value, error)

        # Send a DELETE request to delete a capability
        response = client.delete("/api/v1/capability/delete/1")

        # Assert that the response status code and JSON match the expected values
        assert response.status_code == expected_status_code
        assert response.json() == expected_response
