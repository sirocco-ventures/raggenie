import { API_URL } from "src/config/const"
import DeleteService from "src/utils/http/DeleteService"
import PostService from "src/utils/http/PostService"

export const saveBotCapability = async (configurationId, capabilityName, capabilityDescription, params = {}) => {
    
    let saveData = {
        config_id: configurationId,
        name: capabilityName,
        description: capabilityDescription,
        requirements : params,
    }

    return  PostService(`${API_URL}/capability/create`, saveData, {loaderText : "Saving Capability"})
}

export const updateBotCapability = async (capabilityId, configurationId, capabilityName, capabilityDescription, params = {}) => {
    let updateData = {
        config_id: configurationId,
        name: capabilityName,
        description: capabilityDescription,
        requirements : params,
    }

    return PostService(`${API_URL}/capability/update/${capabilityId}`, updateData, {loaderText : "Updating Capability"})
}

export const deleteBotCapability = async (capabilityId) => {
    return DeleteService(`${API_URL}/capability/delete/${capabilityId}`,{},{loaderText: "Deleting Capability"})
}