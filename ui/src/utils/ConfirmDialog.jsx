import { confirmAlert } from "react-confirm-alert";
import 'react-confirm-alert/src/react-confirm-alert.css';

const defaultValue = {
    icon: <svg xmlns="http://www.w3.org/2000/svg" width="31" height="30" viewBox="0 0 31 30" fill="none">
        <path d="M15.5 20V15M15.5 10H15.5125M28 15C28 21.9036 22.4036 27.5 15.5 27.5C8.59644 27.5 3 21.9036 3 15C3 8.09644 8.59644 2.5 15.5 2.5C22.4036 2.5 28 8.09644 28 15Z" stroke="#FF7F6D" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round" />
    </svg>,
    cancelButtonText: "Cancel",
    confirmButtonText: "Delete",
    deleteButtonIconsvg: <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16" fill="none">
        <path d="M10.6667 4.00016V3.46683C10.6667 2.72009 10.6667 2.34672 10.5213 2.06151C10.3935 1.81063 10.1895 1.60665 9.93865 1.47882C9.65344 1.3335 9.28007 1.3335 8.53333 1.3335H7.46667C6.71993 1.3335 6.34656 1.3335 6.06135 1.47882C5.81046 1.60665 5.60649 1.81063 5.47866 2.06151C5.33333 2.34672 5.33333 2.72009 5.33333 3.46683V4.00016M6.66667 7.66683V11.0002M9.33333 7.66683V11.0002M2 4.00016H14M12.6667 4.00016V11.4668C12.6667 12.5869 12.6667 13.147 12.4487 13.5748C12.2569 13.9511 11.951 14.2571 11.5746 14.4488C11.1468 14.6668 10.5868 14.6668 9.46667 14.6668H6.53333C5.41323 14.6668 4.85318 14.6668 4.42535 14.4488C4.04903 14.2571 3.74307 13.9511 3.55132 13.5748C3.33333 13.147 3.33333 12.5869 3.33333 11.4668V4.00016" stroke="#FF7F6D" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
    </svg>,
    cancelButtonIconsvg: <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16" fill="none">
        <circle cx="8" cy="8" r="7.5" stroke="#3893FF" strokeWidth="1"/>
        <path d="M5 5L11 11M11 5L5 11" stroke="#3893FF" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
    </svg>,
    onCancel: () => { },
    onConfirm: () => { }
};

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
    cancelButton: {
        padding: "3px 13px",
        borderRadius: "4px",
        background: "#ECF5FF",
        border: "none",
        focus: "none",
        color: "#3893FF",
        fontFamily: "Inter",
        fontSize: "16px",
        fontStyle: "normal",
        fontWeight: "500",
        lineHeight: "150%",
        marginLeft: "10px"
    },
    deleteButton: {
        padding: "3px 13px",
        borderRadius: "4px",
        background: "#FFF2F0",
        border: "none",
        focus: "none",
        color: "#FF7F6D",
        fontFamily: "Inter",
        fontSize: "16px",
        fontStyle: "normal",
        fontWeight: "500",
        lineHeight: "150%",
        marginRight: "10px"
    },
    buttonContentAlign: {
        display: "flex",
        flexDirection: "row"
    },
    ButtonIcon: {
        marginLeft: "5px"
    }
};

const confirmDialog = (
    title,
    message,
    deleteButtonIconsvg = defaultValue.deleteButtonIconsvg,
    cancelButtonIconsvg = defaultValue.cancelButtonIconsvg,
    confirmButtonText = defaultValue.confirmButtonText,
    onConfirm = defaultValue.onConfirm,
    config = {}
) => {
    const allConfig = { ...defaultValue, ...config };

    confirmAlert({
        closeOnEscape: true,
        customUI: ({ onClose }) => {
            return (
                <div>
                    <div style={confirmDialogStyle.dialogBody}>
                        <div style={confirmDialogStyle.iconContainer}>
                            {allConfig.icon || defaultValue.icon}
                        </div>
                        <div style={confirmDialogStyle.dialogText}>
                            <h6 style={confirmDialogStyle.dialogMainText}>{title}</h6>
                            <p style={confirmDialogStyle.dialogSubText}>{message}</p>
                        </div>
                        <div style={confirmDialogStyle.actionContainer}>
                            <button
                                style={confirmDialogStyle.deleteButton}
                                onClick={() => {
                                    onConfirm();
                                    onClose();
                                }}
                            >
                                <div style={confirmDialogStyle.buttonContentAlign}>
                                    <div>
                                        {confirmButtonText}
                                    </div>
                                    {deleteButtonIconsvg && (
                                        <div style={confirmDialogStyle.ButtonIcon}>
                                            {deleteButtonIconsvg}
                                        </div>
                                    )}
                                </div>
                            </button>
                            <button
                                style={confirmDialogStyle.cancelButton}
                                onClick={() => {
                                    allConfig.onCancel();
                                    onClose();
                                }}
                            >
                                <div style={confirmDialogStyle.buttonContentAlign}>
                                    <div>
                                        {allConfig.cancelButtonText}
                                    </div>
                                    {cancelButtonIconsvg && (
                                        <div style={confirmDialogStyle.ButtonIcon}>
                                            {cancelButtonIconsvg}
                                        </div>
                                    )}
                                </div>
                            </button>
                        </div>
                    </div>
                </div>
            );
        }
    });
};

export default confirmDialog;