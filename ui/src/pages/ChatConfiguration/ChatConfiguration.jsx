import { useEffect, useRef, useState } from 'react';
import Input from 'src/components/Input/Input';
import Tab from 'src/components/Tab/Tab';
import Tabs from 'src/components/Tab/Tabs';
import Textarea from 'src/components/Textarea/Textarea';
import DashboardBody from 'src/layouts/dashboard/DashboadBody';
import style from './ChatConfiguration.module.css';
import { useForm, Controller } from "react-hook-form"
import Button from "src/components/Button/Button"
import { FaArrowLeft } from 'react-icons/fa6';
import { FiCheckCircle, FiXCircle} from "react-icons/fi"
import { GoPlus } from "react-icons/go"
import { FaRegArrowAltCircleRight } from 'react-icons/fa';
import { BACKEND_SERVER_URL } from 'src/config/const';;
import Select from 'src/components/Select/Select';
import { toast } from 'react-toastify';
import { v4  as uuid4} from "uuid"
import Capability from './Capability/Capability';
import Modal from 'src/components/Modal/Modal';
import { deleteBotCapability, saveBotCapability, updateBotCapability } from 'src/services/Capability';
import { getBotConfiguration, getLLMProviders, saveBotConfiguration, saveBotInferene } from 'src/services/BotConfifuration';
import { useNavigate } from 'react-router-dom';


const BotConfiguration = () => {


    const [selectedOptions, setSelectedOptions] = useState([]);
    const [currentConfigID, setCurrentConfigID] = useState(undefined)
    const [currentInferenceID,setCurrentInferenceID] = useState(undefined)
    const [disabledGenerateYAMLButton, setDisabledGenerateYAMLButton] = useState(true)
    
    const [activeInferencepiontTab, setActiveInferencepiontTab] = useState(true)
    const [activeTab, setActiveTab] = useState("configuration")
    

    const [selectedProvider, setSelectedProvider] = useState()

    const [capabalities, setCapabalities] = useState([])

    const [llmModels, setllmModels] = useState([])

    const [editCapabilityIndexRef, setEditCapabilityIndexRef] = useState("")
    const [editParamsIdRef, setEditParamsIdRef] = useState("")
   
    const editParamsNameRef = useRef("");
    const editParamsDesc = useRef("")

    const [showParamsModal, setShowParamsModal] = useState(false)
    let [currentEditParamsNameError, setCurrentEditParamsNameError] = useState({hasError: false, errorMessage: ""})
    let [currentEditParamsDescError, setCurrentEditParamsDescError] = useState({hasError: false, errorMessage: ""})


    const navigate = useNavigate()

    const customSelect = {
        control: (provided) => ({
            ...provided,
            marginBottom: "10px",
            color: '#DDDDDD',
            background: 'transparent',
            fontSize: "14px",
            fontFamily: 'Inter',
            borderColor: '#F0F0F0',
            alignItemsCentre: "center",
            borderRadius: '4px',
            boxShadow: 'none',
            padding: "5px 5px",
            '&:hover': {
                borderColor: '#3893FF;',
                background: "#FFF"
            },
            '&:focus': {
                borderColor: '#3893FF;',
            },
        }),
        menu: (provided) => ({
            ...provided,
            background: 'white',
            borderRadius: '4px',
            boxShadow: '0 2px 8px rgba(0,0,0,0.2)',
            width: '100%',
            fontSize: "14px",
            fontWeight: "400",
            fontFamily: 'Inter'
        }),
        menuList: (provided) => ({
            ...provided,
            background: "#F0F0F0",
        }),
        option: (provided, state) => ({
            ...provided,
            background: state.isSelected ? 'hsl(0deg 78.56% 95%)' : 'white',
            color: state.isSelected ? 'hsl(0deg 78.56% 55%)' : 'black',
            cursor: 'pointer',
           
            '&:hover': {
                background: '#F9F9F9',
            },
        }),
        multiValue: (provided) => ({
            ...provided,
            minWidth: "auto",
            borderRadius: "20px",
            color: '#FFFFFF',
            background: '#74B3FF',
            padding: "3px 6px",
            width: "max-content",
            cursor: "pointer",
            '&:hover': {
                background: '#3893FF',
            },

        }),
        multiValueLabel: (provided) => ({
            ...provided,
            fontSize: "14px",
            color: '#FFFFFF',
            fontFamily: 'Inter'
        }),
        indicatorSeparator: (provided) => ({
            ...provided,
            display: 'none'
        }),
        indicatorContainer: (provided) => ({
            ...provided,
            display: 'none'
        }),
        multiValueRemove: (provided) => ({
            ...provided,
            color: 'white',
            ':hover': {
                background: 'transparent',
                color: 'white',
            },
        }),
    };


    const { register: configRegister, setValue: configSetValue, handleSubmit : configHandleSubmit, formState: configFormState, setError: configSetError, clearErrors: configClearErrors, watch: configWatch } = useForm({mode : "all"})
    const { errors: configFormError, } = configFormState

    const { register: inferenceRegister, setValue: inferenceSetValue, handleSubmit : inferenceHandleSubmit, formState: inferenceFormState, control: inferenceController } = useForm({mode : "all"})
    const { errors: inferenceFormError } = inferenceFormState


    const onBotConfigSave = (data) => {
        saveBotConfiguration(currentConfigID, data ).then(response => {
                setActiveInferencepiontTab(false)
                setCurrentConfigID(response.data.data.configuration.id)
                toast.success("Configuration saved successfully:")
                setActiveTab("inferenceendpoint")
        })
        .catch(() => {
            toast.error("Configuration faild to save")
        });
    }

    const getCurrentConfig = (llmsList)=>{
        
        getBotConfiguration().then(response=>{
            let configs = response.data?.data?.configurations
            if(configs?.length > 0){
                setDisabledGenerateYAMLButton(false)
                setActiveInferencepiontTab(false)
                setCurrentConfigID(configs[0].id)
                setCurrentInferenceID(configs[0].inference[0]?.id ?? undefined)
                
                configSetValue("botName", configs[0].name, {shouldValidate: true, shouldTouch: true})
                configSetValue("botShortDescription", configs[0].short_description)
                configSetValue("botLongDescription", configs[0].long_description)
                
                
                let tempSelectedCapabilities = [];
                configs[0].capabilities.map(cap => {
                    tempSelectedCapabilities.push({ value: cap.id, label: cap.name })
                })
                setSelectedOptions(tempSelectedCapabilities)
                console.log({k :configs[0].inference[0]?.id})

                if(configs[0].capabilities?.length == 0) {
                    setCapabalities([{id: undefined, title:`Capability 1`, name:"", description:"", requirements: [], isCollapse: false}])
                }else{
                    setCapabalities(configs[0].capabilities)
                }

                if(configs[0].inference[0]?.id){
                    let inference = configs[0].inference[0];
                    inferenceSetValue("inferenceName", inference.name)
                    inferenceSetValue("inferenceModelName", inference.model)
                    inferenceSetValue("inferenceEndpoint", inference.endpoint)
                    inferenceSetValue("inferenceAPIKey", inference.apikey)

                    
                    let tempSelectedProvider = llmsList.find(item=>item.value == inference.llm_provider )
                    
                    setSelectedProvider(tempSelectedProvider)

                    setDisabledGenerateYAMLButton(false)

                }else{
                    setDisabledGenerateYAMLButton(true)
                }
            }else{
                setDisabledGenerateYAMLButton(true)
            }
        })
    }

   
    const getLLMModels = async ()=>{
        getLLMProviders().then(response=>{
            var llmProviders = response.data.data?.providers

            let llmList = []
            llmProviders.map(item=>{
                llmList.push({ value: item.unique_name, label: <div className={style.AlignDropdownOptions}><img src={`${BACKEND_SERVER_URL}${item.icon}`} alt={item.display_name} />{item.display_name}</div> },)
            })

            setllmModels(llmList)
            setSelectedProvider(llmList[0])
            getCurrentConfig(llmList)
        })
    }


    
    const onInferanceSave = (data) => {
        configClearErrors("inferenceProvider")
        if(selectedProvider ==  undefined ){
            configSetError("inferenceProvider", { type:"required", message: "This field is required" });
            return
        }


       
        saveBotInferene(currentConfigID, currentInferenceID, data, selectedProvider.value).then(() => {
            toast.success("Inference saved successfully")
        })
        .catch(() => {
            toast.error("Inference saved failed")
        });
    }


    const addNewCapability = ()=>{
        //console.log({capabalities})
        let tempCapabalities = JSON.parse(JSON.stringify(capabalities))
        tempCapabalities.push({
            id: undefined, title:`Capability ${tempCapabalities.length + 1}`, name:"", description:"", requirements: []
        })
        // console.log({capabalities})
        setCapabalities(tempCapabalities)
    }


    const onSaveCapability = (formData)=>{

        let capabilityId = formData.get("capability-id")
        let paramsIds = formData.getAll("params-id[]")
        let paramsNames = formData.getAll("params-name[]")
        let paramsDescs = formData.getAll("params-description[]")
        let requirements = [];
        
        paramsIds?.map((item, index)=>{
            requirements.push({
                parameter_id: item,
                parameter_name: paramsNames[index],
                parameter_description: paramsDescs[index]
            })
        })
    

        if(requirements.length == 0){
            toast.error("Parameter is missing");
            return 
        }


        if(capabilityId == ""){
            saveBotCapability(currentConfigID, formData.get("capability-name"), formData.get("capability-description"), requirements).then(response=>{
                toast.success("Capability saved")
            }).catch(()=>{
                toast.error("Capability save failed")
            })

        }else{
            updateBotCapability(capabilityId, currentConfigID, formData.get("capability-name"), formData.get("capability-description"), requirements).then(response=>{
                toast.success("Capability updated")
            }).catch(()=>{
                toast.error("Capability update failed")
            })
        }

    }

    const deleteCapability = (capabilityIndex, capabilityId)=>{
        deleteBotCapability(capabilityId).then(()=>toast.success("Capability deleted")).catch(()=>toast.error("Capability deletion failed"))
    }
    
    const onClickNewParams = (capabilityId, capabilityIndex)=>{
        // editCapabilityIndexRef.current.value = capabilityIndex
        setEditCapabilityIndexRef(capabilityIndex)
        setShowParamsModal(true)
    }

    const addNewParameter = ()=>{

        setCurrentEditParamsNameError({hasError: false, errorMessage: ""})
        setCurrentEditParamsDescError({hasError: false, errorMessage: ""})
        if(editParamsNameRef.current.value == "" || editParamsDesc.current.value == ""){
            if(editParamsNameRef.current.value == ""){
                setCurrentEditParamsNameError({hasError: true, errorMessage: "This field is required"})
            }

            if(editParamsDesc.current.value == ""){
                setCurrentEditParamsDescError({hasError: true, errorMessage: "This field is required"})
            }

            return 
        }

        console.log({ k: editCapabilityIndexRef})
        capabalities?.map((item, index)=>{
               
                if(index == editCapabilityIndexRef){
                    let hasParam = item.requirements?.some(params => params.parameter_id == editParamsIdRef)
                    //console.log({k: currentEditParamsId, hasParam})
                    if(hasParam){
                        item.requirements?.map(params=>{
                            if(params.parameter_id == editParamsIdRef){
                                params.parameter_name = editParamsNameRef.current.value;
                                params.parameter_description = editParamsDesc.current.value;
                            }
                        })
                    }else{
                        item.requirements?.push({
                            parameter_id:  editParamsIdRef == "" ? uuid4() : editParamsIdRef,
                            parameter_name: editParamsNameRef.current.value,
                            parameter_description: editParamsDesc.current.value
    
                        })
                    }
                    
                }
            })
            //console.log({tempCap})
            // editCapabilityIndexRef.current.value = "";
            // editParamsIdRef.current.value = "";
            // setEditCapabilityIndexRef("")
            // setEditParamsIdRef("")
            editParamsNameRef.current.value = ""
            editParamsDesc.current.value = ""
            toast.success("New parameter added")
    }

    const editParameter = (capabalityIndex, parameters)=>{
      
        // editCapabilityIndexRef.current.value = capabalityIndex
        // editParamsIdRef.current.value = parameters.parameter_id;
        setEditCapabilityIndexRef(capabalityIndex)
        setEditParamsIdRef(parameters.parameter_id)
        editParamsNameRef.current.value = parameters.parameter_name
        editParamsDesc.current.value = parameters.parameter_description

        setShowParamsModal(true)


    }

    const deleteParameter = (capabilityIndex, paramsIndex, item)=>{
        //console.log({capabilityIndex,paramsIndex, item})
        let tempCapabalities = JSON.parse(JSON.stringify(capabalities))
        tempCapabalities[capabilityIndex].requirements.splice(paramsIndex, 1)
        // delete tempCapabalities[capabilityIndex].requirements[paramsIndex]
        setCapabalities(tempCapabalities)
    }



    useEffect(() => {
        getLLMModels();
       
      
    }, [])



    return (
        <DashboardBody title="Bot Configuration">
            <Tabs activeTab={activeTab}>
               
                {/* ==============first tab==================*/}
                <Tab title="Configuration" tabKey="configuration">
                    <h3 className={style.ConfigHeading}>Bot Configuration details</h3>
                    <p className={style.ConfigDescription}>Provide your database connection details and database data description can make your application more efficient.</p>
                    <form onSubmit={configHandleSubmit(onBotConfigSave)}>
                        <div>
                            <Input label="Bot Configuration Name" maxLength={50} value={configWatch("botName")} hasError={configFormError["botName"]?.message ? true : false} errorMessage={configFormError["botName"]?.message}  {...configRegister("botName", { required: "This field is required", maxLength: 50})} />
                            <Input label="Bot Short Description" placeholder="brief detail about the use case of the bot" minLength={20} maxLength={200} value={configWatch("botShortDescription")} hasError={configFormError["botShortDescription"]?.message ? true : false} errorMessage={configFormError["botShortDescription"]?.message}  {...configRegister("botShortDescription", { required: "This field is required", minLength: {value: 20, message : "minimun length is 20"}, maxLength: {value: 200, message: "maximum length is 200"}})}  />
                            <Textarea label="Bot Long Description" placeholder="detailed information about the bot, including its full use case and functionalities" rows={10} minLength={50} maxLength={400} value={configWatch("botLongDescription")} hasError={configFormError["botLongDescription"]?.message ? true : false} errorMessage={configFormError["botLongDescription"]?.message}  {...configRegister("botLongDescription", { required: "This field is required", minLength:{value: 50, message: "minimun length is 50"}, maxLength: {value: 400, message: "maximum length is 400"}})} />
                            
                            <div className={`${style.ConfigSaveContainer} ${style.SaveConfigContainer}`}>
                                <div>
                                    <Button buttonType="submit" className="icon-button">  Save & Continue <FaRegArrowAltCircleRight /></Button>
                                </div>
                            </div>
                        </div>
                    </form>
                </Tab>

                {/*==============second tab==================*/}
                <Tab title="Inference Endpoint" disabled={activeInferencepiontTab} tabKey="inferenceendpoint">
                    <form onSubmit={inferenceHandleSubmit(onInferanceSave)}>
                        <div>
                            <Input label="Name" hasError={inferenceFormError["inferenceName"]?.message ? true : false} errorMessage={inferenceFormError["inferenceName"]?.message}  {...inferenceRegister("inferenceName", { required: "This field is required", maxLength: 50})} />
                            <div style={{marginBottom: "30px"}}>
                                <Controller
                                    control={inferenceController}
                                    name='inferenceProvider'
                                    render={() => (
                                            <Select label={"LLM Provider"} placeholder={llmModels[0]?.label} options={llmModels} value={selectedProvider} onChange={setSelectedProvider} />
                                        )}
                                />
                                
                                {configFormError["inferenceProvider"]?.message && <span style={{color: "#FF7F6D"}}>{configFormError["inferenceProvider"]?.message}</span> }
                            </div>   
                            <Input label="Model Name" hasError={inferenceFormError["inferenceModelName"]?.message ? true : false} errorMessage={inferenceFormError["inferenceModelName"]?.message}  {...inferenceRegister("inferenceModelName", { required: "This field is required"})}  />
                            <Input label="Endpoint" hasError={inferenceFormError["inferenceEndpoint"]?.message ? true : false} errorMessage={inferenceFormError["inferenceEndpoint"]?.message}  {...inferenceRegister("inferenceEndpoint", { required: "This field is required"})}  />
                            <Input label="API Key" hasError={inferenceFormError["inferenceAPIKey"]?.message ? true : false} errorMessage={inferenceFormError["inferenceAPIKey"]?.message}  {...inferenceRegister("inferenceAPIKey", { required: "This field is required"})}  />
                        </div>
                        <div className={`${style.SaveConfigContainer} ${style.InferenceSaveContainer}`}>
                            <div style={{flexGrow: 1}}>
                                <Button type="transparent" className="icon-button" onClick={()=>setActiveTab("configuration")} > <FaArrowLeft/> Back</Button>
                            </div>
                            <div>
                                <Button buttonType="submit" className="icon-button">  Save <FiCheckCircle /></Button>
                            </div>
                        </div>
                    </form>
                </Tab>
                <Tab title="Capabilities" disabled={activeInferencepiontTab} tabKey="capabalities" key={"capabalities"}>
                            <div style={{marginBottom: "30px"}}>
                                <h4>Capabilities details</h4>
                                <p>Explore and define the functionalities offered by the plugin. By incorporating additional capabilities, you can maximize its benefits and fully leverage the plugin's potential.</p>
                            </div>
                            <div className="text-align-right margin-bottom-10">
                               <Button variant="secondary" className="icon-button" onClick={addNewCapability}>New Capability <GoPlus/> </Button>
                            </div>
                            <div>
                                {capabalities?.map((item, index)=>{
                                    return <Capability  
                                                key={index}
                                                capabilityId={item.id} 
                                                capabilityIndex={index} 
                                                title={item.name == ""  ? item.title : item.name} 
                                                name={item.name}
                                                description={item.description} 
                                                parameters={item.requirements}
                                                isCollapse={item.isCollapse}
                                                onCapabilitySave={onSaveCapability}
                                                onParamEdit={editParameter}
                                                onParamDelete={deleteParameter}
                                                onCapabilityDelete={deleteCapability}
                                                onCreateNewParam={onClickNewParams} 
                                            />
                                })}
                                
                            </div>
                            <div className={style.ActionDiv}>
                                <div style={{flexGrow: 1}}>
                                    <Button type="transparent" className="icon-button" onClick={()=>setCurrentActiveTab("documentation")}> <FaArrowLeft/> Back</Button>
                                </div>
                                <div>
                                    <Button buttonType="submit" className="icon-button" onClick={()=>navigate("/plugins")}>  Finish  <FiCheckCircle/></Button>
                                </div>
                            </div>
                    </Tab>
            </Tabs>

            <Modal title="Create New Parameter" show={showParamsModal} onClose={()=>setShowParamsModal(false)}>
                    <div>
                        <Input  type="hidden" value={editCapabilityIndexRef} /> 
                        <Input  type="hidden" value={editParamsIdRef}  />  
                        <Input ref={editParamsNameRef} label={<>Name <span style={{color:"red"}}>*</span></>}  hasError={currentEditParamsNameError.hasError} errorMessage={currentEditParamsNameError.errorMessage} />
                        <Textarea ref={editParamsDesc} label={<>Description <span style={{color:"red"}}>*</span></>} rows={10} hasError={currentEditParamsDescError.hasError} errorMessage={currentEditParamsDescError.errorMessage} />
                    </div>
                    <div className="text-align-right">
                        <Button variant="secondary-danger" className="icon-button" onClick={()=>setShowParamsModal(false)} style={{marginRight: "10px"}}>Cancel <FiXCircle/></Button>
                        <Button className="icon-button" onClick={addNewParameter}>Save <FiCheckCircle/></Button>
                    </div>
                </Modal>

        </DashboardBody>
    );
};

export default BotConfiguration;
