import { API_URL } from "src/config/const"
import DeleteService from "src/utils/http/DeleteService"
import GetService from "src/utils/http/GetService"
import PostService from "src/utils/http/PostService"



export const getAllActions = ()=>{
    return  GetService(API_URL + `/actions/list`)
}

export const getAllActionsByConnector = (connectorId)=>{
    return  GetService(API_URL + `/actions/${connectorId}/list`)
}

export const saveAction = (actionId, data)=>{
    let apiURL = "/actions/create"
    if(actionId){
        apiURL = `/actions/update/${actionId}`
    }
    return PostService(API_URL + apiURL, data)
}

export const deleteAction = (actionId)=>{
    return DeleteService(API_URL + `/actions/${actionId}`)
}