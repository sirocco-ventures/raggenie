
import SideMenuRoutes from "./SideMenuRoutes"
import style from "./Dashboard.module.css"
import raggenieLogo from "../../assets/logo/logo.svg"
import userIcon from "../../assets/icons/header-user-avatar.svg"
import downArrowIcon from "../../assets/icons/chevron-right.svg"
import { Link, NavLink } from "react-router-dom"
const SideMenu = ()=>{

    return(
        <div className={style.SideMenu}>
            <div className={style.logoContainer}>
                <img src={raggenieLogo} className={style.appLogo}/>
            </div>
            <div className={style.profileContainer}>
                <div className={style.profilePanel}>
                    <div>
                        <img src={userIcon} />
                    </div>
                    <div className={style.usernameDiv}>Ashmil Hussian</div>
                    <div>
                        <img src={downArrowIcon} />
                    </div>
                </div>
            </div>
            <div className={style.menuContainer}>
                <ul className={style.menuList}>
                    {SideMenuRoutes.map((menu, index)=>{
                        return(<NavLink key={index} to={menu.path}>
                                    <li className={style.menu}>
                                        <img src={menu.icon}/>  <span>{menu.title}</span>
                                    </li>
                            </NavLink>)
                    })}
                </ul>
            </div>
        </div>
    )
}

export default SideMenu