import GeneralLayout from "src/layouts/general/GeneralLayout"
import PreviewChatBox from "../Preview/ChatBox"

const Chat = ()=>{ 

    return(
        <>
            <GeneralLayout>
                <div style={{height: "100vh"}}>
                    <PreviewChatBox urlPrex=""/>
                </div>
            </GeneralLayout>
        </>
    )
}

export default Chat