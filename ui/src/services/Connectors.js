import { useNavigate } from "react-router-dom";
import { API_URL } from "src/config/const";
import DeleteService from "src/utils/http/DeleteService";
import GetService from "src/utils/http/GetService";
import PostService from "src/utils/http/PostService";






export const getConnectors = ()=>{
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
    return DeleteService(API_URL + `/connector/delete/${connectorId}`);
}

export const updateDocument = (connectorId, document)=>{
    console.log(document)
    return PostService(API_URL + `/connector/update/${connectorId}`,{connector_docs: document}).catch(()=>alert(error))
}

export const updateSchema = (connectorId, schema)=>{
    console.log(document)
    return PostService(API_URL + `/connector/schema/update/${connectorId}`,{schema_config: schema})
}

export const healthCheck=(providerId, parameters={})=>{
    return PostService(API_URL + `/provider/${providerId}/test-credentials`,parameters)
}




