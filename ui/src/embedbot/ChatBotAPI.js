// src/ChatBotAPI.js
// import { API_URL } from "src/config/const"
import PostService from "src/utils/http/PostService";
import GetService from "src/utils/http/GetService"

export const chatBotAPI = (contextId, apiURL, message) => {
  // console.log(contextId)
  let axiosConfig = {
    headers: {
      "x-llm-context-id": contextId,
    },
  };

  return PostService(
    apiURL + "/query/query",
    { content: message, role: "user" },
    { showLoader: false, allowAuthHeaders: true },
    axiosConfig
  );
};

export const getChatByContext = (contextId, apiURL) => {
  return GetService(apiURL + `/chat/get/${contextId}`,{},{allowAuthHeaders:false})
}


