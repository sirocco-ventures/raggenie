import emptyPluginImg from "src/assets/images/empty-plugin.svg"
import style from "./Configuration.module.css"
import Button from "src/components/Button/Button"
import { HiOutlinePlusCircle } from "react-icons/hi";
import { Link } from "react-router-dom";
const EmptyConfiguration = ()=>{

    return(
        <>
            <div className={style.EmptyDataContainer}>
                <div>
                    <img src={emptyPluginImg}/>
                </div>
                <div style={{marginTop: "19px"}}>
                    <span className={style.EmptyDataTitleSpan}>You don't have any plugins added, to get started go and add a plugin</span>
                </div>
                <div  style={{marginTop: "39px"}}>
                    <Link to={"/bot-configuration/sources"}>
                        <Button className="icon-button">Add Plugin <HiOutlinePlusCircle size={22} /></Button>
                    </Link>
                </div>
                
            </div>
        </>
    )
}

export default EmptyConfiguration