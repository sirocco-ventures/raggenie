import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.models.connector import Connector
from app.models.provider import Provider, ProviderConfig
from unittest.mock import patch

# Use pytest fixtures for client and database session management
@pytest.mark.usefixtures("client", "db_session")
class TestConnectorAPI:

    # Integration testing for creating a PDF-based connector
    @patch('app.repository.provider.get_config_types')  # Mock the get_config_types function to return predefined values
    def test_create_connector_type_2(self, mock_get_config_types, client: TestClient, db_session: Session, provider_fixture: Provider):

        # Mocking the return value of get_config_types to simulate a response from the provider config
        mock_get_config_types.return_value = (
            [
                ProviderConfig(slug="website_url", field="website_url"),
            ],
            False
        )

        # Prepare the connector data for the POST request
        connector_data = {
            "connector_type": provider_fixture.id,  # Use the provider ID from the fixture
            "connector_name": "Test Website Connector",  # Name of the connector
            "connector_description": "Connector for Website database",  # Description of the connector
            "connector_config": {
                "website_url":"https://www.siroccoventures.com/"
            }
        }

        # Perform the POST request to create the connector
        response = client.post("/api/v1/connector/create", json=connector_data)

        # Check the response from the API
        response_data = response.json()  # Get the JSON response data

        # Assert that the response status code is 200 (OK)
        assert response.status_code == 200
        # Assert that the status in the response data is True
        assert response_data["status"] is True
        # Assert that the message indicates the connector was created
        assert response_data["message"] == "Connector Created"
        # Assert that the returned connector name matches the input data
        assert response_data["data"]["connector"]["connector_name"] == connector_data["connector_name"]
        # Assert that the returned connector type matches the provider ID
        assert response_data["data"]["connector"]["connector_type"] == provider_fixture.id

        # Verify that the connector has been created in the database
        created_connector = db_session.query(Connector).filter(Connector.connector_name == connector_data["connector_name"]).first()
        # Assert that the created connector is not None (it should exist in the database)
        assert created_connector is not None
