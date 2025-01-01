// src/ChatBotAPI.js
// import { API_URL } from "src/config/const"
import PostService from "src/utils/http/PostService";

const chatBotAPI = (message, contextId, apiURL) => {
  // console.log(contextId)
  let axiosConfig = {
    headers: {
      "x-llm-context-id": '1516d185-5bba-4190-8491-caa4999fe322',
    },
  };

  return PostService(
    apiURL + "/query/query",
    { content: message, role: "user" },
    { showLoader: false, allowAuthHeaders: true },
    axiosConfig
  );
};


export default chatBotAPI;
