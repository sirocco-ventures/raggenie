import {confirmAlert} from "react-confirm-alert"
import 'react-confirm-alert/src/react-confirm-alert.css';

const defaultValue = {
    icon:<svg xmlns="http://www.w3.org/2000/svg" width="31" height="30" viewBox="0 0 31 30" fill="none">
            <path d="M15.5 20V15M15.5 10H15.5125M28 15C28 21.9036 22.4036 27.5 15.5 27.5C8.59644 27.5 3 21.9036 3 15C3 8.09644 8.59644 2.5 15.5 2.5C22.4036 2.5 28 8.09644 28 15Z" stroke="#FF7F6D" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>,
    cancelButtonText : "Cancel",
    confirmButtonText: "Delete",
    cancelButtonIcon: <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16" fill="none">
                            <g clip-path="url(#clip0_3063_7829)">
                                <path d="M10.0007 6.00065L6.00065 10.0007M6.00065 6.00065L10.0007 10.0007M14.6673 8.00065C14.6673 11.6826 11.6826 14.6673 8.00065 14.6673C4.31875 14.6673 1.33398 11.6826 1.33398 8.00065C1.33398 4.31875 4.31875 1.33398 8.00065 1.33398C11.6826 1.33398 14.6673 4.31875 14.6673 8.00065Z" stroke="#3893FF" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                            </g>
                            <defs>
                                <clipPath id="clip0_3063_7829">
                                    <rect width="16" height="16" fill="white"/>
                                </clipPath>
                            </defs>
                      </svg>,
    deleteButtonIcon: <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16" fill="none">
                        <path d="M10.6667 4.00016V3.46683C10.6667 2.72009 10.6667 2.34672 10.5213 2.06151C10.3935 1.81063 10.1895 1.60665 9.93865 1.47882C9.65344 1.3335 9.28007 1.3335 8.53333 1.3335H7.46667C6.71993 1.3335 6.34656 1.3335 6.06135 1.47882C5.81046 1.60665 5.60649 1.81063 5.47866 2.06151C5.33333 2.34672 5.33333 2.72009 5.33333 3.46683V4.00016M6.66667 7.66683V11.0002M9.33333 7.66683V11.0002M2 4.00016H14M12.6667 4.00016V11.4668C12.6667 12.5869 12.6667 13.147 12.4487 13.5748C12.2569 13.9511 11.951 14.2571 11.5746 14.4488C11.1468 14.6668 10.5868 14.6668 9.46667 14.6668H6.53333C5.41323 14.6668 4.85318 14.6668 4.42535 14.4488C4.04903 14.2571 3.74307 13.9511 3.55132 13.5748C3.33333 13.147 3.33333 12.5869 3.33333 11.4668V4.00016" stroke="#FF7F6D" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                      </svg>,
    onCancel: ()=>{},
    onConfirm: ()=>{}
}



const confirmDialogStyle = {
    dialogBody: {
        borderRadius: "8px",
        boxShadow: "0px 4px 20px 0px rgba(0, 0, 0, 0.12)",
        padding: "28px 40px",
        width: "329px"
    },
    iconContainer: {
        textAlign: "center"    
    },
    icon: {
        margin: "auto",
        display: "block",
        marginBottom: "23px",
    },
    dialogText: {
        textAlign: "center"
    },
    dialogMainText: {
        padding: "0px",
        margin: "0px",
        color: '#32324D',
        textAlign: "center",
        fontFamily: "Inter",
        fontSize: "18px",
        fontStyle: "normal",
        fontWeight: "600",
        lineHeight: "22px"
    },
    dialogSubText: {
        color: "#32324D",
        textAlign: "center",
        fontFamily: "Inter",
        fontSize: "14px",
        fontStyle: "normal",
        fontWeight: "400",
        lineHeight: "20px",
        marginBottom: "30px"
    },
    actionContainer: {
        textAlign: "center"
    },
    actionButton: {
        padding: "3px 13px",
        borderRadius: "4px",
        border: "none",
        focus: "none",
        /* Small text */
        fontFamily: "Inter",
        fontSize: "16px",
        fontStyle: "normal",
        fontWeight: "500",
        lineHeight: "150%",
        marginLeft:"10px",
        cursor: "pointer"
    },
    cancelButton: {
        background: "#ECF5FF",
        color: "#3893FF",
    },
    deleteButton: {
        background: "#FFF2F0",
        color: "#FF7F6D",
    },
    buttonContentAlign:{
        display:"flex",
        flexDirection:"row"
    },
    actionButtonIcon: {
        display: "flex",
        alignItems: "center",
        marginLeft: "5px",
    }

}



const  confirmDailog = (title, message, onConfirm = ()=>{}, config = {} )=>{
  

    let allConfig = {...defaultValue, ...config}
    confirmAlert({
        closeOnEscape: true,
        customUI: ({onClose})=>{
            return(<div>
                <div style={confirmDialogStyle.dialogBody}>
                    <div style={confirmDialogStyle.iconContainer}>
                        <svg style={confirmDialogStyle.icon} xmlns="http://www.w3.org/2000/svg" width="31" height="30" viewBox="0 0 31 30" fill="none">
                            <path d="M15.5 20V15M15.5 10H15.5125M28 15C28 21.9036 22.4036 27.5 15.5 27.5C8.59644 27.5 3 21.9036 3 15C3 8.09644 8.59644 2.5 15.5 2.5C22.4036 2.5 28 8.09644 28 15Z" stroke="#FF7F6D" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
                        </svg>
                    </div>
                    <div style={confirmDialogStyle.dialogText}>
                        <h6 style={confirmDialogStyle.dialogMainText}>{title}</h6>
                        <p style={confirmDialogStyle.dialogSubText}>{message}</p>
                    </div>
                    <div style={confirmDialogStyle.actionContainer}>
                        <button style={{...confirmDialogStyle.actionButton,...confirmDialogStyle.cancelButton}} onClick={onClose}>
                            <div style={confirmDialogStyle.buttonContentAlign}>
                                <div>
                                    {allConfig.cancelButtonText} 
                                </div>
                                <div style={confirmDialogStyle.actionButtonIcon}>
                                    {allConfig.cancelButtonIcon}
                                </div>
                            </div>
                        </button>
                        <button style={{...confirmDialogStyle.actionButton,...confirmDialogStyle.deleteButton}} onClick={()=>{ onConfirm(),onClose() }}>
                            <div style={confirmDialogStyle.buttonContentAlign}>
                                <div>
                                    {allConfig.confirmButtonText}
                                </div>
                                <div style={confirmDialogStyle.actionButtonIcon}>
                                    {allConfig.deleteButtonIcon} 
                                </div>
                            </div>
                        </button>
                    </div>
                </div>
            </div>)
        }
    })
}

export default confirmDailog