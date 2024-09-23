
import { Routes, Route } from "react-router-dom"
import DashboardLayout from "src/layouts/dashboard/Dashboard"
import routes from "src/config/routes"
import Chat from "src/pages/Chat/Chat"

const MainRoute = ()=>{

    return(
        <Routes>
            <Route key={"index"} path="/:contextId/chat" element={<Chat/>} />
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