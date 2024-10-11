import { API_URL } from "src/config/const"
import PostService from "src/utils/http/PostService"

export const AuthService=(authCredentials)=>{
    console.log(authCredentials);
    return PostService(API_URL + `/login`,authCredentials)
}