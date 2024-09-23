
import help from "src/assets/icons/help.svg"
import style from "./Dashboard.module.css"

const DashboardBody = ({ title = "Dashboard",children, containerStyle = {}, containerClassName = ""}) => {
    return (
        <>
            <div className={`${style.DashboardBody} ${containerClassName}`} >
                
                <div className={style.DashboardHeader}>
                    <div className={style.DashboardTitleContainer}>
                        <span className={style.DashboardTitle}>{title}</span>
                    </div>
                    <div>
                    </div>
                    <div>
                        <a href="https://www.raggenie.com/" target="_blank"> <img className={style.DashboardHeaderIcon} src={help} /></a>
                    </div>
                </div>
                <div className={`dashboard-loader-container ${style.LoaderContainer}`}>
                    <span className={style.Loader}></span>
                    <p className={`dashboard-loader-message ${style.LoaderMessage}`}>Getting Data</p>
                </div>
                <div className={style.DashboardChildrenBody} style={containerStyle}>
                   
                    {children}
                </div>
            </div>

        </>
    )
}

export default DashboardBody