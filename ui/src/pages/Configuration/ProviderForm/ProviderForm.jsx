import Tab from "src/components/Tab/Tab"
import Tabs from "src/components/Tab/Tabs"
import DashboardBody from "src/layouts/dashboard/DashboadBody"
import style from "./ProviderForm.module.css"
import Input from "src/components/Input/Input"
import Textarea from "src/components/Textarea/Textarea"
import Button from "src/components/Button/Button"
import Table from "src/components/Table/Table"
import { useForm } from "react-hook-form"
import { FaArrowLeft, FaPen } from "react-icons/fa6";
import { RiPlugLine } from "react-icons/ri";
import { FaRegArrowAltCircleRight } from "react-icons/fa";

import { FiTable} from "react-icons/fi"

import { useEffect, useState, useRef} from "react"
import { useParams, useNavigate, useSearchParams } from "react-router-dom"

import { getConnector, healthCheck, saveConnector, updateSchema, updateDocument} from "src/services/Connectors"
import { toast } from "react-toastify"

import "./DatabaseTable.css"
import TitleDescription from "src/components/TitleDescription/TitleDescription"
import { getProviderInfo } from "src/services/Plugins"


const ProviderForm = ()=>{

    const [providerDetails, setProviderDetails] = useState({})
    const [providerConfig, setProviderConfig] = useState([])
    const [providerSchema, setProviderSchema] = useState([])
    const [currentActiveTab, setCurrentActiveTab] = useState("configuration")
    

    const [disableConnectorSave, setDisableConnectorSave] = useState(true);
    
    let [documentationError, setDocumentationError] = useState({hasError: false, errorMessage: ""})

    let configDocRef = useRef(null)


    let [searchParams] = useSearchParams();

    
    const { register, getValues, handleSubmit, trigger, setValue , formState  } = useForm({mode : "all"})
    const { errors } = formState


    const {providerId, connectorId} = useParams()
    const navigate = useNavigate()


    let tableColumns = [
        
        {
            name: 'Name',
            selector: row =><div className="inline-flex-align-center"> <FiTable color="#BEBEBE" size={16} style={{marginTop: "1px"}}/><span className="">{row.table_name}</span></div>,
            // sortable: true,
            width: "200px"

        },
        {
            name: 'Description',
            grow:1,
            selector: row => {
                return(
                        <div className="textarea-container" style={{position: "relative", zIndex: "10000"}}>
                            <div style={{display: "flex", alignItems: "center"}}> 
                                <div style={{flexGrow : "1"}}>
                                    <textarea key={`textarea-${row.table_id}`} className="textarea" data-type="table" data={`${JSON.stringify(row)}`} data-table-name={`${row.table_name}`} data-table-id={`${row.table_id}`}  style={{display:"none", width: "100%", height: "48px",}} defaultValue={row.description}>{}</textarea>
                                    <span key={`span-${row.table_id}`} className="span" style={{pointerEvents:"none", height: "32px", overflow: "hidden"}}>{row.description}</span>
                                </div>
                                <div className="col-edit">
                                    <FaPen color="#7298ff" style={{pointerEvents: "none"}} />
                                </div>
                            </div>
                        </div>
                )
            }
            // sortable: true,
        }
    
]


    const updateTableDetails = (elem)=>{
        let tempTableDetails =  JSON.parse(window.localStorage.getItem("dbschema")) 

        if(elem){
            if(elem.dataset.type == "table"){
               tempTableDetails[elem.dataset.tableId].description = elem.value

            }else{
                tempTableDetails[elem.dataset.tableId].columns[elem.dataset.columnId].description = elem.value
                
            }
        }
       
        window.localStorage.setItem("dbschema", JSON.stringify(tempTableDetails))
    
    }


    const rowExpandComponent = (row)=>{
        let tempTableDetails =  JSON.parse(window.localStorage.getItem("dbschema")) 
        return(<>
                <div className={style.ExpandRowContainer}>
                    {row?.data?.columns?.map((column, index)=>{
                        return(
                            <div key={index} className={style.ExpandRowDiv}>
                                <div className={`inline-flex-align-center ${ style.ExpandRowCol}`}> <FiTable color="#BEBEBE"/> <span style={{fontSize: "13px"}}>{column.column_name}</span> </div> 
                                <div style={{cursor: "pointer", zIndex: "10000", flexGrow: 1}}>
                                    <div className="child-textarea-container" style={{width: "100%", height: "22px"}}>
                                        <div style={{display: "flex", alignItems: "center"}}>
                                            <div style={{flexGrow: 1}}>
                                                <textarea className="textarea" data-type="column" data={`${JSON.stringify(row.data)}`} data-table-id={`${row.data.table_id}`} data-table-name={`${row.data.table_name}`} data-column-id={`${column.column_id}`} data-column-name={`${column.column_name}`} style={{display:"none", width: "100%", height: "33px", marginTop: "-8px"}} defaultValue={column.description }>{}</textarea>
                                                <span className="span" style={{pointerEvents:"none", height: "24px", overflow: "hidden", fontSize: "13px"}}>{ tempTableDetails[row.data.table_id].columns[column.column_id].description != "" ? tempTableDetails[row.data.table_id].columns[column.column_id].description : column.description}</span>
                                            </div>
                                            <div className="field-edit" style={{paddingRight: "48px"}}>
                                                <FaPen color="#7298ff" size={12} style={{pointerEvents: "none"}}/>
                                            </div>
                                        </div>
                                      
                                    </div>    
                                </div> 
                            </div>
                            
                        )
                    })}
                </div>
        </>)
    }

    const onRowExpand = (expandState)=>{
       
        if(expandState == true){
            setTimeout(()=>{
                let elem = document.querySelectorAll(".field-edit");
                
                for (let index = 0; index < elem.length; index++) {
                    
                    let targetElem = elem[index].parentElement.parentElement

                    targetElem.addEventListener("click",()=>{
                        targetElem.querySelector(".textarea").addEventListener("focusout", (event) => {
                            targetElem.querySelector(".textarea").style.display = "none"
                            targetElem.querySelector(".span").style.display = "block"
                            targetElem.querySelector(".span").innerText = targetElem.querySelector(".textarea").value
                            
                            let txtElem = targetElem.querySelector(".textarea")
                            let tempTableDetails =  JSON.parse(window.localStorage.getItem("dbschema")) 
                            tempTableDetails[txtElem.dataset.tableId].columns[txtElem.dataset.columnId].description = txtElem.value
                            
                            window.localStorage.setItem("dbschema", JSON.stringify(tempTableDetails))
                        
                    });

                    if(targetElem.querySelector(".textarea").style.display == "none"){
                            targetElem.querySelector(".textarea").style.display = "block"
                            targetElem.querySelector(".textarea").focus()
                            targetElem.querySelector(".span").style.display = "none"
                        }else{
                            targetElem.querySelector(".textarea").style.display = "none"
                            targetElem.querySelector(".span").style.display = "block"
                        }

                    })

                }
            },1000)
            
        }
    }


    const getProviderDetails = ()=>{

        getProviderInfo(providerId).then(response=>{
            let data = response.data.data;
            setProviderDetails({
                name: data.provider.name,
                description:  data.provider.description,
                icon: data.provider.icon,
                category_id: data.provider.category_id,
                enable: data.provider.enable
            })

            setProviderConfig(data.provider.configs)
            if(connectorId){
                getConnectDetails();
            }
           
        })
    }
    
    const getConnectDetails = ()=>{
        getConnector(connectorId).then(response=>{
            let connectorData = response.data.data.connector;
            let connectorConfig = response.data.data.connector.connector_config

           
            setValue("pluginName", connectorData.connector_name )
            setValue("pluginDescription", connectorData.connector_description )

            for( let key in connectorConfig){
                setValue(key, connectorConfig[key])
            }

            configDocRef.current.value = connectorData.connector_docs
            setProviderSchema(connectorData.schema_config ?? [])


            let tempSaveTableDetails = {}
            connectorData.schema_config?.map(item=>{
                if(!tempSaveTableDetails[item.table_id]){
                    tempSaveTableDetails[item.table_id] = { table_id: item.table_id, table_name: item.table_name, description: item.description, columns: {}}
                }
                
                item?.columns?.map(col=>{
                    if(!tempSaveTableDetails[item.table_id].columns[col.column_id]){
                        tempSaveTableDetails[item.table_id].columns[col.column_id] = { column_id: col.column_id, column_name: col.column_name, description :col.description }
                    }
                    
                })
                
            })

    

          
            window.localStorage.setItem("dbschema", JSON.stringify(tempSaveTableDetails))
            
        })
    }


    const getConfigFormData = async ()=>{
        let slugs = await providerConfig.map(item=>item.slug)
        let formValues = {};
        let formFilled = true
        slugs.forEach((input)=>{
            formValues[input] = getValues(input)
            if(formValues[input] == ""){
                trigger(input)
                formFilled = false
            }
        });
        return {formValues, formFilled}
    }
    
    const generateConfig = ()=>{

        providerConfig.sort((firstItem, secondItem)=>{
            return firstItem.order > secondItem.order ? -1 : 1
        })

        return(
            <>
                {providerConfig.map((item, index)=>{
                
                    switch(item.config_type){
                        case 1: return <Input key={index} type="text" label={item.name} placeholder={item.description}  hasError={errors[item.slug]?.message ? true : false} errorMessage={errors[item.slug]?.message} {...register(item.slug, {required: "This is required"})} />     
                        case 2: return <Input key={index} type="password" label={item.name} placeholder={item.description} hasError={errors[item.slug]?.message ? true : false} errorMessage={errors[item.slug]?.message}  {...register(item.slug, {required: "This is required"})} />  
                        case 3: return <Input key={index} type="number" label={item.name} placeholder={item.description} hasError={errors[item.slug]?.message ? true : false} errorMessage={errors[item.slug]?.message} {...register(item.slug, {required: "This is required"})} />  
                        case 4: return <Input key={index} type="url" label={item.name} placeholder={item.description} hasError={errors[item.slug]?.message ? true : false} errorMessage={errors[item.slug]?.message} {...register(item.slug, {required: "This is required"})} />  
                        case 5: return <Input key={index} type="email" label={item.name} placeholder={item.description} hasError={errors[item.slug]?.message ? true : false} errorMessage={errors[item.slug]?.message} {...register(item.slug, {required: "This is required"})} />  
                        case 6: return (
                            <div className={style.SelectDropDown}>
                                <label className={style.SelectDropDownLabel}>{item.name}</label>
                                <select key={index} className={`${errors[item.slug]?.message ? style.SelectHasError : ""}`} {...register(item.slug, {required: "This is required"})}>
                                    {item.value?.map((val, valIndex)=>{
                                        return <option key={valIndex} value={val.value}>{val.label}</option>
                                    })}
                                </select>
                                {errors[item.slug]?.message != "" && <label className={style.SelectErrorMessage}>{errors[item.slug]?.message}</label>}
                            </div>
                        )
                        case 7: return <Textarea key={index} rows="5" label={item.name} placeholder={item.description} hasError={errors[item.slug]?.message ? true : false} errorMessage={errors[item.slug]?.message} {...register(item.slug, {required: "This is required"})} />  
                        default : return <Input key={index} type="text" label={item.name} placeholder={item.description} hasError={errors[item.slug]?.message ? true : false} errorMessage={errors[item.slug]?.message} {...register(item.slug, {required: "This is required"})} />     
                    }
                
                })}
                
            </>
        )
    }

    const generateGeneralDetails = ()=>{
        return(
            <>
                <div style={{marginBottom: "30px"}}>
                    <h4>Configuration details</h4>
                    <p>{providerDetails.description}</p>
                </div>
                <div>
                    <Input label="Plugin Name" placeholder="Plugin Name" maxLength={20} hasError={errors["pluginName"]?.message ? true : false} errorMessage={errors["pluginName"]?.message}  {...register("pluginName", {required: "This is required"})} />
                    <Textarea label="Plugin Description" placeholder="Describe the plugin's purpose and content in a detailed and informative manner, emphasizing its key features and functionality." rows={8} maxLength={200} hasError={errors["pluginDescription"]?.message ? true : false} errorMessage={errors["pluginDescription"]?.message}  {...register("pluginDescription", {required: "This is required", minLength: {value: 20, message: "minimum length is 20"}})} />
                    {generateConfig()}
                </div>
            </>
        )
    }


    const onSaveConnector = async (data)=>{
       
        let { formValues} = await getConfigFormData()
        saveConnector(connectorId, providerId, data.pluginName, data.pluginDescription, formValues).then(response=>{
            toast.success("Successfuly plugin added")
            if(connectorId == undefined){
                let url = window.location.href.split('/');
                window.location.href = url.join("/") + `/${response.data.data.connector.connector_id}/details?activeTab=database-table`
            }else{
                setCurrentActiveTab("database-table")
            }
        }).catch(e=>{
            toast.error("Plugin saving failed")
        })
        
     }

     
     const onTestConnection = async ()=>{
        let {formValues, formFilled} = await getConfigFormData()
        if(formFilled){
            healthCheck(providerId, { provider_config: formValues }).then(response=>{
                if(response.data.status == false){
                    toast.error("Connection check failed")
                }else {
                    toast.success("Connection check Success")
                    setDisableConnectorSave(false)
                }
                
            }).catch(()=>{
                toast.error("Health check failed")
            })
        }
       
     }


     const onSaveDBSchema = (e)=>{
       
        let tempTableDetails = []
        let localTableDetails =  JSON.parse(window.localStorage.getItem("dbschema")) 
        let fullFill = true
        Object.keys(localTableDetails).map(table_id=>{
            let tempCols = [];
            Object.keys(localTableDetails[table_id].columns).map(col_id=>{
                if(localTableDetails[table_id].columns[col_id].description == ""){
                    fullFill = false
                }

                tempCols.push({
                    column_id: col_id,
                    column_name: localTableDetails[table_id].columns[col_id].column_name,
                    description: localTableDetails[table_id].columns[col_id].description
                })
            })


            if(localTableDetails[table_id].description == ""){
                fullFill = false
            }

            tempTableDetails.push({
                table_id: table_id,
                table_name: localTableDetails[table_id].table_name,
                description: localTableDetails[table_id].description,
                columns: tempCols
            })
        })

       

        if(fullFill == false){
            toast.error("Please complete form")
            return
        }

        updateSchema(connectorId, tempTableDetails).then(response=>{
            toast.success("Successfuly saved")
            setCurrentActiveTab("documentation") 
        })
    }


    const onDocumentUpdate = (e)=>{
        e.preventDefault();
        setDocumentationError({hasError: false, errorMessage: ""})
        if(configDocRef.current.value == ""){
            setDocumentationError({hasError: true, errorMessage: "This field is required"})
            return
        }
        updateDocument(connectorId, configDocRef.current.value).then(()=>{
            navigate("/plugins")
        })
    }


    const onBacktoDatabaseTable = ()=>{
        if([2].includes(providerDetails.category_id)){
            setCurrentActiveTab("database-table")
        }else{
            setCurrentActiveTab("configuration")
        }
    }


    useEffect(()=>{
        setTimeout(()=>{
            let elem = document.querySelectorAll(".col-edit");
            for (let index = 0; index < elem.length; index++) {
            elem[index].addEventListener("click",(event)=>{
                
                event.stopPropagation()
                const target = event.target.parentElement.parentElement
                
                target.querySelector(".textarea").addEventListener("focusout", () => {
                    target.querySelector(".textarea").style.display = "none"
                    target.querySelector(".span").style.display = "block"
                    target.querySelector(".span").innerText = target.querySelector(".textarea").value
                    updateTableDetails(target.querySelector(".textarea"))
                });
                
                if(target.querySelector(".textarea").style.display == "none"){
                    target.querySelector(".textarea").style.display = "block"
                    target.querySelector(".textarea").focus()
                    target.querySelector(".span").style.display = "none"
                }else{
                    target.querySelector(".textarea").style.display = "none"
                    target.querySelector(".span").style.display = "block"
                }
                
            });
            }
       }, 1000)


       return()=>{
        let elem = document.querySelectorAll(".textarea-container");
        for (let index = 0; index < elem.length; index++) {
          elem[index].removeEventListener("click",()=>{});
          elem[index].querySelector(".textarea").removeEventListener("focusout", () => {});
        }
       };

    }, [])


    useEffect(()=>{
        getProviderDetails()
        if(searchParams.get("activeTab")){
            setCurrentActiveTab(searchParams.get("activeTab"))
        }
    },[])


    return (
        <>
            <DashboardBody title={providerDetails.name}>
                {/* activeTab={searchParams.get("activeTab") ?? "configuration"} */}
                <Tabs activeTab={currentActiveTab}>
                    <Tab  title="Configuration" tabKey="configuration" key={"configuration"}>
                        <form onSubmit={handleSubmit(onSaveConnector)}>
                            {generateGeneralDetails()}
                            <div className={style.ActionDiv}>
                                <div style={{flexGrow: 1}}>
                                    <Button type="transparent" className="icon-button" onClick={()=>navigate("/plugins")}> <FaArrowLeft/> Cancel</Button>
                                </div>
                                <div>
                                    {disableConnectorSave && <Button style={{marginRight: "10px"}} className="icon-button" disabled={Object.keys(errors).length > 0 ? true : false} onClick={onTestConnection}>  Connection Test <RiPlugLine/></Button>}
                                    <Button buttonType="submit" className="icon-button" disabled={disableConnectorSave} >  Save & Continue <FaRegArrowAltCircleRight/></Button>
                                </div>
                            </div>
                        </form>
                    </Tab>
                   
                     <Tab title="Database Schema" tabKey="database-table" key={"database-table"} disabled={connectorId ? false : true} hide={![2].includes(providerDetails.category_id)}>
                        <TitleDescription title="Schema Details" description="Here are the tables and their columns for the plugin. Please describe the tables and it's column details to improve understanding of the plugin schema structure." />
                        <div style={{marginBottom: "30px"}}>
                            <Table columns={tableColumns} data={providerSchema} expandableRows={true} expandableRowsComponent={rowExpandComponent} onRowExpandToggled={onRowExpand} />

                        </div>
                        <div className={style.ActionDiv}>
                            <div style={{flexGrow: 1}}>
                                <Button type="transparent" className="icon-button" onClick={()=>setCurrentActiveTab("configuration")} > <FaArrowLeft/> Back</Button>
                            </div>
                            <div>
                                <Button className="icon-button" onClick={onSaveDBSchema} >  Save & Continue  <FaRegArrowAltCircleRight/></Button>
                            </div>
                        </div>
                    </Tab>    
                    <Tab title="Documentation" tabKey="documentation" key={"documentation"} disabled={connectorId ? false : true}>
                        <form onSubmit={onDocumentUpdate}>
                            <div style={{marginBottom: "30px"}}>
                                <h4>Documentation details</h4>
                                <p>To fully understand how a plugin functions and how to use it effectively, it’s crucial to consult the provider’s documentation. This documentation often includes important conditions and criteria, offering detailed insights and explanations.</p>
                            </div>
                            <div>
                                <Textarea ref={configDocRef} label="Add your document data here" placeholder="eg: This data doesn't contains gender baised information" rows={18} hasError={documentationError.hasError} errorMessage={documentationError.errorMessage} />
                            </div>
                            <div className={style.ActionDiv}>
                                <div style={{flexGrow: 1}}>
                                    <Button type="transparent" className="icon-button" onClick={onBacktoDatabaseTable}> <FaArrowLeft/> Back</Button>
                                </div>
                                <div>
                                    <Button buttonType="submit" className="icon-button">  Save & Continue <FaRegArrowAltCircleRight/></Button>
                                </div>
                            </div>
                        </form>
                    </Tab>
                </Tabs>
            </DashboardBody>
        </>
    )
}

export default ProviderForm