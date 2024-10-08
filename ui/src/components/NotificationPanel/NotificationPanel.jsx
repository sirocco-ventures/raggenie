

import style from "./NotificationPanel.module.css";

const NotificationPanel = ({type = "error", message = "", containerStyle = {}, containerClass = ""})=>{


    const getNotificationType = (type)=>{
        switch (type) {
            case "error": return style.NotificationError;
            case "warning": return style.NotificationWarning;
            case "success": return style.NotificationSuccess;
            default: return style.NotificationError;
        }
    }

    return (
        <div className={`${style.NotificationContainer} ${containerClass}`} style={containerStyle}>
             <div className={`${style.NotificationPanel} ${getNotificationType(type)}`}>
                <div> <img src="" className={style.NotificationImg} /> </div>
                <div className={style.NotificationMessage}>{message}</div>
             </div>
        </div>
    )

}

export default NotificationPanel;