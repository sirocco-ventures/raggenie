import DashboardBody from "src/layouts/dashboard/DashboadBody"
import style from "./Sources.module.css"
import SearchInput from "src/components/SearchInput/SearchInput"
import Connector from "./Connetor"
import { useEffect, useState } from "react"
import { getProviders } from "src/services/Plugins"
import { useNavigate } from "react-router-dom";

const Sources = ()=>{


    const navigate = useNavigate()
    const [sources, setSource] = useState([])
    const [searchedSource, setSearchSource] = useState([])

    const loadSources = ()=>{
        getProviders().then(response=>{
            setSource(response.data.data.providers ?? [])
            setSearchSource(response.data.data.providers ?? [])
        }).catch(() => {
            navigate('/error')
        })
    }

    const onSearchSource = (e)=>{
        let searchValue = e.target.value;
        let searchResult = sources.filter(item=>item.name.toLowerCase().includes(searchValue))
        setSearchSource(searchResult)
    }




    useEffect(()=>{
       loadSources()
    },[])

    return (
        <>
            <DashboardBody title="Plugin List">
                    <SearchInput  placeholder="Search..." style={{width: "400px"}} onChange={onSearchSource} />
                    <div className={style.SourceList}>
                        {searchedSource.map((item, index)=>{
                            return  <Connector connectorId={item.id} plugInkey={item.key} image={item.icon} title={item.name} description={item.description} enabled={item.enable} />
                        })}
                        
                        
                    </div>
            </DashboardBody>
        </>
    )
}


export default Sources