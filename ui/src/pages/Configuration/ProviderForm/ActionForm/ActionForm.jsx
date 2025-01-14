import Panel from  "src/components/Panel/Panel"
import style from "./ActionForm.module.css"
import { useState } from "react"
import { LuTrash2 } from "react-icons/lu"
import { FiCheckCircle } from "react-icons/fi"
import Button from "src/components/Button/Button"
import Database from "./Database"
import { useForm } from "react-hook-form"
import Webhook from "./Webhook"


const ActionForm = ({ index = 0, id = undefined, name = "Action", description = "", type = "get", table = "", condition = {}, body = {}, category = 1, schemas = [], expand = false, actions = [], onActionSave = ()=>{}, onActionDelete = ()=>{}})=>{

    const [panelExpand, setPanelExpand] = useState(false)
    const [actionName, setActioName] = useState(name)
    const actionList = actions.map(item=>({ label: item, value: item }))

    const { register, setValue, handleSubmit, control, formState } = useForm({mode : "all"})
    const { errors } = formState


    const onActioNameChange = (name)=>{
        setActioName(name)
    }

    const onActionExpand = (status)=>{
        setPanelExpand(status)
    }

    const saveAction = (data)=>{
        onActionSave(id, data)
    }

    const deleteAction = ()=>{
        onActionDelete(index, id)
    }



    const panelTitle = <div className={style.ActionTitleContainer}>
        <div className={style.ActionTitle}>
            {actionName}
        </div>
        <div> 
            <Button variant="secondary-danger" className="icon-button" onClick={deleteAction} style={{marginRight: "10px"}}>Delete <LuTrash2/></Button> 
            { panelExpand && <Button buttonType="submit" className="icon-button" >Save  <FiCheckCircle/></Button>}
        </div>
    </div>


    return(
        <>
            <form onSubmit={handleSubmit(saveAction)}>
                <Panel title={panelTitle} expandable={true} onExpandCollapse={onActionExpand} data-action-index={index}>
                    {category == 2 && <Database 
                                        register={register} 
                                        setValue={setValue}
                                        control={control} 
                                        errors={errors} 
                                        schemas={schemas} 
                                        id={id}
                                        name={name}
                                        description={description}
                                        type={type}
                                        table={table}
                                        condition={condition}
                                        body={body}
                                        actions={actionList}
                                        onNameChange={onActioNameChange}
                                    /> }
                    {category == 3 && <Webhook 
                                        register={register} 
                                        setValue={setValue}
                                        control={control} 
                                        errors={errors} 
                                        id={id}
                                        name={name}
                                        description={description}
                                        type={type}
                                        body={body}
                                        actions={actionList}
                                        onNameChange={onActioNameChange}
                                    /> }
                    
                </Panel>  
            </form>

        </>
    )


}

export default ActionForm