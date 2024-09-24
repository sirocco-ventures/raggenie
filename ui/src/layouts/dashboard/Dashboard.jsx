

import { Outlet } from "react-router-dom"
import style from  "./Dashboard.module.css"
import SideMenu from "./SideMenu"

const DashboardLayout = ()=>{

    return(
        <>
            <div className={style.DashboardLayout}>
                <div className={style.SideMenuContainer}>
                    <SideMenu />
                </div>
                <div className={style.DashboardBodyContainer}>
                    <Outlet/>
                </div>
            </div>
        </>
    )
    
}

export default DashboardLayout