
import SideMenuRoutes from "./SideMenuRoutes"
import style from "./Dashboard.module.css"
import raggenieLogo from "../../assets/logo/logo.svg"
import userIcon from "../../assets/icons/header-user-avatar.svg"
import downArrowIcon from "../../assets/icons/chevron-right.svg"
import { NavLink } from "react-router-dom"
const SideMenu = ()=>{

    return(
        <div className={style.SideMenu}>
            <div className={style.LogoContainer}>
                <img src={raggenieLogo} className={style.AppLogo}/>
            </div>
            <div className={style.ProfileContainer}>
                <div className={style.ProfilePanel}>
                    <div>
                        <img src={userIcon} />
                    </div>
                    <div className={style.UsernameDiv}>Ashmil Hussian</div>
                    <div>
                        <img src={downArrowIcon} />
                    </div>
                </div>
            </div>
            <div className={style.MenuContainer}>
                <ul className={style.MenuList}>
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