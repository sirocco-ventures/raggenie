import Tab from "src/components/Tab/Tab"
import Tabs from "src/components/Tab/Tabs"
import DashboardBody from "src/layouts/dashboard/DashboadBody"
import style from "./ProviderForm.module.css"
import Input from "src/components/Input/Input"
import Textarea from "src/components/Textarea/Textarea"
import Button from "src/components/Button/Button"
import Table from "../SchemaTable/SchemaTable"
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
import FileUpload from "src/components/FileUpload/FileUpload"
import { API_URL } from "src/config/const"
import UploadFile from "src/utils/http/UploadFile"
import GenerateConfigs from "src/utils/form/GenerateConfigs"


const ProviderForm = ()=>{

    const [providerDetails, setProviderDetails] = useState({})
    const [providerConfig, setProviderConfig] = useState([])
    const [providerSchema, setProviderSchema] = useState([])
    const [currentActiveTab, setCurrentActiveTab] = useState("configuration")

    const [filePaths, setFilePaths] = useState([]);
    const [files, setFiles] = useState([]);
    const [showProgressBar, setShowProgressBar] = useState(false);
    const [progressPrecentage, setProgressPrecentage] = useState(0);
    const [progressTime, setProgressTime] = useState('');
    const pdfUploadRef = useRef(null);
    
    

    const [disableConnectorSave, setDisableConnectorSave] = useState(true);
    
    let [documentationError, setDocumentationError] = useState({hasError: false, errorMessage: ""})

    let configDocRef = useRef(null)


    let [searchParams] = useSearchParams();

    
    const { register, getValues, handleSubmit, trigger, setValue , formState  } = useForm({mode : "all"})
    const { errors } = formState


    const {providerId, connectorId} = useParams()
    const navigate = useNavigate()

    const maxFiles = 5; 


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

            const fetchedFiles = connectorConfig.document_files?.map(file => ({
                file_path: file.file_path,
                file_name: file.file_name,
                file_size: parseFloat(file.file_size) * 1024, 
                file_id: file.file_id
            })) || [];

            setFiles(prevFiles => [...prevFiles, ...fetchedFiles]);
            setDisableConnectorSave(false); 


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


    
    const onSaveFiles = (file) => {
        const uploadUrl = API_URL + `/connector/upload/datasource`;
        const formData = new FormData();
        formData.append('file', file);
        setShowProgressBar(true);
    
        return UploadFile(uploadUrl, formData, (percentage, estimatedTime) => {
            setProgressPrecentage(percentage);
            setProgressTime(estimatedTime);
        })
        .then(response => {
            const fileData = response.data.data.file;
            const fileDetails = {
                file_path: fileData.file_path,
                file_name: fileData.file_name,
                file_size: fileData.file_size,
                file_id: fileData.file_id
            };
    
            setFilePaths(prevPaths => [...prevPaths, fileDetails]);
    
            setFiles(prevFiles => [
                ...prevFiles,
                {
                    file_name: file.name,
                    file_size: (file.size / (1024 * 1024)).toFixed(2), // Convert size to MB
                    file_path: fileDetails.file_path, 
                    file_id: fileDetails.file_id,
                }
            ]);
    
            setDisableConnectorSave(true);
            setShowProgressBar(false);
        })
        .catch(error => {
            toast.error('File upload failed', error);
            setShowProgressBar(false);
        })
        .finally(() => {
            setProgressPrecentage(0);
            setProgressTime("");
        });
    };
    

    const getMaxFileSize = (extension) => {
        if (extension === "text/csv") {
            return 100
        } else {
            return 10
        }
    }
 

    const onFileChange = (event) => {
        const selectedFile = event.target.files[0];
        if (!selectedFile) return;
        const maxFileSizeMB = getMaxFileSize(selectedFile.type)
        
        const fileSizeMB = selectedFile.size / (1024 * 1024); 
    
        if (files.length >= maxFiles) {
            toast.error(`You can only upload up to ${maxFiles} files.`)
            return;
        }
    
        if (fileSizeMB > maxFileSizeMB) {
            toast.error(`File size should not exceed ${maxFileSizeMB} MB. The selected file is ${fileSizeMB.toFixed(2)} MB.`)
            return;
        }
    
        if (providerDetails.category_id === 5 && selectedFile.type === "text/csv"){
            onSaveFiles(selectedFile)
        } else if (providerDetails.category_id === 4 && selectedFile.type != "text/csv") {
            onSaveFiles(selectedFile)
        }
        else {
            toast.error("Invalid file type")
        }
    };
    
    const onAddFileOnDrag = (event) => {
        event.preventDefault();
        const draggedFile = event.dataTransfer.files[0];
        const maxFileSizeMB = getMaxFileSize(draggedFile.type)

        if (!draggedFile) return;
    
        const fileSizeMB = draggedFile.size / (1024 * 1024); 
    
        if (files.length >= maxFiles) {
            toast.error(`You can only upload up to ${maxFiles} files.`)
            return;
        }
    
        if (fileSizeMB > maxFileSizeMB) {
            toast.error(`File size should not exceed ${maxFileSizeMB} MB. The selected file is ${fileSizeMB.toFixed(2)} MB.`)
            return;
        }
        if (providerDetails.category_id === 5 && draggedFile.type === "text/csv"){
            onSaveFiles(draggedFile)
        } else if (providerDetails.category_id === 4 && draggedFile.type != "text/csv") {
            onSaveFiles(draggedFile)
        }
        else {
            toast.error("Invalid file type")
        }
    };


const onRemoveFile = (fileId) => {
    const updatedFiles = files.filter(file => file.file_id !== fileId);
    setFiles(updatedFiles);

    const updatedFilePaths = filePaths.filter(filePath => filePath.file_id !== fileId);
    setFilePaths(updatedFilePaths);

    if (updatedFiles.length === 0) {
        setDisableConnectorSave(true);
    }
};


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
    
    
    const generateConfig = () => {

        providerConfig.sort((firstItem, secondItem) => {
            return firstItem.order > secondItem.order ? -1 : 1
        })
        
        const fileConfig = {
            onRemoveFile:onRemoveFile,
            onAddFileOnDrag:onAddFileOnDrag,
            pdfUploadRef:pdfUploadRef,
            title:"Upload your files",
            description:`You can upload up to 5 files, with each file having a maximum size of ${providerDetails.category_id === 5 ? 100 : 10} MB.`,
            accept:providerDetails.category_id === 5 ? ".csv" : ".pdf,.yaml,.txt,.docx",
            dragMessage:"Drag your files to start uploading",
            progressPrecentage:progressPrecentage,
            showProgressBar:showProgressBar,
            progressTime:progressTime,
            onAddFileOnDrag:onAddFileOnDrag,
            onFileChange:onFileChange,
            onRemoveFile:onRemoveFile,
            files:files,
            supportedFileMessage:`${providerConfig[0]?.description}`,
            multipleFileSupport:false
        }


        return (
            <>
                <GenerateConfigs
                    configs={providerConfig}
                    errors={errors}
                    register={register}
                    fileConfig={fileConfig}
                    restForm={onChangesOption}

                />

            </>
        )
    }

    const onChangesOption=()=>{
        if (files.length === 0) {
            setDisableConnectorSave(true);
        }
    }


    const generateGeneralDetails = ()=>{
        return(
            <>
                <div style={{marginBottom: "30px"}}>
                    <h4>Configuration details</h4>
                    <p>{providerDetails.description}</p>
                </div>
                <div>
                    <Input label="Plugin Name" placeholder="Plugin Name" maxLength={20} required hasError={errors["pluginName"]?.message ? true : false} errorMessage={errors["pluginName"]?.message}  {...register("pluginName", {required: "This is required" ,minLength: {value: 10, message: "minimum length is 10"}})} onChange={onChangesOption}/>
                    <Textarea label="Plugin Description" placeholder="Describe the plugin's purpose and content in a detailed and informative manner, emphasizing its key features and functionality." required rows={8} maxLength={200} hasError={errors["pluginDescription"]?.message ? true : false} errorMessage={errors["pluginDescription"]?.message}  {...register("pluginDescription", {required: "This is required", minLength: {value: 20, message: "minimum length is 20"}})} onChange={onChangesOption}/>
                    {generateConfig()}
        
                </div>
            </>
        )
    }


    const onSaveConnector = async (data) => {

        let { formValues } = await getConfigFormData();
        if(providerDetails.category_id == 4 || providerDetails.category_id == 5){
            formValues.document_files = files; 
        }
        saveConnector(connectorId, providerId, data.pluginName, data.pluginDescription, formValues).then(response => {
            toast.success("Successfuly plugin added")
            if (connectorId == undefined) {
                let url = window.location.href.split('/');
                if(providerDetails.category_id == 2 || providerDetails.category_id == 5){
                    window.location.href = url.join("/") + `/${response.data.data.connector.connector_id}/details?activeTab=database-table`
                }else{
                    window.location.href = url.join("/") + `/${response.data.data.connector.connector_id}/details?activeTab=documentation`
                }
            } else {
                if(providerDetails.category_id == 2 || providerDetails.category_id == 5){
                    setCurrentActiveTab("database-table")
                }else{
                    setCurrentActiveTab("documentation")
                }
            }
        }).catch(e => {
            toast.error("Plugin saving failed")
        }
        )
    }

     
     const onTestConnection = async ()=>{
        let {formValues, formFilled} = await getConfigFormData()
        if(formFilled){
            if(providerDetails.category_id == 4 || providerDetails.category_id == 5){
                formValues.document_files = files; 
            }
            healthCheck(providerId, { provider_config: formValues, connector_name: getValues("pluginName") }).then(response=>{
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
        let fullFill = false
        Object.keys(localTableDetails).map(table_id=>{
            let tempCols = [];
            Object.keys(localTableDetails[table_id].columns).map(col_id=>{
                tempCols.push({
                    column_id: col_id,
                    column_name: localTableDetails[table_id].columns[col_id].column_name,
                    description: localTableDetails[table_id].columns[col_id].description
                })
            })


            if(localTableDetails[table_id].description.trim() !== ""){
                fullFill = true
            }

            tempTableDetails.push({
                table_id: table_id,
                table_name: localTableDetails[table_id].table_name,
                description: localTableDetails[table_id].description,
                columns: tempCols
            })
        })

       

        if(fullFill == false){
            toast.error("Table description is a required field. Please provide a valid description.")
            return
        }

        updateSchema(connectorId, tempTableDetails).then(response=>{
            toast.success("Data saved successfully.")
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
                                {disableConnectorSave && <Button style={{marginRight: "10px",display: providerDetails.category_id == 4 ? "none" : ""}} className="icon-button" disabled={Object.keys(errors).length > 0 ? true : false} onClick={onTestConnection}>  Connection Test <RiPlugLine/></Button>}
                                    <Button buttonType="submit" className="icon-button" disabled={disableConnectorSave} >  Save & Continue <FaRegArrowAltCircleRight/></Button>
                                </div>
                            </div>
                        </form>
                    </Tab>
                   
                     <Tab title="Database Schema" tabKey="database-table" key={"database-table"} disabled={connectorId ? false : true} hide={![2,5].includes(providerDetails.category_id)}>
                        <TitleDescription title="Schema Details" description="Here are the tables and their columns for the plugin. Please describe the tables and it's column details to improve understanding of the plugin schema structure." />
                        <div style={{marginBottom: "30px"}}>
                            <Table data={providerSchema} ></Table>
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