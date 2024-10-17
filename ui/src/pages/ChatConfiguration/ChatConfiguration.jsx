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
import { LiaToolsSolid } from "react-icons/lia";
import { FiCheckCircle, FiXCircle} from "react-icons/fi"
import { GoPlus } from "react-icons/go"
import { FaRegArrowAltCircleRight } from 'react-icons/fa';
import { API_URL, BACKEND_SERVER_URL } from 'src/config/const';;
import Select from 'src/components/Select/Select';
import { ToastContainer, toast } from 'react-toastify';
import { v4  as uuid4} from "uuid"
import Capability from './Capability/Capability';
import Modal from 'src/components/Modal/Modal';
import { deleteBotCapability, saveBotCapability, updateBotCapability } from 'src/services/Capability';
import { getBotConfiguration, getLLMProviders, saveBotConfiguration, saveBotInferene, testInference } from 'src/services/BotConfifuration';
import { useNavigate } from 'react-router-dom';
import NotificationPanel from 'src/components/NotificationPanel/NotificationPanel';
import PostService from 'src/utils/http/PostService';
import ToastIcon from "./assets/ToastIcon.svg"
import { RiRestartLine } from 'react-icons/ri';
import { IoMdClose } from 'react-icons/io';


const BotConfiguration = () => {


    const [selectedOptions, setSelectedOptions] = useState([]);
    const [currentConfigID, setCurrentConfigID] = useState(undefined)
    const [currentInferenceID,setCurrentInferenceID] = useState(undefined)
    const [disabledInferenceSave, setDisabledInferenceSave] = useState(true)
    const [showNotificationPanel, setShowNotificationPanel] = useState(false)
    const [notificationMessage, setNotificationMessage] = useState("")
    
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



    const { register: configRegister, setValue: configSetValue, handleSubmit : configHandleSubmit, formState: configFormState, setError: configSetError, clearErrors: configClearErrors, watch: configWatch } = useForm({mode : "all"})
    const { errors: configFormError, } = configFormState

    const { register: inferenceRegister, getValues: inferenceGetValues , setValue: inferenceSetValue, handleSubmit : inferenceHandleSubmit, formState: inferenceFormState, control: inferenceController, trigger: inferenceTrigger, watch: inferenceWatch } = useForm({mode : "all"})
    const { errors: inferenceFormError } = inferenceFormState

    const ToastCloseButton = ({ closeToast }) => {
        return (
          <button className={style.CustomBotCloseButton} onClick={closeToast}>
            <IoMdClose size={18} />
          </button>
        );
      };


    const ToastMessage = ({ message}) => {
        return (
                <div className={style.BotRestartToast}>
                <span className={style.BotRestartMessage}><img src={ToastIcon} alt="toasticon"/>{message}</span>
                <Button onClick={restartChatBot}>
                    Restart Chatbot  <RiRestartLine size={24}/>
                </Button>
            </div>
        );
      };
      

      const restartChatBot = () => {
        toast.dismiss("RAG001"); 
        PostService(API_URL + `/connector/createyaml/${currentConfigID}`, {}, { loaderText: "Restarting Chatbot" })
          .then(() => {
            toast.success("Bot Restarted successfully");
          })
          .catch(() => {
            toast.error("Failed to restart bot");
          });
      };
      
      const onBotConfigSave = (data) => {
        saveBotConfiguration(currentConfigID, data)
          .then((response) => {
            toast.success("Configuration Saved Successfully")
            setCurrentConfigID(response.data.data.configuration.id);
            setActiveTab("inferenceendpoint")
          })
          .catch(() => {
            toast.error("Configuration failed to save");
          });
      };
      

    const getCurrentConfig = (llmsList)=>{
        
        getBotConfiguration().then(response=>{
            let configs = response.data?.data?.configurations
            if(configs?.length > 0){
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
                

                 if(configs[0].capabilities?.length>0){
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

                }
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


    const onTestInference = ()=>{
        inferenceTrigger().then((result)=>{
            if(result){
                testInference(currentConfigID, {
                    "inferenceName": inferenceGetValues("inferenceName"),
                    "inferenceAPIKey": inferenceGetValues("inferenceAPIKey"),
                    "inferenceLLMProvider": selectedProvider.value,
                    "inferenceModelName": inferenceGetValues("inferenceModelName"),
                    "inferenceEndpoint":  inferenceGetValues("inferenceEndpoint"),
                }).then(()=>{
                    toast.success("Inference test successful")
                    setShowNotificationPanel(false);
                    setDisabledInferenceSave(false)
                }).catch(err=>{
                    toast.error("Inference endpoint verification failed")
                    setShowNotificationPanel(true);
                    setNotificationMessage(err.data?.error ?? "Inference endpoint verification failed")
                });
            }
           
        })
    }

    
    const onInferanceSave = (data) => {
        configClearErrors("inferenceProvider")
        if(selectedProvider ==  undefined ){
            configSetError("inferenceProvider", { type:"required", message: "This field is required" });
            return
        }
 

        data["inferenceLLMProvider"] = selectedProvider.value
        saveBotInferene(currentConfigID, currentInferenceID, data).then(() => {
            toast.success("Inference saved successfully")
            toast(
                <ToastMessage message={`Please restart the bot to get changes to take effect.`} />,
                {
                  toastId: "RAG001", 
                  autoClose: false, 
                  hideProgressBar: true,
                  className: style.ToastContainerClass,
                  closeButton: <ToastCloseButton />,
                }
              );
            setShowNotificationPanel(false);
            setActiveTab("capabalities")
        })
        .catch(() => {
            setShowNotificationPanel(true);
            setNotificationMessage(err.data?.error)
            toast.error("Failed to save inference")
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
            editParamsNameRef.current.value = ""
            editParamsDesc.current.value = ""
            toast.success("New parameter added")
    }

    const editParameter = (capabalityIndex, parameters)=>{
      
        setEditCapabilityIndexRef(capabalityIndex)
        setEditParamsIdRef(parameters.parameter_id)
        editParamsNameRef.current.value = parameters.parameter_name
        editParamsDesc.current.value = parameters.parameter_description

        setShowParamsModal(true)


    }

    const deleteParameter = (capabilityIndex, paramsIndex, item)=>{
        let tempCapabalities = JSON.parse(JSON.stringify(capabalities))
        tempCapabalities[capabilityIndex].requirements.splice(paramsIndex, 1)
        setCapabalities(tempCapabalities)
    }

    const resetTestInference = ()=>{
        setDisabledInferenceSave(true)
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
                        <Input 
                                label="Bot Configuration Name" 
                                maxLength={50} 
                                value={configWatch("botName")} 
                                hasError={configFormError["botName"]?.message ? true : false} 
                                errorMessage={configFormError["botName"]?.message}  
                                {...configRegister("botName", { 
                                    required: "This field is required", 
                                    maxLength: {
                                    value: 50,
                                    message: "The maximum length is 50 characters"
                                    },
                                    minLength: {
                                    value: 10,
                                    message: "The minimum length is 20 characters"
                                    }
                                })} 
                                />
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
                                            <Select label={"LLM Provider"} placeholder={llmModels[0]?.label} options={llmModels} value={selectedProvider} onChange={(value)=>{setSelectedProvider(value); resetTestInference() }} />
                                        )}
                                />
                                
                                {configFormError["inferenceProvider"]?.message && <span style={{color: "#FF7F6D"}}>{configFormError["inferenceProvider"]?.message}</span> }
                            </div>   
                            <Input label="Model Name" hasError={inferenceFormError["inferenceModelName"]?.message ? true : false} errorMessage={inferenceFormError["inferenceModelName"]?.message}  {...inferenceRegister("inferenceModelName", { required: "This field is required"})}  onChange={resetTestInference} />
                            <Input label="Endpoint" hasError={inferenceFormError["inferenceEndpoint"]?.message ? true : false} errorMessage={inferenceFormError["inferenceEndpoint"]?.message}  {...inferenceRegister("inferenceEndpoint", { required: "This field is required"})}  onChange={resetTestInference}  />
                            <Input label="API Key" type="password" hasError={inferenceFormError["inferenceAPIKey"]?.message ? true : false} errorMessage={inferenceFormError["inferenceAPIKey"]?.message}  {...inferenceRegister("inferenceAPIKey", { required: "This field is required"})}  onChange={resetTestInference} />
                        </div>
                        { showNotificationPanel && <NotificationPanel message={notificationMessage} containerStyle={{marginBottom: "30px"}} /> }
                        <div className={`${style.SaveConfigContainer} ${style.InferenceSaveContainer}`}>
                            <div style={{flexGrow: 1}}>
                                <Button type="transparent" className="icon-button" onClick={()=>{setActiveTab("configuration")}} > <FaArrowLeft/> Back</Button>
                            </div>
                            <div>
                                 { disabledInferenceSave && <Button onClick={onTestInference} style={{marginRight: "10px"}}> Test <LiaToolsSolid/>  </Button> }
                                <Button buttonType="submit" className="icon-button" disabled={disabledInferenceSave}>  Save <FiCheckCircle /></Button>
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
                                    <Button type="transparent" className="icon-button" onClick={()=>setActiveTab("inferenceendpoint")}> <FaArrowLeft/> Back</Button>
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
