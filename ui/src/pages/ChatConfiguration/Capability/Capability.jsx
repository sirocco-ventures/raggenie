

import { IoIosArrowDown, IoIosArrowUp } from "react-icons/io";
import { GoPencil } from "react-icons/go";
import { LuTrash2 } from "react-icons/lu";
import { FiCheckCircle} from "react-icons/fi"
import Button from "src/components/Button/Button";
import Select from "src/components/Select/Select";
import Input from "src/components/Input/Input";
import Textarea from "src/components/Textarea/Textarea";
import { GoPlus } from "react-icons/go"
import { useEffect, useState } from "react";
import style from "./Capability.module.css"


const Capability = ({capabilityId = "", capabilityIndex = 0, title = "", name = "", description = "", parameters = [], actions = [], actionsList = [], isCollapse= true, onCapabilitySave = ()=>{}, onCapabilityDelete = ()=>{}, onParamEdit=()=>{}, onParamDelete = ()=>{}, onCreateNewParam = ()=>{}})=>{

    const [expand, setExpand] = useState(true)
    const [capabilityLitle, setCapabilityLitle] = useState(title)
    const [selectedActions, setSelectedActions] = useState([])
    const actionsForSelect = actionsList?.map(item=>({label: item.name, value: item.id }))

    const onDeleteCapability = ()=> {
        onCapabilityDelete(capabilityIndex, capabilityId)
    }

    const onCreateNewParamClick = ()=>{
        onCreateNewParam(capabilityId, capabilityIndex)
    }

    const onFormSubmit = (e)=>{
        e.preventDefault()
        var data = new FormData(e.target);
        let formActions = selectedActions?.map(item=>item.value)
        formActions.forEach((item) => data.append("actions[]", item))
        onCapabilitySave(data)
    }

    useEffect(()=>{
        setExpand(isCollapse)
        let tempAcitions = actionsForSelect.filter(item=>actions?.includes(item.value))
        setSelectedActions(tempAcitions)
    },[isCollapse])


    return(
        <>
            <form onSubmit={onFormSubmit}>
                <div data-capability-index={`${capabilityIndex}`} data-capability-id={`${capabilityId}`} className={`${style.CapabilityContainer} ${expand == false ? "" : style.CapabilityContainerCollapse}`}>
                    <div className={style.CapabilityHeader}>
                        <div onClick={()=>setExpand(!expand)} style={{cursor: "pointer"}}> {expand == false ? <IoIosArrowUp/> : <IoIosArrowDown/>} </div>
                        <div className={`flex-grow-1 ${style.CapabilityTitle}`}>
                            {capabilityLitle}
                        </div>
                        <div> 
                            <Button variant="secondary-danger" className="icon-button" onClick={onDeleteCapability}  style={{marginRight: "10px"}}>Delete <LuTrash2/></Button> 
                            { !expand && <Button buttonType="submit" className="icon-button" >Save  <FiCheckCircle/></Button>}
                        </div>
                    </div>
                    <div>
                        <div className={style.CapabilityDetailsContainer}>
                            <Input type="hidden" name="capability-id" value={capabilityId}  />
                            <Input label="Capability Name" name="capability-name" value={name}  onChange={(e)=>setCapabilityLitle(e.target.value)} />
                            <Textarea label="Description" name="capability-description" value={description} rows={8}/>
                            <Select label="Select Action" name="capability-actions" isMulti={true} options={actionsForSelect} value={selectedActions} onChange={setSelectedActions} />
                        </div>
                    </div>

                    <div className={style.CapabilityParamsBody}>
                        <div className={style.CapabilityParamsHeader}>
                            <div className={`flex-grow-1 ${style.CapabilityTitle}`}>
                                Create Parameters for Capability
                            </div>
                            <div> 
                                <Button variant="secondary" className="icon-button" onClick={onCreateNewParamClick}>Create New Parameter <GoPlus/></Button> 
                            </div>
                        </div>
                        <div>
                            <table className={style.CapabilityParamsTable}>
                                <thead>
                                    <tr>
                                        <th className={style.CapabilityParamsTableHeader} style={{width: "250px"}}>Name</th>
                                        <th className={style.CapabilityParamsTableHeader}>Description</th>
                                    </tr>
                                </thead>
                                <tbody key={"tbody"}>
                                {parameters?.map((item, index)=>{
                                    return(
                                        <>
                                            <tr key={index}>
                                                <td className={style.CapabilityParamsTableColumn}>
                                                    <Input type="hidden" name="params-id[]" value={item.parameter_id} />
                                                    <Input type="hidden" name="params-name[]" value={item.parameter_name} />
                                                    {item.parameter_name}
                                                </td>
                                                <td className={style.CapabilityParamsTableColumn}>
                                                    <Input type="hidden" name="params-description[]" value={item.parameter_description} />
                                                    {item.parameter_description}
                                                    <span style={{float: "right"}}>
                                                        <GoPencil size={20} color="#3893FF" onClick={()=>onParamEdit(capabilityIndex, item)} style={{marginRight: "23px"}}/>
                                                        <LuTrash2 size={20} color="#FF7F6D" onClick={()=>onParamDelete(capabilityIndex, index, item)}/>
                                                    </span>
                                                </td>
                                            </tr>
                                        </>
                                    )
                                })}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </form>
        </>
    )
}


export default Capability