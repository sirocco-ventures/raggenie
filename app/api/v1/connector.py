from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import app.schemas.connector as schemas
import app.schemas.common as resp_schemas
from app.utils.database import get_db
import app.services.connector as svc
from starlette.requests import Request

from app.chain.chains.capability_chain import CapabilityChain
from app.chain.chains.metadata_chain import MetadataChain
from app.chain.chains.chain import Chain
from app.chain.chains.intent_chain import IntentChain
from app.plugins.loader import DSLoader

from app.providers.data_preperation import SourceDocuments
import app.api.v1.commons as commons
from loguru import logger
from app.providers.config import configs


router = APIRouter()
cap_router = APIRouter()
inference_router = APIRouter()
actions = APIRouter()

@router.get("/list", response_model=resp_schemas.CommonResponse)
def list_connectors(db: Session = Depends(get_db)):
    result, error = svc.list_connectors(db)

    if error:
        return commons.is_error_Response("DB Error", result, {"connectors": []})
    
    if not result:
        return commons.is_None_Reponse("Connector Not Found", {"connectors": []})
    
    return resp_schemas.CommonResponse(
        status=True,
        status_code=200,
        data={"connectors": result},
        message="Connectors Found",
        error=None
    )

@router.get("/get/{connector_id}", response_model=resp_schemas.CommonResponse)
def get_connector(connector_id: int, db: Session = Depends(get_db)):
    result, error = svc.get_connector(connector_id, db)

    if error:
        return commons.is_error_Response("DB Error", result, {"connector": {}})
    
    if not result:
        return commons.is_None_Reponse("Connector Not Found", {"connector": {}})
    
    return resp_schemas.CommonResponse(
        status=True,
        status_code=200,
        data={"connector": result},
        message="Connector Found",
        error=None
    )

@router.post("/create", response_model=resp_schemas.CommonResponse)
def create_connector(connector: schemas.ConnectorBase, db: Session = Depends(get_db)):
    result, error = svc.create_connector(connector, db)

    if error:
        return commons.is_error_Response("Connector Not Created", error, {"connector": {}})
    
    return resp_schemas.CommonResponse(
        status=True,
        status_code=201,
        data={"connector": result},
        message="Connector Created",
        error=None
    )

@router.post("/update/{connector_id}", response_model=resp_schemas.CommonResponse)
def update_connector(connector_id: int, connector: schemas.ConnectorUpdate, db: Session = Depends(get_db)):
    result, error = svc.update_connector(connector_id, connector, db)

    if error:
        return commons.is_error_Response("DB Error", result, {"connector": {}})
    
    if not result:
        return commons.is_None_Reponse("Connector Not Found", {"connector": {}})
    
    return resp_schemas.CommonResponse(
        status=True,
        status_code=200,
        data={"connector": result},
        message="Connector Updated",
        error=None
    )

@router.delete("/delete/{connector_id}", response_model=resp_schemas.CommonResponse)
def delete_connector(connector_id: int, db: Session = Depends(get_db)):
    result, error = svc.delete_connector(connector_id, db)

    if error:
        return commons.is_error_Response("DB Error", result, {"connector": {}})
    
    if not result:
        return commons.is_None_Reponse("Connector Not Found", {"connector": {}})
    
    return resp_schemas.CommonResponse(
        status=True,
        status_code=200,
        data={"connector": result},
        message="Connector Deleted",
        error=None
    )

@router.post("/schema/update/{connector_id}", response_model=resp_schemas.CommonResponse)
def updateschemas(connector_id: int, connector: schemas.SchemaUpdate, db: Session = Depends(get_db)):
    result, error = svc.updateschemas(connector_id, connector, db)

    if error:
        return commons.is_error_Response("DB Error", result, {"schemas": {}})
    
    if not result:
        return commons.is_None_Reponse("Connector Not Found", {"schemas": {}})
    
    return resp_schemas.CommonResponse(
        status=True,
        status_code=200,
        data={"schemas": result},
        message="Schema Updated",
        error=None
    )



@router.get("/configuration/list", response_model=resp_schemas.CommonResponse)
def list_configurations(db: Session = Depends(get_db)):
    result, error = svc.list_configurations(db)

    if error and not result:
        return commons.is_error_Response("DB error", result, {"configurations": []})

    if not result:
        return commons.is_None_Reponse("Configurations Not Found", {"configurations": []})
    
    return resp_schemas.CommonResponse(
        status=True,
        status_code=200,
        message="Configurations retrieved successfully",
        error=None,
        data={"configurations": result}
    )

@router.post("/configuration/create", response_model=resp_schemas.CommonResponse)
def create_configuration(configuration: schemas.ConfigurationCreation, db: Session = Depends(get_db)):
    result, error = svc.create_configuration(configuration, db)

    if error:
        return commons.is_error_Response("DB error", result, {"configuration": []})


    if not result:
        return commons.is_None_Reponse("Configuration Not Found", {"configuration": {}})

    
    return resp_schemas.CommonResponse(
        status=True,
        status_code=201,
        message="Configuration created successfully",
        error=None,
        data={"configuration": result}
    )

@router.post("/configuration/update/{config_id}", response_model=resp_schemas.CommonResponse)
def update_configuration(config_id: int, configuration: schemas.ConfigurationUpdate, db: Session = Depends(get_db)):
    result, error = svc.update_configuration(config_id, configuration, db)

    if error:
        return commons.is_error_Response("DB error", result, {"configuration": []})
    

    if not result:
        return commons.is_None_Reponse("Configuration Not Found", {"configuration": {}})
    
    
    return resp_schemas.CommonResponse(
        status=True,
        status_code=200,
        message="Configuration updated successfully",
        error=None,
        data={"configuration": result}
    )




@cap_router.post("/create", response_model=resp_schemas.CommonResponse)
def create_capability(capability: schemas.CapabilitiesBase, db: Session = Depends(get_db)):
    result, error = svc.create_capabilities(capability, db)

    if error:
        return commons.is_error_Response("DB error", result, {"capability": {}})

    
    return resp_schemas.CommonResponse(
        status=True,
        status_code=201,
        message="Capabilities created successfully",
        error=None,
        data={"capability": result}
    )

@cap_router.get("/all", response_model=resp_schemas.CommonResponse)
def list_capabilities_by_connector(db: Session = Depends(get_db)):
    result, error = svc.get_all_capabilities(db)

    if error:
        return commons.is_error_Response("DB error", result, {"capabilities": []})
    
    
    if not result:
        return commons.is_None_Reponse("Configuration Not Found", {"capabilities": []})
    

    return resp_schemas.CommonResponse(
        status=True,
        status_code=200,
        message="Capabilities retrieved successfully",
        error=None,
        data={"capabilities": result}
    )


@cap_router.post("/update/{cap_id}", response_model=resp_schemas.CommonResponse)
def update_capability(cap_id: int, capability: schemas.CapabilitiesUpdateBase, db: Session = Depends(get_db)):
    result, error = svc.update_capability(cap_id, capability, db)

    if error:
        return commons.is_error_Response("DB error", result, {"capability": {}})
    
    
    if not result:
        return commons.is_None_Reponse("Configuration Not Found", {"capability": {}})


    return resp_schemas.CommonResponse(
        status=True,
        status_code=200,
        message="Capability updated successfully",
        error=None,
        data={"capability": result}
    )

@cap_router.delete("/delete/{cap_id}", response_model=resp_schemas.CommonResponse)
def delete_capability(cap_id: int, db: Session = Depends(get_db)):
    result, error = svc.delete_capability(cap_id, db)

    if error:
        return commons.is_error_Response("DB error", result, {"capability": {}})

    
    if not result:
        return commons.is_None_Reponse("Configuration Not Found", {"capability": {}})
    

    return resp_schemas.CommonResponse(
        status=True,
        status_code=200,
        message="Capability deleted successfully",
        error=None,
        data={"capability": {}}
    )



@router.post("/createyaml/{config_id}")
def create_yaml(request: Request, config_id: int, db: Session = Depends(get_db)):

    documentations, use_case, is_error = svc.create_yaml_file(request,config_id, db)

    if is_error:
        return {
            "success":False,
            "error":is_error
        }

    inference_config, is_error = svc.create_inference_yaml(config_id,db)

    if is_error and not inference_config :
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

    data_sources_obj = {}
    index = 0
    
    for data_source_config in data_sources:
            datasource = DSLoader(
                data_source_config
            ).load_ds()
            datasource.connect()
            datasource.healthcheck()
            schema_config = data_source_config['schema_config']
            schema_details, metadata = datasource.fetch_schema_details()
            sd = SourceDocuments(schema_details, schema_config,[])
            chunked_document, chunked_schema = sd.get_source_documents()
            vectore_store.prepare_data(data_source_config['name'], chunked_document, chunked_schema, [])
            index = index + 1
            
            data_sources_obj[data_source_config["name"]] = datasource

    logger.info("checking execution mode")
   
     
    genna_chain = Chain(config, vectore_store, data_sources_obj, context_storage)
    capability_chain = CapabilityChain(config, context_storage, genna_chain)
    metedata_chain = MetadataChain(config, vectore_store, data_sources_obj, context_storage)

    chain = IntentChain(config, vectore_store, data_sources_obj, context_storage, genna_chain, capability_chain, metedata_chain)
    
    request.app.chain = chain
    
    return {
        "succcess": True,
        "error":None
    }
    
    
@inference_router.get("/get/{inference_id}", response_model=resp_schemas.CommonResponse)
def get_inference(inference_id: int, db: Session = Depends(get_db)):
    result, error = svc.get_inference(inference_id, db)

    if error:
        return commons.is_error_Response("DB error", result, {"inference": {}})
    

    if not result:
        return commons.is_None_Reponse("Inference Not Found", {"inference": {}})
    

    return resp_schemas.CommonResponse(
        status=True,
        status_code=200,
        message="Inference Found",
        error=None,
        data={"inference": result}
    )

@inference_router.post("/create", response_model=resp_schemas.CommonResponse)
def create_inference(inference: schemas.InferenceBase, db: Session = Depends(get_db)):
    result, error = svc.create_inference(inference, db)

    if error:
        return commons.is_error_Response("DB error", result, {"inference": {}})
    
    
    return resp_schemas.CommonResponse(
        status=True,
        status_code=201,
        message="Inference Created Successfully",
        error=None,
        data={"inference": result}
    )

@inference_router.post("/update/{inference_id}", response_model=resp_schemas.CommonResponse)
def update_inference(inference_id: int, inference: schemas.InferenceBaseUpdate, db: Session = Depends(get_db)):
    result, error = svc.update_inference(inference_id, inference, db)

    if error:
        return commons.is_error_Response("DB error", result, {"inference": {}})
    

    if not result:
        return commons.is_None_Reponse("Inference Not Found", {"inference": {}})


    return resp_schemas.CommonResponse(
        status=True,
        status_code=200,
        message="Inference Updated Successfully",
        error=None,
        data={"inference": result}
    )



@actions.get("/list", response_model=resp_schemas.CommonResponse)
def list_actions(db: Session = Depends(get_db)):
    result, error = svc.list_actions(db)

    if error:
        return commons.is_error_Response("DB error", result, {"actions": []})
    
    if not result:
        return commons.is_None_Reponse("Actions Not Found", {"actions": []})
    
    
    return resp_schemas.CommonResponse(
        status=True,
        status_code=200,
        data={"actions": result},
        message="Actions Found",
        error=None
    )

@actions.get("/get/{action_id}", response_model=resp_schemas.CommonResponse)
def get_action(action_id:int, db: Session = Depends(get_db)):
    result, error = svc.get_actions(action_id,db)

    if error:
        return commons.is_error_Response("DB error", result, {"action": {}})
    
    if not result:
        return commons.is_None_Reponse("Action Not Found", {"action": {}})
    
    
    return resp_schemas.CommonResponse(
        status=True,
        status_code=200,
        data={"action": result},
        message="Action Found",
        error=None
    )

@actions.get("/{connector_id}/list", response_model=resp_schemas.CommonResponse)
def get_actions_by_connector(connector_id:int, db: Session = Depends(get_db)):
    result, error = svc.get_actions_by_connector(connector_id,db)

    if error:
        return commons.is_error_Response("DB error", result, {"actions": []})
    
    if not result:
        return commons.is_None_Reponse("Actions Not Found", {"actions": []})
    
    
    return resp_schemas.CommonResponse(
        status=True,
        status_code=200,
        data={"actions": result},
        message="Action Found",
        error=None
    )

@actions.post("/create", response_model=resp_schemas.CommonResponse)
def create_action(action: schemas.Actions, db: Session = Depends(get_db)):
    result, error = svc.create_action(action, db)

    if error:
        return commons.is_error_Response("Action Not Created", error, {"action": {}})
    
    return resp_schemas.CommonResponse(
        status=True,
        status_code=201,
        data={"action": result},
        message="Action Created",
        error=None
    )