import {  Outlet, useNavigate} from "react-router-dom";
import { useEffect } from "react";
import useAppSettings from "src/store/authStore";
import style from "./Dashboard.module.css";
import SideMenu from "./SideMenu";
import { GetUserDetails } from "src/services/Auth";


const DashboardLayout = () => {

  const { username, setUsername, authEnabled, isAuthenticated, setIsAuthenticated, setAuthEnabled } = useAppSettings();

  const navigate = useNavigate()

  
  const fetchUserInfo = async() => {
   try{
    const response = await GetUserDetails()
    const userData = response?.data?.data
    console.log(response)
    console.log(userData)
    if(userData){
      const user= userData.username
      setUsername(user.email)
      setAuthEnabled(userData.auth_enabled)
      setIsAuthenticated(true)
    } else {
      throw new Error("Invalid User data")
    }
   }catch(e){
      console.error('Error fetching details',error)
      if(error?.response?.status===401){
        navigate('/login')
      }else {
        console.log('fine')
      }
   }
  }

  useEffect(() => {
    fetchUserInfo()
  }, []);

  return isAuthenticated ? (
    <div className={style.DashboardLayout}>
      <div className={style.SideMenuContainer}>
        <SideMenu username={username || "Guest"} authEnabled={authEnabled} />
      </div>
      <div className={style.DashboardBodyContainer}>
        <Outlet />
      </div>
    </div>
  ) : null; 
};


export default DashboardLayout;
