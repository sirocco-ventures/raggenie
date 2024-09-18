
import { Routes, Route } from "react-router-dom"
import routes from "src/config/routes"
import DashboardLayout from "src/layouts/dashboard/Dashboard"

const DashboardRoute = ()=>{

    return(
        <Routes>
            <Route path='/' element={<DashboardLayout/>}>
                {
                routes.map((item, index)=>{
                    return (
                        <Route key={index} path={item.path} element={item.page} />
                    )
                })
                }
            </Route>
      </Routes >
    )

}

export default DashboardRoute