
import DashboardBody from "src/layouts/dashboard/DashboadBody"
import EmptyConfiguration from "./EmptyConfiguration"
import ConfigurationList from "./ConfigurationList"
import { useEffect, useState } from "react"

import { toast } from "react-toastify"
import { deleteConnector, getConnectors } from "src/services/Connectors"


const Configuration = ()=>{

    const [configurationList, setConfigurationList] = useState([])

    const loadConnectors = ()=>{
       getConnectors().then(response=>{
            setConfigurationList(response.data.data.connectors ?? [])
       })
    }


    const onConnectorDelete = (connectorId)=>{
        deleteConnector(connectorId).then(response=>{
            if(response.data.status == true){
                toast.success("Plugin Deleted")
                loadConnectors()
            }else{
                toast.error("Opps something went wrong")
            }
        })
    }


    useEffect(()=>{
        loadConnectors()
    }, [])

    
    return(
        <DashboardBody title="Plugin List">
                {configurationList?.length === 0  && <EmptyConfiguration/>}
                {configurationList?.length > 0  && <ConfigurationList configurations={configurationList} onPluginDelete={onConnectorDelete} />}
                
        </DashboardBody>
    )
}

export default Configuration
