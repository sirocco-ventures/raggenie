# import pytest
# from unittest.mock import patch
# from fastapi.testclient import TestClient

# @pytest.mark.usefixtures("client")
# class TestConnectorAPI:

#     @pytest.mark.parametrize(
#         "mock_return_value, error, expected_response, expected_status_code",
#         [
#             # Success case
#             ([{"id": 1, "name": "Connector A"}], None, {
#                 "status": True,
#                 "status_code": 200,
#                 "data": {"connectors": [{"id": 1, "name": "Connector A"}]},
#                 "message": "Connectors Found",
#                 "error": None
#             }, 200),
#             # Empty connector case
#             ([], None, {
#                 "status": True,
#                 "status_code": 200,
#                 "data": {"connectors": []},
#                 "message": "Connector Not Found",
#                 "error": "Not Found"
#             }, 200),
#             # Database error case
#             ("DB Error", "DB Error", {
#                 "status": False,
#                 "status_code": 422,
#                 "data": {"connectors": []},
#                 "message": "DB Error",
#                 "error": "DB Error"
#             }, 200)
#         ]
#     )
#     @patch('app.services.connector.list_connectors')
#     def test_list_connectors(self, mock_list_connectors, client: TestClient, mock_return_value, error, expected_response, expected_status_code):
#         mock_list_connectors.return_value = (mock_return_value, error)

#         response = client.get("/api/v1/connector/list")

#         assert response.status_code == expected_status_code
#         assert response.json() == expected_response


#     @pytest.mark.parametrize(
#         "mock_return_value, error, expected_response, expected_status_code",
#         [
#             # Success case
#             ({"id": 1, "name": "Connector A"}, None, {
#                 "status": True,
#                 "status_code": 200,
#                 "data": {"connector": {"id": 1, "name": "Connector A"}},
#                 "message": "Connector Found",
#                 "error": None
#             }, 200),
#             # Connector not found case
#             ({}, None, {
#                 "status": True,
#                 "status_code": 200,
#                 "data": {"connector": {}},
#                 "message": "Connector Not Found",
#                 "error": "Not Found"
#             }, 200),
#             # Database error case
#             ("DB Error", "DB Error", {
#                 "status": False,
#                 "status_code": 422,
#                 "data": {"connector": {}},
#                 "message": "DB Error",
#                 "error": "DB Error"
#             }, 200)
#         ]
#     )
#     @patch('app.services.connector.get_connector')
#     def test_get_connector(self, mock_get_connector, client: TestClient, mock_return_value, error, expected_response, expected_status_code):
#         mock_get_connector.return_value = (mock_return_value, error)

#         response = client.get("/api/v1/connector/get/1")

#         assert response.status_code == expected_status_code
#         assert response.json() == expected_response

#     @pytest.mark.parametrize(
#         "mock_return_value, error, expected_response, expected_status_code",
#         [
#             # Success case
#             ({"id": 1, "name": "Connector A", "type": 1, "config": {"type": "Config A"}}, None, {
#                 "status": True,
#                 "status_code": 201,
#                 "data": {"connector": {"id": 1, "name": "Connector A", "type": 1, "config": {"type": "Config A"}}},
#                 "message": "Connector Created",
#                 "error": None
#             }, 200),
#             # Database error case
#             ("DB Error", "DB Error", {
#                 "status": False,
#                 "status_code": 422,
#                 "data": {"connector": {}},
#                 "message": "DB Error",
#                 "error": "DB Error"
#             }, 200)
#         ]
#     )
#     @patch('app.services.connector.create_connector')
#     def test_create_connector(self, mock_create_connector, client: TestClient, mock_return_value, error, expected_response, expected_status_code):
#         mock_create_connector.return_value = (mock_return_value, error)

#         response = client.post("/api/v1/connector/create", json={
#             "name": "Connector A",
#             "connector_type": 1,
#             "connector_name": "Connector A",
#             "connector_config": {"type": "Config A"}
#         })

#         assert response.status_code == expected_status_code
#         assert response.json() == expected_response

#     @pytest.mark.parametrize(
#         "mock_return_value, error, expected_response, expected_status_code",
#         [
#             # Success case
#             ({"id": 1, "name": "Connector A"}, None, {
#                 "status": True,
#                 "status_code": 200,
#                 "data": {"connector": {"id": 1, "name": "Connector A"}},
#                 "message": "Connector Updated",
#                 "error": None
#             }, 200),
#             # Connector not found case
#             (None, None, {
#                 "status": True,
#                 "status_code": 200,
#                 "data": {"connector": {}},
#                 "message": "Connector Not Found",
#                 "error": "Not Found"
#             }, 200),
#             # Database error case
#             ("DB Error", "DB Error", {
#                 "status": False,
#                 "status_code": 422,
#                 "data": {"connector": {}},
#                 "message": "DB Error",
#                 "error": "DB Error"
#             }, 200)
#         ]
#     )
#     @patch('app.services.connector.update_connector')
#     def test_update_connector(self, mock_update_connector, client: TestClient, mock_return_value, error, expected_response, expected_status_code):
#         mock_update_connector.return_value = (mock_return_value, error)

#         response = client.post("/api/v1/connector/update/1", json={"name": "Connector A"})

#         assert response.status_code == expected_status_code
#         assert response.json() == expected_response

#     @pytest.mark.parametrize(
#         "mock_return_value, error, expected_response, expected_status_code",
#         [
#             # Success case
#             ({"id": 1, "name": "Connector A"}, None, {
#                 "status": True,
#                 "status_code": 200,
#                 "data": {"connector": {"id": 1, "name": "Connector A"}},
#                 "message": "Connector Deleted",
#                 "error": None
#             }, 200),
#             # Connector not found case
#             (None, None, {
#                 "status": True,
#                 "status_code": 200,
#                 "data": {"connector": {}},
#                 "message": "Connector Not Found",
#                 "error": "Not Found"
#             }, 200),
#             # Database error case
#             ("DB Error", "DB Error", {
#                 "status": False,
#                 "status_code": 422,
#                 "data": {"connector": {}},
#                 "message": "DB Error",
#                 "error": "DB Error"
#             }, 200)
#         ]
#     )

#     @patch('app.services.connector.delete_connector')
#     def test_delete_connector(self, mock_delete_connector, client: TestClient, mock_return_value, error, expected_response, expected_status_code):
#         mock_delete_connector.return_value = (mock_return_value, error)

#         response = client.delete("/api/v1/connector/delete/1")

#         assert response.status_code == expected_status_code
#         assert response.json() == expected_response
#     @pytest.mark.parametrize(
#         "mock_return_value, error, expected_response, expected_status_code",
#         [
#             # Success case
#             ({"id": 1, "schema_config": [{"key": "value"}]}, None, {
#                 "status": True,
#                 "status_code": 200,
#                 "data": {"schemas": {"id": 1, "schema_config": [{"key": "value"}]}},
#                 "message": "Schema Updated",
#                 "error": None
#             }, 200),
#             # Connector not found case
#             (None, None, {
#                 "status": True,
#                 "status_code": 200,
#                 "data": {"schemas": {}},
#                 "message": "Connector Not Found",
#                 "error": "Not Found"
#             }, 200),
#             # Database error case
#             ("DB Error", "DB Error", {
#                 "status": False,
#                 "status_code": 422,
#                 "data": {"schemas": {}},
#                 "message": "DB Error",
#                 "error": "DB Error"
#             }, 200)
#         ]
#     )
#     @patch('app.services.connector.updateschemas')
#     def test_update_schemas(self, mock_updateschemas, client: TestClient, mock_return_value, error, expected_response, expected_status_code):
#         mock_updateschemas.return_value = (mock_return_value, error)

#         response = client.post("/api/v1/connector/schema/update/1", json={
#             "schema_config": [{"key": "value"}]
#         })

#         assert response.status_code == expected_status_code
#         assert response.json() == expected_response





#     @pytest.mark.parametrize(
#         "mock_return_value, error, expected_response, expected_status_code",
#         [
#             # Success case
#             ([{"id": 1, "name": "Config A"}], None, {
#                 "status": True,
#                 "status_code": 200,
#                 "message": "Configurations retrieved successfully",
#                 "error": None,
#                 "data": {"configurations": [{"id": 1, "name": "Config A"}]}
#             }, 200),
#             # No configurations found case
#             ([], None, {
#                 "status": True,
#                 "status_code": 200,
#                 "message": "Configurations Not Found",
#                 "error": "Not Found",
#                 "data": {"configurations": []}
#             }, 200),
#             # Database error case
#             ("DB error", "DB error", {
#                 "status": False,
#                 "status_code": 422,
#                 "message": "DB error",
#                 "error": "DB error",
#                 "data": {"configurations": []}
#             }, 200)
#         ]
#     )
#     @patch('app.services.connector.list_configurations')
#     def test_list_configurations(self, mock_list_configurations, client: TestClient, mock_return_value, error, expected_response, expected_status_code):
#         mock_list_configurations.return_value = (mock_return_value, error)

#         response = client.get("/api/v1/connector/configuration/list")

#         assert response.status_code == expected_status_code
#         assert response.json() == expected_response

#     @pytest.mark.parametrize(
#         "mock_return_value, error, expected_response, expected_status_code",
#         [
#             # Success case
#             ({"id": 1, "name": "Config A"}, None, {
#                 "status": True,
#                 "status_code": 201,
#                 "message": "Configuration created successfully",
#                 "error": None,
#                 "data": {"configuration": {"id": 1, "name": "Config A"}}
#             }, 200),
#             # Database error case
#             ("DB error", "DB error", {
#                 "status": False,
#                 "status_code": 422,
#                 "message": "DB error",
#                 "error": "DB error",
#                 "data": {"configuration": []}
#             }, 200)
#         ]
#     )
#     @patch('app.services.connector.create_configuration')
#     def test_create_configuration(self, mock_create_configuration, client: TestClient, mock_return_value, error, expected_response, expected_status_code):
#         mock_create_configuration.return_value = (mock_return_value, error)

#         response = client.post("/api/v1/connector/configuration/create", json={
#             "name": "Config A",
#             "short_description": "Short description",
#             "long_description": "Long description",
#             "status": 1,
#             "capabilities": [1, 2]
#         })

#         assert response.status_code == expected_status_code
#         assert response.json() == expected_response

#     @pytest.mark.parametrize(
#         "mock_return_value, error, expected_response, expected_status_code",
#         [
#             # Success case
#             ({"id": 1, "name": "Config A"}, None, {
#                 "status": True,
#                 "status_code": 200,
#                 "message": "Configuration updated successfully",
#                 "error": None,
#                 "data": {"configuration": {"id": 1, "name": "Config A"}}
#             }, 200),
#             # Database error case
#             ("DB error", "DB error", {
#                 "status": False,
#                 "status_code": 422,
#                 "message": "DB error",
#                 "error": "DB error",
#                 "data": {"configuration": []}
#             }, 200)
#         ]
#     )
#     @patch('app.services.connector.update_configuration')
#     def test_update_configuration(self, mock_update_configuration, client: TestClient, mock_return_value, error, expected_response, expected_status_code):
#         mock_update_configuration.return_value = (mock_return_value, error)

#         response = client.post("/api/v1/connector/configuration/update/1", json={
#             "name": "Config A Updated",
#             "short_description": "Updated short description",
#             "long_description": "Updated long description",
#             "status": 1
#         })

#         assert response.status_code == expected_status_code
#         assert response.json() == expected_response

#     @pytest.mark.parametrize(
#         "mock_return_value, error, expected_response, expected_status_code",
#         [
#             # Success case
#             ({"id": 1, "name": "Capability A"}, None, {
#                 "status": True,
#                 "status_code": 201,
#                 "message": "Capabilities created successfully",
#                 "error": None,
#                 "data": {"capability": {"id": 1, "name": "Capability A"}}
#             }, 200),
#             # Database error case
#             ("DB error", "DB error", {
#                 "status": False,
#                 "status_code": 422,
#                 "message": "DB error",
#                 "error": "DB error",
#                 "data": {"capability": {}}
#             }, 200)
#         ]
#     )


#     @patch('app.services.connector.create_capabilities')
#     def test_create_capability(self, mock_create_capabilities, client: TestClient, mock_return_value, error, expected_response, expected_status_code):
#         mock_create_capabilities.return_value = (mock_return_value, error)

#         response = client.post("/api/v1/capability/create", json={
#             "name": "Capability A",
#             "description": "Description for Capability A",
#             "requirements": [{"key": "value"}]
#         })

#         assert response.status_code == expected_status_code
#         assert response.json() == expected_response

#     @pytest.mark.parametrize(
#         "mock_return_value, error, expected_response, expected_status_code",
#         [
#             # Success case
#             ([{"id": 1, "name": "Capability A"}], None, {
#                 "status": True,
#                 "status_code": 200,
#                 "message": "Capabilities retrieved successfully",
#                 "error": None,
#                 "data": {"capabilities": [{"id": 1, "name": "Capability A"}]}
#             }, 200),
#             # Database error case
#             ("DB error", "DB error", {
#                 "status": False,
#                 "status_code": 422,
#                 "message": "DB error",
#                 "error": "DB error",
#                 "data": {"capabilities": []}
#             }, 200),
#             # Not found case
#             ([], None, {
#                 "status": True,
#                 "status_code": 200,
#                 "message": "Capabilities Not Found",
#                 "error": "Not Found",
#                 "data": {"capabilities": []}
#             }, 200)
#         ]
#     )
#     @patch('app.services.connector.get_all_capabilities')
#     def test_list_capabilities(self, mock_get_all_capabilities, client: TestClient, mock_return_value, error, expected_response, expected_status_code):
#         mock_get_all_capabilities.return_value = (mock_return_value, error)

#         response = client.get("/api/v1/capability/all")

#         assert response.status_code == expected_status_code
#         assert response.json() == expected_response

#     @pytest.mark.parametrize(
#         "mock_return_value, error, expected_response, expected_status_code",
#         [
#             # Success case
#             ({"id": 1, "name": "Capability A Updated"}, None, {
#                 "status": True,
#                 "status_code": 200,
#                 "message": "Capability updated successfully",
#                 "error": None,
#                 "data": {"capability": {"id": 1, "name": "Capability A Updated"}}
#             }, 200),
#             # Database error case
#             ("DB error", "DB error", {
#                 "status": False,
#                 "status_code": 422,
#                 "message": "DB error",
#                 "error": "DB error",
#                 "data": {"capability": {}}
#             }, 200),
#             # Not found case
#             (None, None, {
#                 "status": True,
#                 "status_code": 200,
#                 "message": "Capability Not Found",
#                 "error": "Not Found",
#                 "data": {"capability": {}}
#             }, 200)
#         ]
#     )
#     @patch('app.services.connector.update_capability')
#     def test_update_capability(self, mock_update_capability, client: TestClient, mock_return_value, error, expected_response, expected_status_code):
#         mock_update_capability.return_value = (mock_return_value, error)

#         response = client.post("/api/v1/capability/update/1", json={
#             "name": "Capability A Updated",
#             "description": "Updated description",
#             "requirements": [{"key": "new_value"}]
#         })

#         assert response.status_code == expected_status_code
#         assert response.json() == expected_response

#     @pytest.mark.parametrize(
#         "mock_return_value, error, expected_response, expected_status_code",
#         [
#             # Success case
#             ({"id": 1, "name": "Capability"}, None, {
#                 "status": True,
#                 "status_code": 200,
#                 "message": "Capability deleted successfully",
#                 "error": None,
#                 "data": {"capability": {"id": 1, "name": "Capability"}}
#             }, 200),
#             # Database error case
#             ("DB error", "DB error", {
#                 "status": False,
#                 "status_code": 422,
#                 "message": "DB error",
#                 "error": "DB error",
#                 "data": {"capability": {}}
#             }, 200),
#             # Not found case
#             (None, None, {
#                 "status": True,
#                 "status_code": 200,
#                 "message": "Capability Not Found",
#                 "error": "Not Found",
#                 "data": {"capability": {}}
#             }, 200)
#         ]
#     )
#     @patch('app.services.connector.delete_capability')
#     def test_delete_capability(self, mock_delete_capability, client: TestClient, mock_return_value, error, expected_response, expected_status_code):
#         mock_delete_capability.return_value = (mock_return_value, error)

#         response = client.delete("/api/v1/capability/delete/1")

#         assert response.status_code == expected_status_code
#         assert response.json() == expected_response


#     @pytest.mark.parametrize(
#         "mock_return_value, error, expected_response, expected_status_code",
#         [
#             # Success case
#             ({"id": 1, "name": "Inference A"}, None, {
#                 "status": True,
#                 "status_code": 200,
#                 "message": "Inference Found",
#                 "error": None,
#                 "data": {"inference": {"id": 1, "name": "Inference A"}}
#             }, 200),
#             # Database error case
#             ("DB error", "DB error", {
#                 "status": False,
#                 "status_code": 422,
#                 "message": "DB error",
#                 "error": "DB error",
#                 "data": {"inference": {}}
#             }, 200),
#             # Not found case
#             (None, None, {
#                 "status": True,
#                 "status_code": 200,
#                 "message": "Inference Not Found",
#                 "error": "Not Found",
#                 "data": {"inference": {}}
#             }, 200)
#         ]
#     )


#     @patch('app.services.connector.get_inference')
#     def test_get_inference(self, mock_get_inference, client: TestClient, mock_return_value, error, expected_response, expected_status_code):
#         mock_get_inference.return_value = (mock_return_value, error)

#         response = client.get("/api/v1/inference/get/1")

#         assert response.status_code == expected_status_code
#         assert response.json() == expected_response


#     @pytest.mark.parametrize(
#         "mock_return_value, error, expected_response, expected_status_code",
#         [
#             # Success case
#             ({"id": 1, "name": "Inference A"}, None, {
#                 "status": True,
#                 "status_code": 201,
#                 "message": "Inference Created Successfully",
#                 "error": None,
#                 "data": {"inference": {"id": 1, "name": "Inference A"}}
#             }, 200),
#             # Database error case
#             ("DB error", "DB error", {
#                 "status": False,
#                 "status_code": 422,
#                 "message": "DB error",
#                 "error": "DB error",
#                 "data": {"inference": {}}
#             }, 200)
#         ]
#     )
#     @patch('app.services.connector.create_inference')
#     def test_create_inference(self, mock_create_inference, client: TestClient, mock_return_value, error, expected_response, expected_status_code):
#         mock_create_inference.return_value = (mock_return_value, error)

#         response = client.post("/api/v1/inference/create", json={
#             "name": "Inference A",
#             "apikey": "apikey123",
#             "llm_provider": "provider",
#             "model": "model123",
#             "endpoint": "http://example.com"
#         })

#         assert response.status_code == expected_status_code
#         assert response.json() == expected_response

#     @pytest.mark.parametrize(
#         "mock_return_value, error, expected_response, expected_status_code",
#         [
#             # Success case
#             ({"id": 1, "name": "Inference A Updated"}, None, {
#                 "status": True,
#                 "status_code": 200,
#                 "message": "Inference Updated Successfully",
#                 "error": None,
#                 "data": {"inference": {"id": 1, "name": "Inference A Updated"}}
#             }, 200),
#             # Database error case
#             ("DB error", "DB error", {
#                 "status": False,
#                 "status_code": 422,
#                 "message": "DB error",
#                 "error": "DB error",
#                 "data": {"inference": {}}
#             }, 200),
#             # Not found case
#             (None, None, {
#                 "status": True,
#                 "status_code": 200,
#                 "message": "Inference Not Found",
#                 "error": "Not Found",
#                 "data": {"inference": {}}
#             }, 200)
#         ]
#     )
#     @patch('app.services.connector.update_inference')
#     def test_update_inference(self, mock_update_inference, client: TestClient, mock_return_value, error, expected_response, expected_status_code):
#         mock_update_inference.return_value = (mock_return_value, error)

#         response = client.post("/api/v1/inference/update/1", json={
#             "name": "Inference A Updated",
#             "apikey": "new_apikey",
#             "llm_provider": "new_provider",
#             "model": "new_model",
#             "endpoint": "http://newexample.com"
#         })

#         assert response.status_code == expected_status_code
#         assert response.json() == expected_response