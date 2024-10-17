

export const showDashboardLoader = ()=>{
    let loaderDiv = document.querySelector(".dashboard-loader-container");
    loaderDiv.style.display = "block"
}

export const hideDashboardLoader = ()=>{
    let loaderDiv = document.querySelector(".dashboard-loader-container");
    loaderDiv.style.display = "none"
}


export const isJSON = (json)=>{

    try {
        JSON.parse(json);
        return true;
    } catch (e) {
        return false;
    }
}
