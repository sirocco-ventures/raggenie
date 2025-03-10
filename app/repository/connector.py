from sqlalchemy.orm import Session, joinedload
import app.models.connector as models
import app.models.provider as prov_models
import app.schemas.connector as schemas
from sqlalchemy.exc import SQLAlchemyError
from typing import List

from app.models.environment import UserEnvironmentMapping


def get_connectors_by_configuration_id(configuration_id: int, db: Session):
    try:
        connectors = (
            db.query(models.Connector)
            .join(models.ConfigurationConnectorMapping, models.Connector.id == models.ConfigurationConnectorMapping.connector_id)
            .filter(models.ConfigurationConnectorMapping.configuration_id == configuration_id)
            .all()
        )
        return connectors, False
    except Exception as e:
        return None, str(e)    
    

def get_all_connectors(db: Session, user_id: str):
    try:
        active_env = (db.query(UserEnvironmentMapping)
            .filter(UserEnvironmentMapping.user_id == user_id, UserEnvironmentMapping.is_active == True)
            .first())
        connectors = (
            db.query(models.Connector)
            .filter(models.Connector.environment_id == active_env.id)  
            .options(joinedload(models.Connector.provider))  
            .all()
        )
        return connectors, False
    except SQLAlchemyError as e:
        return str(e), True


def get_connector_by_id(connector_id: int, db: Session):
    try:
        return db.query(models.Connector).options(joinedload(models.Connector.provider)).filter(models.Connector.id == connector_id).first(), False
    except SQLAlchemyError as e:
        return str(e), True

def create_new_connector(connector: schemas.ConnectorBase, db: Session, user_id: str):
    try:
        active_env = (db.query(UserEnvironmentMapping)
            .filter(UserEnvironmentMapping.user_id == user_id, UserEnvironmentMapping.is_active == True)
            .first())
        db_connector = models.Connector(**connector.model_dump(),environment_id=active_env.id)
        db.add(db_connector)
        db.commit()
        db.refresh(db_connector)
        return db_connector, False
    except SQLAlchemyError as e:
        db.rollback()
        return str(e), True

def update_existing_connector(connector_id: int, connector: schemas.ConnectorUpdate, db: Session):
    try:
        db_connector = db.query(models.Connector).filter(models.Connector.id == connector_id).first()
        if db_connector:
            for key, value in connector.model_dump(exclude_unset=True).items():
                setattr(db_connector, key, value)
            db.commit()
            db.refresh(db_connector)
        return db_connector, False
    except SQLAlchemyError as e:
        db.rollback()
        return str(e), True

def update_schemas(connector_id: int, connector: schemas.ConnectorUpdate, db: Session):
    try:
        db_connector = db.query(models.Connector).filter(models.Connector.id == connector_id).first()

        if db_connector and connector.schema_config:
            db_connector.schema_config = connector.schema_config
            db.commit()
            db.refresh(db_connector)

        return db_connector, False
    except SQLAlchemyError as e:
        db.rollback()
        return str(e), True


def delete_connector_by_id(connector_id: int, db: Session):
    try:
        db_connector = db.query(models.Connector).filter(models.Connector.id == connector_id).first()
        if db_connector:
            db.delete(db_connector)
            db.commit()
        return db_connector, False
    except SQLAlchemyError as e:
        db.rollback()
        return str(e), True

def get_all_configurations(db: Session, user_id: str):
    try:
        active_env = (db.query(UserEnvironmentMapping)
            .filter(UserEnvironmentMapping.user_id == user_id, UserEnvironmentMapping.is_active == True)
            .first())
        return (
            db.query(models.Configuration)
            .filter(models.Configuration.environment_id == active_env.id)
            .options(
                joinedload(models.Configuration.capabilities),
                joinedload(models.Configuration.inference_mapping).joinedload(models.Inferenceconfigmapping.inference),
                joinedload(models.Configuration.vectordb_config_mapping).joinedload(prov_models.VectorDBConfigMapping.vector_db),
                joinedload(models.Configuration.connectors).joinedload(models.ConfigurationConnectorMapping.connector)  
            )
            .all(),
            False
        )
    except SQLAlchemyError as e:
        return str(e), True


def get_inference_by_config(config_id: int, db: Session):
    """
    Retrieves the Inference based on the config_id, using joinedload to load related data.

    Args:
        config_id (int): The configuration ID to query.
        db (Session): Database session object.

    Returns:
        Tuple: Inference instance, error message (if any).
    """
    try:
        result = db.query(models.Inferenceconfigmapping).options(joinedload(models.Inferenceconfigmapping.inference)).options(joinedload(models.Inferenceconfigmapping.configuration)).filter(models.Inferenceconfigmapping.config_id == config_id).first()

        if result:
            return result.inference, False
        else:
            return None, "Inference not found for the given config_id"

    except SQLAlchemyError as e:
        db.rollback()
        return None, str(e)

def getbotconfiguration(db:Session):

    try:
        return (
            db.query(models.Configuration).filter(models.Configuration.status == 2).first()
        ), False

    except SQLAlchemyError as e:
        return str(e), True

def create_new_configuration(configuration: schemas.ConfigurationCreation, db: Session, user_id: str):
    try:
        active_env = (db.query(UserEnvironmentMapping)
            .filter(UserEnvironmentMapping.user_id == user_id, UserEnvironmentMapping.is_active == True)
            .first())
        db_configuration = models.Configuration(
            name=configuration.name,
            short_description=configuration.short_description,
            long_description=configuration.long_description,
            status=configuration.status,
            environment_id=active_env.id 
        )
        db.add(db_configuration)
        db.commit()
        db.refresh(db_configuration)

        for capability_id in configuration.capabilities:
            db_capability = db.query(models.Capabilities).get(capability_id)
            if db_capability:
                db_capability.config_id = db_configuration.id
                db.add(db_capability)

        db.commit()
        
        if configuration.connectors:
            link_configuration_to_connectors(db_configuration.id, configuration.connectors, db)

        return db_configuration, False
    except SQLAlchemyError as e:
        db.rollback()
        return str(e), True


def link_configuration_to_connectors(config_id: int, connector_ids: list[int], db: Session):
    """
    Links a configuration with selected connectors.
    """
    try:
        for connector_id in connector_ids:
            existing_mapping = (
                db.query(models.ConfigurationConnectorMapping)
                .filter_by(configuration_id=config_id, connector_id=connector_id)
                .first()
            )
            if not existing_mapping:
                mapping = models.ConfigurationConnectorMapping(configuration_id=config_id, connector_id=connector_id)
                db.add(mapping)

        db.commit()
        return True, None
    except SQLAlchemyError as e:
        db.rollback()
        return False, str(e)

def update_existing_configuration(config_id: int, configuration: schemas.ConfigurationUpdate, db: Session):
    try:
        db_configuration = db.query(models.Configuration).filter(models.Configuration.id == config_id).first()
        if db_configuration is None:
            return None, True

        db_configuration.name = configuration.name if configuration.name else db_configuration.name
        db_configuration.short_description = configuration.short_description if configuration.short_description else db_configuration.short_description
        db_configuration.long_description = configuration.long_description if configuration.long_description else db_configuration.long_description
        db_configuration.status = configuration.status if configuration.status else db_configuration.status

        db.commit()
        db.refresh(db_configuration)

        if configuration.capabilities is not None:
            db.query(models.Capabilities).filter(models.Capabilities.config_id == config_id).update(
                {models.Capabilities.config_id: None}, synchronize_session=False
            )
            db.commit()

            for capability_id in configuration.capabilities:
                query = db.query(models.Capabilities).filter(models.Capabilities.id == capability_id).first()
                if query:
                    query.config_id = config_id
                    db.add(query)
                    db.commit()
                    db.refresh(query)
                    
        if configuration.connectors is not None:
            
            """ fetch existing connector mapping """
            existing_connector_ids = {
                mapping.connector_id for mapping in db.query(models.ConfigurationConnectorMapping)
                .filter(models.ConfigurationConnectorMapping.configuration_id == config_id)
                .all()
            }
            
            new_connector_ids = set(configuration.connectors)
            connectors_to_remove = existing_connector_ids - new_connector_ids
            if connectors_to_remove:
                db.query(models.ConfigurationConnectorMapping).filter(
                models.ConfigurationConnectorMapping.configuration_id == config_id,
                models.ConfigurationConnectorMapping.connector_id.in_(connectors_to_remove)
                ).delete(synchronize_session=False)
                db.commit()
            
            connector_to_add = new_connector_ids - existing_connector_ids
            if connector_to_add:
                link_configuration_to_connectors(db_configuration.id, connector_to_add, db)
            
            
        return db_configuration, False
    except SQLAlchemyError as e:
        db.rollback()
        return str(e), True

def get_configuration_by_id(config_id: int, db: Session):
    try:
        return (
            db.query(models.Configuration)
            .filter(models.Configuration.id == config_id)
            .options(
                joinedload(models.Configuration.capabilities),
                joinedload(models.Configuration.inference_mapping).joinedload(models.Inferenceconfigmapping.inference),
                joinedload(models.Configuration.vectordb_config_mapping).joinedload(prov_models.VectorDBConfigMapping.vector_db),
                joinedload(models.Configuration.connectors).joinedload(models.ConfigurationConnectorMapping.connector)  # 🔹 Include connectors
            )
            .first(), 
            False
            )
    except SQLAlchemyError as e:
        return str(e), True
    
def delete_configuration_by_id(configuration_id: int, db: Session):
    try:
        db_configuration = db.query(models.Configuration).filter(models.Configuration.id == configuration_id).options(joinedload(models.Configuration.capabilities)).first()
        if db_configuration:
            db.delete(db_configuration)
            db.commit()
        return db_configuration, False
    except SQLAlchemyError as e:
        db.rollback()
        return str(e), True

def update_configuration_status(config_id: int, db: Session):
    try:
        db_config, is_error = get_configuration_by_id(config_id, db)

        if db_config and not is_error:
            db.query(models.Configuration).filter(
            models.Configuration.status == 2
            ).update({"status": 0})
            db_config.status = 2

            db.commit()
            db.refresh(db_config)

            return db_config, False
        else:
            return None, True
    except (SQLAlchemyError, ValueError) as e:
        db.rollback()
        return str(e), True



def create_capability(capability: schemas.CapabilitiesBase, db: Session):
    try:
        new_capability = models.Capabilities(
            name=capability.name,
            description=capability.description,
            requirements=capability.requirements,
            config_id=capability.config_id if capability.config_id else None,
            enable=True
        )
        db.add(new_capability)
        db.commit()
        db.refresh(new_capability)
        return new_capability, False
    except SQLAlchemyError as e:
        db.rollback()
        return str(e), True

def create_capability_action_mappings(capability_id: int, action_ids: List[int], db: Session):
    try:
        for action_id in action_ids:
            mapping = models.CapActionsMapping(
                capability_id=capability_id,
                action_id=action_id,
                enable=True
            )
            db.add(mapping)

        db.commit()
        return True, False  # Successful creation, no error
    except SQLAlchemyError as e:
        db.rollback()
        return str(e), True  # Error occurred

def get_all_capabilities(db: Session):
    try:
        capabilities = db.query(models.Capabilities).options(
            joinedload(models.Capabilities.cap_actions_mapping).joinedload(models.CapActionsMapping.actions)
        ).all()

        return capabilities, False
    except SQLAlchemyError as e:
        return str(e), True


def update_capability(cap_id: int, capability: schemas.CapabilitiesUpdateBase, db: Session):
    try:
        capability_record = db.query(models.Capabilities).filter(models.Capabilities.id == cap_id).first()

        if capability_record:
            capability_record.name = capability.name if capability.name else capability_record.name
            capability_record.description = capability.description if capability.description else capability_record.description
            capability_record.requirements = capability.requirements if capability.requirements else capability_record.requirements
            capability_record.config_id = capability.config_id if capability.config_id else capability_record.config_id

            if capability.actions_list:
                db.query(models.CapActionsMapping).filter(models.CapActionsMapping.capability_id == cap_id).delete()

                for action_id in capability.actions_list:
                    new_mapping = models.CapActionsMapping(
                        capability_id=cap_id,
                        action_id=action_id,
                        enable=True
                    )
                    db.add(new_mapping)

            db.commit()
            db.refresh(capability_record)

            return capability_record, False

        return None, True
    except SQLAlchemyError as e:
        db.rollback()
        return str(e), True

def delete_capability(cap_id: int, db: Session):
    try:
        capability_record = db.query(models.Capabilities).filter(models.Capabilities.id == cap_id).first()

        if capability_record:
            db.query(models.CapActionsMapping).filter(models.CapActionsMapping.capability_id == cap_id).delete()

            db.delete(capability_record)
            db.commit()

            return True, False

        return False, True
    except SQLAlchemyError as e:
        db.rollback()
        return str(e), True


def get_inference_by_id(inference_id: int, db: Session):
    try:
        return db.query(models.Inference).filter(models.Inference.id == inference_id).first(), False
    except SQLAlchemyError as e:
        return str(e), True


def create_inference(inference: schemas.InferenceBase, db: Session):
    try:
        db_inference = models.Inference(
            name=inference.name,
            apikey=inference.apikey,
            llm_provider=inference.llm_provider,
            model=inference.model,
            endpoint=inference.endpoint
        )
        db.add(db_inference)
        db.commit()
        db.refresh(db_inference)

        db_mapping = models.Inferenceconfigmapping(
            inference_id=db_inference.id,
            config_id=inference.config_id,
            enable=True
        )
        db.add(db_mapping)
        db.commit()

        db.refresh(db_inference)

        return db_inference, False

    except SQLAlchemyError as e:
        db.rollback()
        return str(e), True

def update_inference(inference_id: int, inference: schemas.InferenceBaseUpdate, db: Session):
    try:
        db_inference = db.query(models.Inference).filter(models.Inference.id == inference_id).first()

        if db_inference is None:
            return "Data is None", True

        db_inference.name = inference.name if inference.name else db_inference.name
        db_inference.apikey = inference.apikey if inference.apikey else db_inference.apikey
        db_inference.llm_provider = inference.llm_provider if inference.llm_provider else db_inference.llm_provider
        db_inference.model = inference.model if inference.model else db_inference.model
        db_inference.endpoint = inference.endpoint if inference.endpoint else db_inference.endpoint

        db.commit()
        db.refresh(db_inference)

        if inference.config_id:
            db_mapping = db.query(models.Inferenceconfigmapping).filter(models.Inferenceconfigmapping.inference_id == inference_id).first()
            if db_mapping:
                db_mapping.config_id = inference.config_id
            else:
                db_mapping = models.Inferenceconfigmapping(
                    inference_id=inference_id,
                    config_id=inference.config_id,
                    enable=True
                )
                db.add(db_mapping)
            db.commit()
            db.refresh(db_mapping)

        return db_inference, False

    except SQLAlchemyError as e:
        db.rollback()
        return str(e), True

def get_inferences_by_config_id(config_id: int, db: Session):
    try:
        return db.query(models.Inferenceconfigmapping).options(joinedload(models.Inferenceconfigmapping.inference)).filter(models.Inferenceconfigmapping.config_id == config_id).all(), False
    except SQLAlchemyError as e:
        return str(e), True

def list_actions(db:Session):
    try:
        return db.query(models.Actions).all(), False
    except SQLAlchemyError as e:
        return str(e),

def get_action_by_id(action_id:int, db:Session):
    try:
        return db.query(models.Actions).filter(models.Actions.id == action_id).first(), False
    except SQLAlchemyError as e:
        return str(e),

def get_actions_by_connector(connector_id:int, db:Session):
    try:
        return db.query(models.Actions).filter(models.Actions.connector_id == connector_id).all(), False
    except SQLAlchemyError as e:
        return str(e), True

def create_action(action:schemas.Actions, db:Session):
    try:
        db_action = models.Actions(
            name=action.name,
            description=action.description if action.description else None,
            types=action.types,
            connector_id = action.connector_id,
            condition = action.condition if action.condition else None,
            table = action.table if action.table else None,
            body = action.body
        )
        db.add(db_action)
        db.commit()
        db.refresh(db_action)
        return db_action, False

    except SQLAlchemyError as e:
        db.rollback()
        return str(e), True


def update_action(action_id: int, action: schemas.ActionsUpdate, db: Session):
    try:
        db_action = db.query(models.Actions).filter(models.Actions.id == action_id).first()

        if db_action is None:
            return "Data is None", True

        db_action.name = action.name if action.name else db_action.name
        db_action.description = action.description if action.description else db_action.description
        db_action.types = action.types if action.types else db_action.types
        db_action.connector_id = action.connector_id if action.connector_id else db_action.connector_id
        db_action.condition = action.condition if action.condition else db_action.condition
        db_action.table = action.table if action.table else db_action.table
        db_action.body = action.body if action.body else db_action.body

        db.commit()
        db.refresh(db_action)

        return db_action, False

    except SQLAlchemyError as e:
        db.rollback()
        return str(e), True


def delete_action_by_id(action_id: int, db: Session):
    try:
        db_action = db.query(models.Actions).filter(models.Actions.id == action_id).first()

        if db_action is None:
            return "Data is None", True

        db.delete(db_action)
        db.commit()

        return True, False

    except SQLAlchemyError as e:
        db.rollback()
        return str(e), True