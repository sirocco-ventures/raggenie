import Request from "./Request"

const DeleteService = (url, data = {} , config = {}, axiosConfig = {})=>{
    return Request("delete", url, data, {}, config, axiosConfig)
}

export default DeleteService