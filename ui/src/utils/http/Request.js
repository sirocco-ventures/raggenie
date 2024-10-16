import axios from "axios";
import { useNavigate } from "react-router-dom";
import { toast } from "react-toastify";
import { useTokenStore } from "src/store/authStore";

const defaultConfig = {
    showLoader: true,
    fullLoader: false,
    loaderText: "Getting Data"
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
        headers: {
            Authorization: `Bearer ${token}`,
        },
        withCredentials: true, 
        ...allAxiosConfig
    };
    

    return axios.request(requestConfig).then(response => {
        
        if (loaderContainer) {
            loaderContainer.style.display = "none";
        }
        
        if (response.data?.status == false) {
            return new Promise((resolve, reject) => reject(response));
        }
        return new Promise((resolve) => resolve(response))

    }).catch(error => {
        if (loaderContainer) {
            loaderContainer.style.display = "none";
        }
        if (error.response?.status === 401) {
            window.location.href = '/login';
        }
        if (error?.code === "ERR_NETWORK") {
            window.location.href = '/login';
        }
        if (!error.response) {
            toast.error("Network error");
        }
        return Promise.reject(error);
    });
    
   
}

export default Request