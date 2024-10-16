import { API_URL } from "src/config/const";
import GetService from "src/utils/http/GetService";
import PostService from "src/utils/http/PostService";

export const AuthLoginService = (authCredentials) => {
    return PostService(API_URL + `/login`, authCredentials, { 
        showLoader: false, 
        loaderText: null, 
        fullLoader: false 
    }, {}, true);  
};


export const GetUserDetails = () =>{
    return GetService(API_URL + `/login/user_info`)
}

