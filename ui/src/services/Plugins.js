import { API_URL } from "src/config/const"
import GetService from "src/utils/http/GetService"

export const getProviders = ()=>{
    return GetService(API_URL + "/provider/list")
}

export const getProviderInfo= (providerId)=>{
    return GetService(API_URL + `/provider/get/${providerId}`)
}