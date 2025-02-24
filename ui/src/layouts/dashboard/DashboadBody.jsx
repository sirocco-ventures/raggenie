
import help from "src/assets/icons/help.svg"
import style from "./Dashboard.module.css"
import { restartBot } from "src/services/BotConfifuration";
import { toast } from "react-toastify";

const DashboardBody = ({ title = "Dashboard",options=[], select, children, containerStyle = {}, containerClassName = ""}) => {
    const handleRestart = (event) => {
        const selectedId = event.target.value;
        restartBot(selectedId)
            .then(() => {
                toast.success(`Configuration ${selectedId} loaded`);
            })
            .catch(() => {
                toast.error("Failed to load configuration");
            });
    };
    return (
        <>
            <div className={`${style.DashboardBody} ${containerClassName}`} >
                
                <div className={style.DashboardHeader}>
                    <div className={style.DashboardTitleContainer}>
                        {select ? (
                            <select onChange={handleRestart} defaultValue="">
                                <option value="" disabled>Select a Configuration</option>
                                {options.map((id) => (
                                    <option key={id} value={id}>Configuration {id}</option>
                                ))}
                            </select>
                        ) : ( 
                        <span className={style.DashboardTitle}>{title}</span> )}
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