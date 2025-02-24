import { useState, useEffect } from "react";
import DashboardBody from "src/layouts/dashboard/DashboadBody"
import PreviewChatBox from "./ChatBox"
import { getBotConfiguration } from "src/services/BotConfifuration";


const Preview = ()=>{ 
    const [select, setSelect] = useState(false);
    const [options, setOptions] = useState([]);

    const getConfig = ()=>{
            getBotConfiguration().then(response=>{
                let configs = response.data?.data?.configurations
                if(configs?.length > 0){
                    setSelect(true)
                    let extractedOptions = configs.map(config => config.id);
                    setOptions(extractedOptions);  
                }
            })
        }
    
    useEffect(() => {
        getConfig(); 
    }, []);

    return(
        <DashboardBody title="Preview" options={options} select={select} containerStyle={{padding: "0px 0px", height: "calc(100vh - 68px)"}}>
            <PreviewChatBox/>
        </DashboardBody>
    )
}

export default Preview