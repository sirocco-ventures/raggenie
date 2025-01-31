import { useEffect, useState } from 'react';
import RouteTab from 'src/components/RouteTab/RouteTab';
import DashboardBody from 'src/layouts/dashboard/DashboadBody';
import TitleDescription from 'src/components/TitleDescription/TitleDescription';
import TitleDescriptionContainer from 'src/components/TitleDescription/TitleDescriptionContainer';
import Button from 'src/components/Button/Button';
import style from "./Deploy.module.css"
import rightArraow from "src/assets/icons/arrow-right-icon.svg"
import { deployTabroutes } from './deployTabRoutes';
import { RiRestartLine } from 'react-icons/ri';
import { Link } from 'react-router-dom';
import GetService from 'src/utils/http/GetService';
import { API_URL } from 'src/config/const';
import PostService from 'src/utils/http/PostService';
import { toast } from 'react-toastify';
import { useNavigate } from 'react-router-dom';


const Deploy = () => {

  const navigate = useNavigate()
  const [currentConfigID, setCurrentConfigID] = useState(undefined)
  const [disabledGenerateYAMLButton, setDisabledGenerateYAMLButton] = useState(true)


  const onPageLoad = ()=>{
        
      GetService(API_URL + "/connector/configuration/list").then(response=>{
          let configs = response.data?.data?.configurations
          if(configs?.length > 0){
              setCurrentConfigID(configs[0].id)
          
              if(configs[0].inference[0]?.id){
                  setDisabledGenerateYAMLButton(false)
              }else{
                  setDisabledGenerateYAMLButton(true)
              }
          }else{
              setDisabledGenerateYAMLButton(true)
          }
      }).catch(() => {
        navigate('/error')
    })
    }

  const generateYMAL = ()=>{
    PostService(API_URL + `/connector/createyaml/${currentConfigID}`,{},{loaderText: "Restarting Chatbot"}).then(()=>{
        toast.success("Chatbot Restarted")
    }).catch(()=>{
        toast.error("Failed to restart bot")
    })
  }

  useEffect(()=>{
    onPageLoad()
  }, [])


  return (
    <div>
      <DashboardBody title="Deploy URL">
      <div className={style.DeployURLContainer}>
      <TitleDescriptionContainer>
          <TitleDescription orderNumber={1} title='Restart your Chatbot' description='Deploy your chatbot to experience real-time updates based on your configuration changes.' />
        </TitleDescriptionContainer>
      <div className={`${style.DeployPageButton}`}>
        <Link to={"/bot-configuration"}>
          <Button type="soild" className={`${style.LightButton}`}> Go to Bot Configuration<img src={rightArraow} alt="right-arrow"/></Button>
        </Link>
        <Button onClick={generateYMAL} disabled={disabledGenerateYAMLButton} > 
          Restart Chatbot  <RiRestartLine/>
        </Button>

      </div>
        <TitleDescriptionContainer>
          <TitleDescription orderNumber={2} title='Deployment details' description='Get the URL to preview your chatbot live and the embed code to integrate it into your website or app.' />
        </TitleDescriptionContainer>
        <div>

        </div>
        
        <div style={{padding: "0px 30px"}}>
          <RouteTab Deployroutes={deployTabroutes} />
        </div>
      </div>
      </DashboardBody>
    </div>
  );
};

export default Deploy;
