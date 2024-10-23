import { useState } from "react";
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

const SideMenu = ({ username }) => {

    const [isDropdownOpen, setIsDropdownOpen] = useState(false);
    const navigate = useNavigate(); 


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
                AuthLogoutService().then((response) => {
                    navigate("/login");
                    toast.success(response.data.message);
                    storeToken(null) 
                }).catch((error) => {
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

                {isDropdownOpen && (
                    <div className={style.DropdownMenu}>
                        {UserNameDetails.map((item, index) => (
                            <ul key={index} className={style.MenuList} onClick={() => onHandleClick(item.action)}>
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
