import style from "./ChatBox.module.css"

const Loader = ()=>{

    return(
        <div className={style.Loader}>
            <span></span>
            <span></span>
            <span></span>
        </div>
    )
}

export default Loader