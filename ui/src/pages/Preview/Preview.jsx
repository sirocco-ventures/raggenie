import DashboardBody from "src/layouts/dashboard/DashboadBody"
import PreviewChatBox from "./ChatBox"

const Preview = ()=>{ 
    return(
        <DashboardBody title="Preview" containerStyle={{padding: "0px 0px", height: "calc(100vh - 68px)"}}>
            <PreviewChatBox/>
        </DashboardBody>
    )
}

export default Preview