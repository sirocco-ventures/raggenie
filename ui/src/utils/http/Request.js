import axios from "axios";
import { useTokenStore } from "src/store/authStore";

const defaultConfig = {
    showLoader: true,
    fullLoader: false,
    loaderText: "Getting Data",
    allowHeaders: true,
}

const defaultAxiosConfig = { }


const Request = (method, url, data = {}, params = {}, config = {}, axiosConfig = {} )=>{
    
    let allConfig = {...defaultConfig, ...config}
    let allAxiosConfig = {...defaultAxiosConfig, ...axiosConfig}


    let loaderContainer = document.querySelector(".dashboard-loader-container")
    let loaderTextPara = document.querySelector(".dashboard-loader-message")

    const token = useTokenStore.getState().token;

    if (loaderContainer && allConfig.showLoader) {

        if(allConfig.showLoader){
            loaderContainer.style.display = "block"
        }
    
        if(allConfig.fullLoader){
            loaderContainer.style.width = "100%"
            loaderContainer.style.h = "100%"
        }
    
        if(allConfig.loaderText){
            loaderTextPara.innerHTML = allConfig.loaderText
        }
    }

    let requestConfig = {
        method: method,
        url: url,
        data: data,
        params: params,
        headers: allConfig.allowHeaders ? { 
            Authorization: `Bearer ${token}`,
            ...axiosConfig.headers
        } : {}, 
        ...allAxiosConfig
    };
    

    return new Promise((resolve, reject)=> {
        axios.request(requestConfig).then(response => {
            if (loaderContainer) {
                loaderContainer.style.display = "none";
            }
            
            if (response.data?.status == false) {
                return  reject(response);
            }
            return  resolve(response)
    
        }).catch(error => {
            if (loaderContainer) {
                loaderContainer.style.display = "none";
            }
            if (error.response?.status === 401) {
                window.location.href = '/login';
            }
            return reject(error)
        });
    })
       
}

export default Request