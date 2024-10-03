import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.models.connector import Connector
from app.models.provider import Provider, ProviderConfig
from unittest.mock import patch


@pytest.mark.usefixtures("client", "db_session")
class TestConnectorAPI:

    # Integration testing for creating pdf based connector
    @patch('app.repository.provider.get_config_types')
    def test_create_connector_type_2(self,mock_get_config_types, client: TestClient, db_session: Session, provider_fixture: Provider):

        mock_get_config_types.return_value = (
            [
                ProviderConfig(slug="db_name", field="db_name"),
                ProviderConfig(slug="db_host", field="db_host"),
                ProviderConfig(slug="db_port", field="db_port"),
                ProviderConfig(slug="db_user", field="db_user"),
                ProviderConfig(slug="db_password", field="db_password"),
                ProviderConfig(slug="db_sslmode", field="db_sslmode"),
            ],
            False
        )

        connector_data = {
            "connector_type": provider_fixture.id,
            "connector_name": "Test PSQL Connector",
            "connector_description": "Connector for PSQL database",
            "connector_config": {
                "db_host": "localhost",
                "db_port": 5432,
                "db_name": "sampledb",
                "db_user": "postgres",
                "db_password": "root",
                "db_sslmode": "disable"
            }
        }

        # Perform the POST request
        response = client.post("/api/v1/connector/create", json=connector_data)

        # Check response
        response_data = response.json()

        assert response.status_code == 200
        assert response_data["status"] is True
        assert response_data["message"] == "Connector Created"
        assert response_data["data"]["connector"]["connector_name"] == connector_data["connector_name"]
        assert response_data["data"]["connector"]["connector_type"] == provider_fixture.id

        # Verify database entry
        created_connector = db_session.query(Connector).filter(Connector.connector_name == connector_data["connector_name"]).first()
        assert created_connector is not None
