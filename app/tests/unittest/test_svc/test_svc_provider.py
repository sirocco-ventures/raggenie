# from fastapi.testclient import TestClient
# from sqlalchemy.orm import Session
# from app.models.provider import Provider
# from app.api.v1.provider import router
# from app.services import provider as svc
# from app.schemas.provider import ProviderResp
# from unittest.mock import patch
# from unittest.mock import MagicMock
# import pytest

# @pytest.mark.usefixtures("client")
# class TestProviderAPI:

#     def test_get_provider_success(db_session: Session):
#         # Arrange
#         provider = Provider(
#             id=1,
#             name="Test Provider",
#             description="A test provider",
#             enable=True,
#             icon="icon.png",
#             category_id=1,
#             key="test_provider"
#         )
#         provider.providerconfig = []  # Empty list for simplicity

#         mock_repo = MagicMock()
#         mock_repo.get_provider_by_id.return_value = (provider, False)

#         svc.repo = mock_repo  # Override repo with mock

#         # Act
#         result, error = svc.get_provider(1, db_session)

#         # Assert
#         assert error is None
#         assert isinstance(result, ProviderResp)
#         assert result.id == 1
#         assert result.name == "Test Provider"

#     def test_get_provider_db_error(db_session: Session):
#         # Arrange
#         mock_repo = MagicMock()
#         mock_repo.get_provider_by_id.return_value = (None, "DB Error")

#         svc.repo = mock_repo  # Override repo with mock

#         # Act
#         result, error = svc.get_provider(1, db_session)

#         # Assert
#         assert error == "DB Error"
#         assert result is None

#     def test_get_provider_not_found(db_session: Session):
#         # Arrange
#         mock_repo = MagicMock()
#         mock_repo.get_provider_by_id.return_value = ({}, None)

#         svc.repo = mock_repo  # Override repo with mock

#         # Act
#         result, error = svc.get_provider(1, db_session)
#         # Assert
#         assert error is None
#         assert result == {}
