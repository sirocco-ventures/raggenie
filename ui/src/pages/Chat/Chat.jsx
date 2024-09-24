import GeneralLayout from "src/layouts/general/GeneralLayout"
import PreviewChatBox from "../Preview/ChatBox"
import style from "./Chat.module.css"
const Chat = ()=>{ 

    return(
        <>
            <GeneralLayout>
                <div className={style.ChatBody}>
                    <div>
                        <div className={style.ChatHeader}>
                            <span className={style.ChatHeaderTitle}>Rag Assistant</span>
                        </div>
                    </div>
                    <PreviewChatBox urlPrex=""/>
                </div>
            </GeneralLayout>
        </>
    )
}

export default Chat