
import DashboardBody from "src/layouts/dashboard/DashboadBody"
import EmptyConfiguration from "./EmptyConfiguration"
import ConfigurationList from "./ConfigurationList"
import { useEffect, useState } from "react"
import { useNavigate } from 'react-router-dom';
import { toast } from "react-toastify"
import { deleteBotConfiguration, getBotConfiguration } from "src/services/BotConfifuration";

const ChatConfigurationMain = ()=>{

    const navigate = useNavigate()
    const [configurationList, setConfigurationList] = useState([])

    const loadConfigurations = ()=>{
       getBotConfiguration().then(response=>{
            setConfigurationList(response.data.data.configurations ?? [])
       }).catch(() => {
        navigate('/error')
    })
    }


    const onConfigurationDelete = (configId)=>{
        deleteBotConfiguration(configId).then(response=>{
            if(response.data.status == true){
                toast.success("Configuration Deleted")
                loadConnectors()
            }else{
                toast.error("Opps something went wrong")
            }
        })
    }


    useEffect(()=>{
        loadConfigurations()
    }, [])

    
    return(
        <DashboardBody title="Bot Configuration">
                {configurationList?.length === 0  && <EmptyConfiguration/>}
                {configurationList?.length > 0  && <ConfigurationList configurations={configurationList} onConfigDelete={onConfigurationDelete}/>}
                
        </DashboardBody>
    )
}

export default ChatConfigurationMain
