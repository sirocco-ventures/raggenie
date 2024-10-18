
import { SLACK_URL } from "src/config/const"
import slackIcon from "./assets/slack-icon.svg"
import closeIcon from "./assets/error-close.svg"
import style from './ChatBox.module.css'

const ErrorMessage = ({ error = "", onClose = ()=>{}})=>{

    return(
        <div className={style.ErrorContainer}>
            <div className={style.ErrorHeaderContainer}>
                <div className={style.ErrorHeadingContainer}>
                    <h1 className={style.ErrorHeading}>An unexpected error has occurred</h1>
                </div>
                <div>
                    <img src={closeIcon} className={style.ErrorCloseIcon} onClick={onClose} />
                </div>
            </div>
           
            <p className={style.ErrorDescription}>{error}</p>
            <a href={SLACK_URL} target="_blank" className={style.ErrorButtonAnchor}>
                <button className={style.ErrorActionButton}>Contact Us <img src={slackIcon}/></button>
            </a>
        </div>
    )
}

export default ErrorMessage