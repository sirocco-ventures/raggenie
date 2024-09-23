
import { Link } from "react-router-dom"
import style from "./Sources.module.css"
import { BACKEND_SERVER_URL } from "src/config/const"

const  Connector = ({connectorId, image, title, description, enabled, plugInkey})=>{

    


    return(
        <>
            <Link className={style.ConnectLink} to={enabled == true ? `/plugins/${connectorId}/${plugInkey}` : "" }>
                <div className={style.SourceContainer}>
                    {enabled == false && <div className={style.sourceOverlay}></div>}
                    <div className={style.ConnectorImageContainer}>
                        <img src={`${BACKEND_SERVER_URL}${image}`}/>
                    </div>
                    <div>
                        <h6 className={style.ConnectorTitle}>{title}</h6>
                        <span className={style.ConnectorDescription}>{description}</span>
                    </div>
                </div>
            </Link>
        </>
    )
}

export default Connector