
import { Routes, Route, Navigate} from "react-router-dom"
import DashboardLayout from "src/layouts/dashboard/Dashboard"
import routes from "src/config/routes"
import Chat from "src/pages/Chat/Chat"
import { v4 } from "uuid"

const MainRoute = ()=>{

    return(
        <Routes>
            <Route key={"index"} path="/:contextId/chat" element={<Chat/>} />
            <Route path="/"  element={ <Navigate to={`/preview/${v4()}/chat`} repalce={true} /> } />
            <Route path='/' element={<DashboardLayout/>}>
                {
                routes.map((item, index)=>{
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