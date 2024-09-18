
import { Routes, Route } from "react-router-dom"
import Chat from "src/pages/Chat/Chat"
import DashboardRoute from "./DashboardRoute"
import DashboardLayout from "src/layouts/dashboard/Dashboard"
import routes from "src/config/routes"

const MainRoute = ()=>{

    return(
        <Routes>
            {/* <Route path="/" element={<Chat/>} /> */}
            {/* <Route path="*" element={<DashboardLayout/>} /> */}
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