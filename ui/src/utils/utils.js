

export const showDashboardLoader = ()=>{
    let loaderDiv = document.querySelector(".dashboard-loader-container");
    loaderDiv.style.display = "block"
}

export const hideDashboardLoader = ()=>{
    let loaderDiv = document.querySelector(".dashboard-loader-container");
    loaderDiv.style.display = "none"
}

export const isEmptyJSON = (json)=>{

    if(!json){
        return true
    }

    if(typeof(json) == "string" && json == ""){
        return true
    }
    if(typeof(json) == "object" && Object.keys(json).length == 0){
        return true
    }

    return false
}

