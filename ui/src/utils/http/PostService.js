import Request from "./Request"

const PostService = (url, data = {} , config = {}, axiosConfig = {})=>{
    return Request("post", url, data, {}, config, axiosConfig)
}

export default PostService