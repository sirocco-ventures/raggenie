import Request from "./Request"


const GetService = (url, params = {}, config = {}, axiosConfig = {})=>{
     return Request("get", url, {}, params, config, axiosConfig)
}

export default GetService