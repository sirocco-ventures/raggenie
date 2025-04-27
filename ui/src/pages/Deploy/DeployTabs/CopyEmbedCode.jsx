import RouteTab from 'src/components/RouteTab/RouteTab'
import TitleDescription from 'src/components/TitleDescription/TitleDescription'
import { ChatBotEmbeddedCodeTabs } from '../deployTabRoutes'

const CopyEmbedCode = ({currentConfigID}) => {
    return (
        <div>
            <TitleDescription showOrder={false} title={"Select Chatbot Layout"} description={"Pick the ideal table layout to fit your website or app's design."} />
            <RouteTab ContainerStyle={{width:"350px"}} TabStyle={{padding:"13px 4px", width:"fitcontent",fontSize:"14px"}} Deployroutes={ChatBotEmbeddedCodeTabs(currentConfigID)} />
        </div>
    )
}

export default CopyEmbedCode