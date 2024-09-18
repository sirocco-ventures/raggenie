import axios from "axios";

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

    // console.log({allAxiosConfig})

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


    let requestConfig = {
        method: method,
        url: url,
        data: data,
        params: params, 
        ...allAxiosConfig
    }

    // console.log({requestConfig})


    return axios.request(requestConfig).then(response=>{
        loaderContainer.style.display = "none"
        return new Promise((resolve, reject)=>resolve(response))

    }).catch(error=>{
        loaderContainer.style.display = "none"
        console.log({error})
        return new Promise((resolve, reject)=>reject(error))
    })
}

export default Request