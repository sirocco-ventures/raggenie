import { API_URL } from "src/config/const";
import DeleteService from "src/utils/http/DeleteService";
import GetService from "src/utils/http/GetService";
import PostService from "src/utils/http/PostService";

export const getConnectors = (provider_category_id = null)=>{
    if (provider_category_id) {
        return GetService(API_URL + `/connector/list?provider_category_id=${provider_category_id}`);
    }
    return GetService(API_URL + "/connector/list")
}

export const getConnector = (connectorId)=>{
    return GetService(API_URL + `/connector/get/${connectorId}`)
}

export const saveConnector = (connectorId = undefined, connectorType, connectorName, connectorDescription, connectorConfig = {})=>{
    let apiURL = "/connector/create";
    if(connectorId){
        apiURL = `/connector/update/${connectorId}`;
    }
    return PostService(API_URL + apiURL,{
        connector_type: connectorType,
        connector_name: connectorName,
        connector_description: connectorDescription,
        connector_config: connectorConfig
    })
}

export const deleteConnector = (connectorId)=>{
    return PostService(API_URL + `/connector/delete/${connectorId}`);
}

export const updateDocument = (connectorId, document)=>{
    return PostService(API_URL + `/connector/update/${connectorId}`,{connector_docs: document})
}

export const updateSchema = (connectorId, schema)=>{
    return PostService(API_URL + `/connector/schema/update/${connectorId}`,{schema_config: schema})
}

export const healthCheck=(providerId, parameters={})=>{
    return PostService(API_URL + `/provider/${providerId}/test-credentials`,parameters)
}