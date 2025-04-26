// src/ChatBotAPI.js
// import { API_URL } from "src/config/const"
import PostService from "src/utils/http/PostService";
import GetService from "src/utils/http/GetService"
export const chatBotAPI = (contextId, configID, apiURL, message) => {

  // console.log(contextId)
  let axiosConfig = {
    headers: {}
  }

  return PostService(
    apiURL + `/query/query?contextId=${contextId}&configId=${configID}&envId=${0}`,
    { "content": message, "role":"user" }, {showLoader: false,allowAuthHeaders:true}, axiosConfig)
};

export const getChatByContext = (contextId, apiURL) => {
  return GetService(apiURL + `/chat/get/${contextId}`,{},{allowAuthHeaders:false})
}


