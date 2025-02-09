import { redirect } from "react-router-dom";
import { API_URL } from "src/config/const";
import GetService from "src/utils/http/GetService";
import PostService from "src/utils/http/PostService";

export const AuthLoginService = (authCredentials) => {
    return PostService(API_URL + `/auth/login`, authCredentials, { 
        showLoader: false,allowAuthHeaders:false},{});  
};

export const IdpLoginService = () => {
    window.location.href = API_URL + "/auth/login/idp/305901299952517123";
};

export const GetUserDetails = () =>{
    return GetService(API_URL + `/auth/user_info`);
}


export const AuthLogoutService = () => {
    return PostService(API_URL + `/auth/logout`);  
   
};


