
import DashboardBody from "src/layouts/dashboard/DashboadBody"
import EmptyConfiguration from "./EmptyConfiguration"
import ConfigurationList from "./ConfigurationList"
import { useEffect, useState } from "react"
import { useNavigate } from 'react-router-dom';
import { toast } from "react-toastify"
import { deleteConnector, getConnectors } from "src/services/Connectors"


const Configuration = ()=>{

    const navigate = useNavigate()
    const [configurationList, setConfigurationList] = useState([])

    const loadConnectors = ()=>{
       getConnectors().then(response=>{
            setConfigurationList(response.data.data.connectors ?? [])
       }).catch(() => {
        navigate('/error')
    })
    }


    const onConnectorDelete = (connectorId)=>{
        deleteConnector(connectorId).then(response=>{
            toast.success("Plugin Deleted")
            loadConnectors()
        }).catch(()=>{
            toast.error("Plugin deletion failed")
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
