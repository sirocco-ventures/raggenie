import { useEffect } from "react";
import { useSearchParams, useNavigate } from "react-router-dom";
import { storeToken } from "src/store/authStore";

const AuthHandler = () => {
    const [searchParams] = useSearchParams();
    const accessToken = searchParams.get("access_token");
    const navigate = useNavigate();

    useEffect(() => {
        if (accessToken) {
            console.log("Access Token:", accessToken);
            storeToken(accessToken);  
            localStorage.setItem("access_token", accessToken);  
            navigate("/");  
        }
    }, [accessToken, navigate]);

    return (
        <div>
            <h1>Authenticating...</h1>
        </div>
    );
};

export default AuthHandler;
