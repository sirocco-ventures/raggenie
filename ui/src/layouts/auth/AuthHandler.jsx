import { useEffect } from "react";
import { useSearchParams, useNavigate } from "react-router-dom";
import { storeToken } from "src/store/authStore";

const AuthHandler = () => {
    const [searchParams] = useSearchParams();
    const accessToken = searchParams.get("access_token");
    const clientId = searchParams.get('client_id')
    const navigate = useNavigate();

    useEffect(() => {
        if (accessToken || clientId ) {
            console.log("Access Token:", accessToken);
            console.log('Client ID', clientId)
            storeToken(accessToken);  
            localStorage.setItem("access_token", accessToken);
            localStorage.setItem('client_id',clientId)  
            navigate("/");  
        }else {
            console.error('Missing Token or clientId')

        }
    }, [accessToken, navigate]);

    return (
        <div>
            
        </div>
    );
};

export default AuthHandler;
