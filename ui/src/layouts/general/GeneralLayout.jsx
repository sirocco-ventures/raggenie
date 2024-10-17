
import style from "src/layouts/dashboard/Dashboard.module.css"

const GeneralLayout = ({children})=>{
    return(
        <>
            <div className={`dashboard-loader-container ${style.LoaderContainer}`}>
                <span className={style.Loader}></span>
                <p className={`dashboard-loader-message ${style.LoaderMessage}`}>Getting Data</p>
            </div>
        <div>
            {children}
        </div>
        </>
    )
}

export default GeneralLayout