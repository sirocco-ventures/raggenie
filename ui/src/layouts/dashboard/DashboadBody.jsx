
import help from "src/assets/icons/help.svg"
import style from "./Dashboard.module.css"
import { restartBot } from "src/services/BotConfifuration";
import { toast } from "react-toastify";
import Select from "src/components/Select/Select";
import { useState } from "react";

const DashboardBody = ({ title = "Dashboard",options=[], select, children, containerStyle = {}, containerClassName = ""}) => {
    const [selectedOption, setSelectedOption] = useState()
    const handleRestart = (value) => {
        let selectedId = value.value
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
                            <div style={{width: '183px'}}>
                                <Select
                                    options={options}
                                    value={selectedOption}
                                    onChange={(value) => { setSelectedOption(value); handleRestart(value)}}
                                    noMargin={true}
                                    placeholder={'Configuration'}
                                />
                            </div>
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