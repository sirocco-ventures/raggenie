import { useEffect, useState } from "react";
import SideMenuRoutes from "./SideMenuRoutes";
import style from "./Dashboard.module.css";
import raggenieLogo from "../../assets/logo/logo.svg";
import userIcon from "../../assets/icons/header-user-avatar.svg";
import downArrowIcon from "../../assets/icons/chevron-right.svg";
import { NavLink, useNavigate } from "react-router-dom";
import userLogout from "../../assets/icons/menu-icons/log-out.svg";
import { AuthLogoutService } from "src/services/Auth";
import { toast } from "react-toastify";
import { storeToken } from "src/store/authStore";
import { useTokenStore } from "src/store/authStore";
import Cookies from "js-cookie";
import { createZitadelAuth } from "@zitadel/react";
const SideMenu = ({ username, authEnabled }) => {
    const config = {
        authority: "https://flask-auth-pogve2.us1.zitadel.cloud",
        client_id: "301994840332269984",
      };
      const zitadel = createZitadelAuth(config)
      function Logout() {
        zitadel.userManager.signoutRedirect({
             post_logout_redirect_uri: "http://localhost:5000/login"
        }).catch((error) => {
          console.error("Logout failed:", error);
        });
      }
     
    const [isDropdownOpen, setIsDropdownOpen] = useState(false);
     
     


    const UserNameDetails = [
        // {
        //     action:"profile",
        //     icon: userProfile,
        //     title: "Profile"
        // },
        {
            action:"logout",
            icon: userLogout,
            title: "Logout"
        }
    ];

    const toggleDropdown = () => {
        setIsDropdownOpen(!isDropdownOpen);
    };

     
    const onHandleClick = (action) => {
        switch (action) {
            case "logout":
                AuthLogoutService()
                    .then((response) => {
                        console.log("Logging out...");
    
                        // Clear cookies & local storage
                        Cookies.remove("accessToken");
                        localStorage.removeItem("accessToken");
                        sessionStorage.removeItem("accessToken");
    
                        // Update Zustand store
                        useTokenStore.setState({ token: null });
    
                        window.location.href = "/login"
                        toast.success(response.data.message);
                    })
                    .catch((error) => {
                        console.error("Logout failed:", error);
                    });
                break;
            default:
                break;
        }
    };
    return (
        <div className={style.SideMenu}>
            <div className={style.LogoContainer}>
                <img src={raggenieLogo} className={style.AppLogo} />
            </div>
            <div className={style.ProfileContainer}>
                <div className={style.ProfilePanel} onClick={toggleDropdown}>
                    <div>
                        <img src={userIcon} alt="User Icon" />
                    </div>
                    <div className={style.UsernameDiv}>{username}</div>
                    <div>
                        <img src={downArrowIcon} alt="Arrow Icon" />
                    </div>
                </div>

                { authEnabled && isDropdownOpen && (
                    <div className={style.DropdownMenu}>
                        {UserNameDetails.map((item, index) => (
                            <ul key={index} className={style.MenuList} onClick={() =>Logout()}>
                                        <li className={style.menu}>
                                            <img src={item.icon} alt={item.title} /> <span>{item.title}</span>
                                        </li>
                            </ul>
                        ))}
                    </div>
                )}
            </div>

            <div className={style.MenuContainer}>
                <ul className={style.MenuList}>
                    {SideMenuRoutes.map((menu, index) => (
                        <NavLink key={index} to={menu.path}>
                            <li className={style.menu}>
                                <img src={menu.icon} alt={menu.title} /> <span>{menu.title}</span>
                            </li>
                        </NavLink>
                    ))}
                </ul>
            </div>
        </div>
    );
};

export default SideMenu;