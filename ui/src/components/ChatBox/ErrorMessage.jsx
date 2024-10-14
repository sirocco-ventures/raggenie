
import { SLACK_URL } from "src/config/const"
import slackIcon from "./assets/slack-icon.svg"
import style from './ChatBox.module.css'

const ErrorMessage = ()=>{

    return(
        <div className={style.ErrorContainer}>
            <h1 className={style.ErrorHeading}>500 internal server issue</h1>
            <p className={style.ErrorDescription}>The server encountered an internal error or misconfiguration and was unable to complete your request</p>
            <a href={SLACK_URL} target="_blank" className={style.ErrorButtonAnchor}>
                <button className={style.ErrorActionButton}>Contact Us <img src={slackIcon}/></button>
            </a>
        </div>
    )
}

export default ErrorMessage