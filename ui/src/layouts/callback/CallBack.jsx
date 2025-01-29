import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { storeToken } from "src/store/authStore";

const BACKEND_CALLBACK_URI = "http://localhost:5000/callback";

const CallBack = () => {
    const navigate = useNavigate();
    const [isLoading, setIsLoading] = useState(true)

    useEffect(() => {
        const params = new URLSearchParams(window.location.search);
        const code = params.get("code");
        console.log(code)

        if (code) {
            fetch(`${BACKEND_CALLBACK_URI}?code=${code}`)
                .then(async (response) => {
                    if (response.ok) {
                        const data = await response.json();
                        const { access_token, user_info } = data;

                     
                        storeToken(access_token);
                        console.log("Access Token:", access_token);

                         
                        navigate("/dashboard");
                    } else {
                        console.error("Failed to fetch access token:", await response.text());
                        navigate("/login");
                    }
                })
                .catch((error) => {
                    console.error("Error during callback processing:", error);
                    navigate("/login");
                })
                .finally(() => setIsLoading(false));
        } else {
            console.error("Authorization code not found in the URL.");
            navigate("/login");
        }
    }, [navigate]);

    return (
        <div>
            {isLoading ? (
                <div>Authenticating Process...</div>  
            ) : (
                <div>Redirecting...</div>  
            )}
        </div>
    );
};

export default CallBack;
