import { Navigate, Outlet } from "react-router-dom";
import { useTokenStore } from "src/store/authStore";

const ProtectedRoute = () => {
    const token = useTokenStore((state) => state.token);

    if (!token) {
        console.log("No token found, redirecting to login...");
        console.log("Current token in Zustand store:", token);

        return <Navigate to="/login" />;
    }

    console.log("Token found, rendering protected route...");
    return <Outlet />;
};

export default ProtectedRoute;
