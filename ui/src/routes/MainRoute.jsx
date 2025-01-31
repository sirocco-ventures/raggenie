import { Routes, Route, Navigate } from "react-router-dom"
import DashboardLayout from "src/layouts/dashboard/Dashboard"
import routes from "src/config/routes"
import Chat from "src/pages/Chat/Chat"
import { v4 } from "uuid"
import AuthLogin from "src/layouts/auth/AuthLogin"
import CallBack from "src/layouts/callback/CallBack"
import AuthHandler from "src/layouts/auth/AuthHandler"


const MainRoute = () => {

    return (
        <Routes>

            <Route path="/login" element={<AuthLogin />} />
            <Route path="/callback" element={<CallBack />} />
            <Route path="/:contextId/chat" element={<Chat />} />
            <Route path="/auth" element={<AuthHandler />} />



            <Route path="/" element={<Navigate to={`/preview/${v4()}/chat`} repalce={true} />} />

            
                <Route path='/' element={<DashboardLayout />}>
                    {
                        routes.map((item, index) => {
                            return (
                                <Route key={index} path={item.path} element={item.page} />
                            )
                        })
                    }
                </Route>
            


        </Routes>
    )
}

export default MainRoute