from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import app.schemas.connector as schemas
import app.schemas.common as resp_schemas
from app.utils.database import get_db
import app.services.connector as svc
from starlette.requests import Request

from app.chain.chains.capability_chain import CapabilityChain
from app.chain.chains.metadata_chain import MetadataChain
from app.chain.chains.query_chain import QueryChain
from app.chain.chains.intent_chain import IntentChain
from app.chain.chains.general_chain import GeneralChain

import app.api.v1.commons as commons
from loguru import logger
from app.providers.config import configs


router = APIRouter()
cap_router = APIRouter()
inference_router = APIRouter()
actions = APIRouter()

@router.get("/list", response_model=resp_schemas.CommonResponse)
def list_connectors(db: Session = Depends(get_db)):

    """
    Retrieves a list of all connectors from the database.

    Args:
        db (Session): Database session dependency.

    Returns:
        CommonResponse: A response containing either the list of connectors or an error message.
    """

    result, error = svc.list_connectors(db)

    if error:
        return commons.is_error_response("DB Error", result, {"connectors": []})

    if not result:
        return commons.is_none_reponse("Connector Not Found", {"connectors": []})

    return resp_schemas.CommonResponse(
        status=True,
        status_code=200,
        data={"connectors": result},
        message="Connectors Found",
        error=None
    )

@router.get("/get/{connector_id}", response_model=resp_schemas.CommonResponse)
def get_connector(connector_id: int, db: Session = Depends(get_db)):

    """
    Retrieves a specific connector by its ID from the database.

    Args:
        connector_id (int): The ID of the connector.
        db (Session): Database session dependency.

    Returns:
        CommonResponse: A response containing either the connector details or an error message.
    """

    result, error = svc.get_connector(connector_id, db)

    if error:
        return commons.is_error_response("DB Error", result, {"connector": {}})

    if not result:
        return commons.is_none_reponse("Connector Not Found", {"connector": {}})

    return resp_schemas.CommonResponse(
        status=True,
        status_code=200,
        data={"connector": result},
        message="Connector Found",
        error=None
    )

@router.post("/create", response_model=resp_schemas.CommonResponse)
def create_connector(connector: schemas.ConnectorBase, db: Session = Depends(get_db)):

    """
    Creates a new connector in the database.

    Args:
        connector (ConnectorBase): The data for the new connector.
        db (Session): Database session dependency.

    Returns:
        CommonResponse: A response indicating success or failure of the connector creation process.
    """

    result, error = svc.create_connector(connector, db)
    if error:
        return commons.is_error_response("Connector Not Created", error, {"connector": {}})

    return resp_schemas.CommonResponse(
        status=True,
        status_code=201,
        data={"connector": result},
        message="Connector Created",
        error=None
    )

@router.post("/update/{connector_id}", response_model=resp_schemas.CommonResponse)
def update_connector(connector_id: int, connector: schemas.ConnectorUpdate, db: Session = Depends(get_db)):

    """
    Updates an existing connector based on its ID.

    Args:
        connector_id (int): The ID of the connector to update.
        connector (ConnectorUpdate): The updated data for the connector.
        db (Session): Database session dependency.

    Returns:
        CommonResponse: A response indicating success or failure of the update process.
    """

    result, error = svc.update_connector(connector_id, connector, db)

    if error:
        return commons.is_error_response("DB Error", result, {"connector": {}})

    if not result:
        return commons.is_none_reponse("Connector Not Found", {"connector": {}})

    return resp_schemas.CommonResponse(
        status=True,
        status_code=200,
        data={"connector": result},
        message="Connector Updated",
        error=None
    )

@router.delete("/delete/{connector_id}", response_model=resp_schemas.CommonResponse)
def delete_connector(connector_id: int, db: Session = Depends(get_db)):

    """
    Deletes a connector from the database based on its ID.

    Args:
        connector_id (int): The ID of the connector to delete.
        db (Session): Database session dependency.

    Returns:
        CommonResponse: A response indicating success or failure of the deletion process.
    """

    result, error = svc.delete_connector(connector_id, db)

    if error:
        return commons.is_error_response("DB Error", result, {"connector": {}})

    if not result:
        return commons.is_none_reponse("Connector Not Found", {"connector": {}})

    return resp_schemas.CommonResponse(
        status=True,
        status_code=200,
        data={"connector": result},
        message="Connector Deleted",
        error=None
    )

@router.post("/schema/update/{connector_id}", response_model=resp_schemas.CommonResponse)
def updateschemas(connector_id: int, connector: schemas.SchemaUpdate, db: Session = Depends(get_db)):

    """
    Updates the schema details of a connector based on its ID.

    Args:
        connector_id (int): The ID of the connector whose schema is being updated.
        connector (SchemaUpdate): The schema update data for the connector.
        db (Session): Database session dependency.

    Returns:
        CommonResponse: A response indicating success or failure of the schema update.
    """

    result, error = svc.updateschemas(connector_id, connector, db)

    if error:
        return commons.is_error_response("DB Error", result, {"schemas": {}})

    if not result:
        return commons.is_none_reponse("Connector Not Found", {"schemas": {}})

    return resp_schemas.CommonResponse(
        status=True,
        status_code=200,
        data={"schemas": result},
        message="Schema Updated",
        error=None
    )



@router.get("/configuration/list", response_model=resp_schemas.CommonResponse)
def list_configurations(db: Session = Depends(get_db)):

    """
    Lists all available configurations from the database.

    Args:
        db (Session): Database session dependency.

    Returns:
        CommonResponse: A response containing the list of configurations or an error message.
    """

    result, error = svc.list_configurations(db)

    if error and not result:
        return commons.is_error_response("DB error", result, {"configurations": []})

    if not result:
        return commons.is_none_reponse("Configurations Not Found", {"configurations": []})

    return resp_schemas.CommonResponse(
        status=True,
        status_code=200,
        message="Configurations retrieved successfully",
        error=None,
        data={"configurations": result}
    )

@router.post("/configuration/create", response_model=resp_schemas.CommonResponse)
def create_configuration(configuration: schemas.ConfigurationCreation, db: Session = Depends(get_db)):

    """
    Creates a new configuration and stores it in the database.

    Args:
        configuration (ConfigurationCreation): The new configuration details.
        db (Session): Database session dependency.

    Returns:
        CommonResponse: A response indicating the success or failure of the configuration creation.
    """

    result, error = svc.create_configuration(configuration, db)

    if error:
        return commons.is_error_response("DB error", result, {"configuration": []})


    if not result:
        return commons.is_none_reponse("Configuration Not Found", {"configuration": {}})


    return resp_schemas.CommonResponse(
        status=True,
        status_code=201,
        message="Configuration created successfully",
        error=None,
        data={"configuration": result}
    )

@router.post("/configuration/update/{config_id}", response_model=resp_schemas.CommonResponse)
def update_configuration(config_id: int, configuration: schemas.ConfigurationUpdate, db: Session = Depends(get_db)):

    """
    Updates an existing configuration in the database.

    Args:
        config_id (int): The ID of the configuration to update.
        configuration (ConfigurationUpdate): The updated configuration details.
        db (Session): Database session dependency.

    Returns:
        CommonResponse: A response indicating the success or failure of the configuration update.
    """

    result, error = svc.update_configuration(config_id, configuration, db)

    if error:
        return commons.is_error_response("DB error", result, {"configuration": []})


    if not result:
        return commons.is_none_reponse("Configuration Not Found", {"configuration": {}})


    return resp_schemas.CommonResponse(
        status=True,
        status_code=200,
        message="Configuration updated successfully",
        error=None,
        data={"configuration": result}
    )




@cap_router.post("/create", response_model=resp_schemas.CommonResponse)
def create_capability(capability: schemas.CapabilitiesBase, db: Session = Depends(get_db)):

    """
    Creates a new capability in the database.

    Args:
        capability (CapabilitiesBase): The new capability details.
        db (Session): Database session dependency.

    Returns:
        CommonResponse: A response indicating the success or failure of the capability creation.
    """

    result, error = svc.create_capabilities(capability, db)

    if error:
        return commons.is_error_response("DB error", result, {"capability": {}})


    return resp_schemas.CommonResponse(
        status=True,
        status_code=201,
        message="Capabilities created successfully",
        error=None,
        data={"capability": result}
    )

@cap_router.get("/all", response_model=resp_schemas.CommonResponse)
def get_all_capabilities(db: Session = Depends(get_db)):

    """
    Retrieves all capabilities from the database.

    Args:
        db (Session): Database session dependency.

    Returns:
        CommonResponse: A response containing the list of capabilities or an error message.
    """

    result, error = svc.get_all_capabilities(db)

    if error:
        return commons.is_error_response("DB error", result, {"capabilities": []})


    if not result:
        return commons.is_none_reponse("Configuration Not Found", {"capabilities": []})


    return resp_schemas.CommonResponse(
        status=True,
        status_code=200,
        message="Capabilities retrieved successfully",
        error=None,
        data={"capabilities": result}
    )


@cap_router.post("/update/{cap_id}", response_model=resp_schemas.CommonResponse)
def update_capability(cap_id: int, capability: schemas.CapabilitiesUpdateBase, db: Session = Depends(get_db)):

    """
    Updates an existing capability in the database.

    Args:
        cap_id (int): The ID of the capability to update.
        capability (CapabilitiesUpdateBase): The updated capability details.
        db (Session): Database session dependency.

    Returns:
        CommonResponse: A response indicating the success or failure of the capability update.
    """

    result, error = svc.update_capability(cap_id, capability, db)

    if error:
        return commons.is_error_response("DB error", result, {"capability": {}})


    if not result:
        return commons.is_none_reponse("Configuration Not Found", {"capability": {}})


    return resp_schemas.CommonResponse(
        status=True,
        status_code=200,
        message="Capability updated successfully",
        error=None,
        data={"capability": result}
    )

@cap_router.delete("/delete/{cap_id}", response_model=resp_schemas.CommonResponse)
def delete_capability(cap_id: int, db: Session = Depends(get_db)):

    """
    Deletes an existing capability from the database.

    Args:
        cap_id (int): The ID of the capability to delete.
        db (Session): Database session dependency.

    Returns:
        CommonResponse: A response indicating the success or failure of the capability deletion.
    """

    result, error = svc.delete_capability(cap_id, db)

    if error:
        return commons.is_error_response("DB error", result, {"capability": {}})


    if not result:
        return commons.is_none_reponse("Configuration Not Found", {"capability": {}})


    return resp_schemas.CommonResponse(
        status=True,
        status_code=200,
        message="Capability deleted successfully",
        error=None,
        data={"capability": {}}
    )



@router.post("/createyaml/{config_id}")
def create_yaml(request: Request, config_id: int, db: Session = Depends(get_db)):

    """
    Creates a YAML configuration file and initializes processing chains for the specified configuration.

    Args:
        request (Request): The request object containing the data for YAML creation.
        config_id (int): The ID of the configuration to use.
        db (Session): The database session dependency.

    Returns:
        dict: A dictionary with success status and error message, if any.
    """

    documentations, use_case, is_error = svc.create_yaml_file(request,config_id, db)

    if is_error:
        return {
            "success":False,
            "error":is_error
        }

    inference_config, is_error = svc.create_inference_yaml(config_id,db)

    if is_error and not inference_config:
        return {
            "success":False,
            "error":is_error
        }


    combined_yaml_content = {
        'datasources': documentations if documentations != None else [],
        'use_case': use_case
    }

    configs.inference_llm_model=inference_config[0]["unique_name"]

    config = request.app.config
    vectore_store = request.app.vector_store
    vectore_store.connect()
    context_storage = request.app.context_storage

    data_sources = combined_yaml_content["datasources"]
    use_case = combined_yaml_content["use_case"]

    config["use_case"] = use_case
    config["datasources"] = data_sources
    config["models"] = inference_config

    confyaml = svc.get_inference_and_plugin_configurations(db)
    request.app.container.config.from_dict(confyaml)
    datasources = request.app.container.datasources()

    mappings = confyaml.get("mappings",{})
    err = svc.update_datasource_documentations(db, vectore_store, datasources, mappings)

    if err:
        logger.error("Error updating")


    query_chain = QueryChain(config, vectore_store, datasources, context_storage)
    general_chain = GeneralChain(config, vectore_store, datasources, context_storage)
    capability_chain = CapabilityChain(config, context_storage, query_chain)
    metedata_chain = MetadataChain(config, vectore_store, datasources, context_storage)

    chain = IntentChain(config, vectore_store, datasources, context_storage, query_chain, general_chain, capability_chain, metedata_chain)

    request.app.chain = chain

    return {
        "success": True,
        "error":None
    }


@inference_router.get("/get/{inference_id}", response_model=resp_schemas.CommonResponse)
def get_inference(inference_id: int, db: Session = Depends(get_db)):

    """
    Retrieves an inference record from the database using the given inference ID.

    Args:
        inference_id (int): The ID of the inference record to retrieve.
        db (Session): The database session dependency.

    Returns:
        dict: A dictionary with the inference details or error message, if any.
    """

    result, error = svc.get_inference(inference_id, db)

    if error:
        return commons.is_error_response("DB error", result, {"inference": {}})


    if not result:
        return commons.is_none_reponse("Inference Not Found", {"inference": {}})


    return resp_schemas.CommonResponse(
        status=True,
        status_code=200,
        message="Inference Found",
        error=None,
        data={"inference": result}
    )

@inference_router.post("/create", response_model=resp_schemas.CommonResponse)
def create_inference(inference: schemas.InferenceBase, db: Session = Depends(get_db)):

    """
    Creates a new inference record in the database.

    Args:
        inference (schemas.InferenceBase): The details of the inference to be created.
        db (Session): The database session dependency.

    Returns:
        dict: A dictionary indicating the success of the operation and the created inference details or error message.
    """

    result, error = svc.create_inference(inference, db)

    if error:
        return commons.is_error_response("DB error", result, {"inference": {}})


    return resp_schemas.CommonResponse(
        status=True,
        status_code=201,
        message="Inference Created Successfully",
        error=None,
        data={"inference": result}
    )

@inference_router.post("/update/{inference_id}", response_model=resp_schemas.CommonResponse)
def update_inference(inference_id: int, inference: schemas.InferenceBaseUpdate, db: Session = Depends(get_db)):

    """
    Updates an existing inference record in the database.

    Args:
        inference_id (int): The ID of the inference record to update.
        inference (schemas.InferenceBaseUpdate): The updated details of the inference.
        db (Session): The database session dependency.

    Returns:
        dict: A dictionary with the status of the update operation and the updated inference details or error message, if any.
    """

    result, error = svc.update_inference(inference_id, inference, db)

    if error:
        return commons.is_error_response("DB error", result, {"inference": {}})


    if not result:
        return commons.is_none_reponse("Inference Not Found", {"inference": {}})


    return resp_schemas.CommonResponse(
        status=True,
        status_code=200,
        message="Inference Updated Successfully",
        error=None,
        data={"inference": result}
    )



@actions.get("/list", response_model=resp_schemas.CommonResponse)
def list_actions(db: Session = Depends(get_db)):

    """
    Retrieves all actions from the database.

    Args:
        db (Session): Database session dependency.

    Returns:
        CommonResponse: A response containing the list of actions or an error message.
    """

    result, error = svc.list_actions(db)

    if error:
        return commons.is_error_response("DB error", result, {"actions": []})

    if not result:
        return commons.is_none_reponse("Actions Not Found", {"actions": []})


    return resp_schemas.CommonResponse(
        status=True,
        status_code=200,
        data={"actions": result},
        message="Actions Found",
        error=None
    )

@actions.get("/get/{action_id}", response_model=resp_schemas.CommonResponse)
def get_action(action_id:int, db: Session = Depends(get_db)):

    """
    Retrieves a specific action by its ID.

    Args:
        action_id (int): The unique identifier of the action to retrieve.
        db (Session): Database session dependency.

    Returns:
        CommonResponse: A response containing the action details or an error message.
    """

    result, error = svc.get_actions(action_id,db)

    if error:
        return commons.is_error_response("DB error", result, {"action": {}})

    if not result:
        return commons.is_none_reponse("Action Not Found", {"action": {}})


    return resp_schemas.CommonResponse(
        status=True,
        status_code=200,
        data={"action": result},
        message="Action Found",
        error=None
    )

@actions.get("/{connector_id}/list", response_model=resp_schemas.CommonResponse)
def get_actions_by_connector(connector_id:int, db: Session = Depends(get_db)):

    """
    Retrieves all actions related to a specific connector by its ID.

    Args:
        connector_id (int): The unique identifier of the connector.
        db (Session): Database session dependency.

    Returns:
        CommonResponse: A response containing the list of actions or an error message.
    """

    result, error = svc.get_actions_by_connector(connector_id,db)

    if error:
        return commons.is_error_response("DB error", result, {"actions": []})

    if not result:
        return commons.is_none_reponse("Actions Not Found", {"actions": []})


    return resp_schemas.CommonResponse(
        status=True,
        status_code=200,
        data={"actions": result},
        message="Action Found",
        error=None
    )

@actions.post("/create", response_model=resp_schemas.CommonResponse)
def create_action(action: schemas.Actions, db: Session = Depends(get_db)):

    """
    Creates a new action in the database.

    Args:
        action (Actions): The schema containing action details to create.
        db (Session): Database session dependency.

    Returns:
        CommonResponse: A response indicating the success or failure of the action creation.
    """

    result, error = svc.create_action(action, db)

    if error:
        return commons.is_error_response("Action Not Created", result, {"action": {}})

    return resp_schemas.CommonResponse(
        status=True,
        status_code=201,
        data={"action": result},
        message="Action Created",
        error=None
    )

@actions.post("/update/{action_id}", response_model=resp_schemas.CommonResponse)
def update_action(action_id: int, action: schemas.ActionsUpdate, db: Session = Depends(get_db)):

    """
    Updates an existing action in the database by its ID.

    Args:
        action_id (int): The unique identifier of the action to update.
        action (ActionsUpdate): The schema containing updated action details.
        db (Session): Database session dependency.

    Returns:
        CommonResponse: A response indicating the success or failure of the action update.
    """

    result, error = svc.update_action(action_id, action, db)

    if error:
        return commons.is_error_response("DB error", result, {"action": {}})

    if not result:
        return commons.is_none_reponse("Action Not Found", {"action": {}})


    return resp_schemas.CommonResponse(
        status=True,
        status_code=200,
        data={"action": result},
        message="Action Updated",
        error=None
    )

@actions.delete("/{action_id}", response_model=resp_schemas.CommonResponse)
def delete_action(action_id: int, db: Session = Depends(get_db)):

    """
    Deletes an action by its ID from the database.

    Args:
        action_id (int): The unique identifier of the action to delete.
        db (Session): Database session dependency.

    Returns:
        CommonResponse: A response indicating the success or failure of the action deletion.
    """

    result, error = svc.delete_action(action_id, db)

    if error:
        return commons.is_error_response("DB error", result, {"action": {}})

    if not result:
        return commons.is_none_reponse("Action Not Found", {"action": {}})


    return resp_schemas.CommonResponse(
        status=True,
        status_code=200,
        data={"action": result},
        message="Action Deleted",
        error=None
    )
