import { Outlet} from "react-router-dom";
import { useEffect } from "react";
import GetService from "src/utils/http/GetService";
import { API_URL } from "src/config/const";
import useAppSettings from "src/store/authStore";
import style from "./Dashboard.module.css";
import SideMenu from "./SideMenu";
import { GetUserDetails } from "src/services/Auth";

const DashboardLayout = () => {

  const { username, setUsername } = useAppSettings();

  const fetchUserInfo = () => {
    GetUserDetails().then((response) => {
      const userData = response.data;
      setUsername(userData.data.username);
    })
      .catch((error) => {
        console.error("Error fetching user info:", error);
      });
  };

  useEffect(() => {
    fetchUserInfo();
  }, []);

  return (
    <div className={style.DashboardLayout}>
      <div className={style.SideMenuContainer}>
        <SideMenu username={username} />
      </div>
      <div className={style.DashboardBodyContainer}>
        <Outlet />
      </div>
    </div>
  );
};

export default DashboardLayout;
