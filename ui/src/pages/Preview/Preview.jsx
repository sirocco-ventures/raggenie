import { useState, useEffect } from "react";
import DashboardBody from "src/layouts/dashboard/DashboadBody"
import PreviewChatBox from "./ChatBox"
import { getBotConfiguration } from "src/services/BotConfifuration";


const Preview = ()=>{ 
    const [select, setSelect] = useState(false);
    const [options, setOptions] = useState([]);
    const [selectedOption, setSelectedOption] = useState(null);
    

    const getConfig = ()=>{
            getBotConfiguration().then(response=>{
                let configs = response.data?.data?.configurations
                if(configs?.length > 0){
                    setSelect(true)
                    let configList = []
                    configs.map(item => {
                        configList.push({ value: item.id, label: item.name})
                    })
                    setOptions(configList);  
                    setSelectedOption(configList[0])
                }
            })
        }
    
    useEffect(() => {
        getConfig(); 
    }, []);

    return(
        <DashboardBody title="Preview" options={options} select={select} selectedOption={selectedOption} setSelectedOption={setSelectedOption} containerStyle={{padding: "0px 0px", height: "calc(100vh - 76px)"}}>
            <PreviewChatBox selectedOption={selectedOption} setSelectedOption={setSelectedOption}/>
        </DashboardBody>
    )
}

export default Preview