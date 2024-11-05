from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.models.provider import Provider
from app.api.v1.provider import router
from app.services import provider as svc
from app.schemas.provider import ProviderResp
from unittest.mock import patch
import pytest

# Use the pytest fixture for client management
@pytest.mark.usefixtures("client")
class TestProviderAPI:

    # Test case for successfully retrieving a provider by ID
    @patch('app.services.provider.repo')  # Mock the repository layer for the test
    def test_get_provider_success(self, mock_repo, db_session: Session):
        # Create a mock provider instance to simulate a successful database return
        provider = Provider(
            id=1,
            name="Test Provider",
            description="A test provider",
            enable=True,
            icon="icon.png",
            category_id=1,
            key="test_provider"
        )
        provider.providerconfig = []  # Initialize an empty list for provider config

        # Set the mock return value for the repo method
        mock_repo.get_provider_by_id.return_value = (provider, False)

        # Call the service method to get the provider
        result, error = svc.get_provider(1, db_session)

        # Assertions to verify the correct behavior
        assert error is None  # No error should occur
        assert isinstance(result, ProviderResp)  # Result should be an instance of ProviderResp
        assert result.id == 1  # ID should match the mock provider's ID
        assert result.name == "Test Provider"  # Name should match the mock provider's name

    # Test case for handling a database error when retrieving a provider
    @patch('app.services.provider.repo')  # Mock the repository layer for the test
    def test_get_provider_db_error(self, mock_repo, db_session: Session):
        # Simulate a database error by returning None and an error message
        mock_repo.get_provider_by_id.return_value = (None, "DB Error")

        # Call the service method to get the provider
        result, error = svc.get_provider(1, db_session)

        # Assertions to verify the correct error handling
        assert error == "DB Error"  # Error should match the simulated database error
        assert result is None  # Result should be None due to the error

    # Test case for handling a case where a provider is not found
    @patch('app.services.provider.repo')  # Mock the repository layer for the test
    def test_get_provider_not_found(self, mock_repo, db_session: Session):
        # Simulate a case where no provider is found by returning an empty dict and no error
        mock_repo.get_provider_by_id.return_value = ({}, None)

        # Call the service method to get the provider
        result, error = svc.get_provider(1, db_session)

        # Assertions to verify the correct handling of a not found case
        assert error is None  # No error should occur
        assert result == {}  # Result should be an empty dict
