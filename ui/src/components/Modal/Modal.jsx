

import closeIcon from "./assets/closeIcon.svg"
import style from "./Modal.module.css"

const Modal = ({title = "", show = "", onClose=()=>{}, children})=>{




    return(
        <div className={`${style.modal} ${show == false ? "": style.modalShow} `}>
            <div className={style.modalHeader}>
                <div className={style.modalTitle}>{title}</div>
                <div className={style.closeIconContainer} onClick={()=>onClose()}><img src={closeIcon}/></div>
            </div>
            <div>
                {children}
            </div>
        </div>
    )
}

export default Modal