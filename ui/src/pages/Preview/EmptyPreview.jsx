import emptyConfiguationImg from "src/assets/images/empty-configuration.svg"
import style from "./Preview.module.css"
import Button from "src/components/Button/Button"
import { HiOutlinePlusCircle } from "react-icons/hi";
import { Link } from "react-router-dom";

const EmptyPreview = ({message = "", url = "", buttonText = ""})=>{

    return(
        <>
            <div className={style.EmptyDataContainer}>
                <div>
                    <img src={emptyConfiguationImg}/>
                </div>
                <div style={{marginTop: "19px"}}>
                    <span className={style.EmptyDataTitleSpan}>{message}</span>
                </div>
                <div  style={{marginTop: "39px"}}>
                    <Link to={url}>
                        <Button className="icon-button">{buttonText}<HiOutlinePlusCircle size={22} /></Button>
                    </Link>
                </div>
                
            </div>
        </>
    )
}

export default EmptyPreview