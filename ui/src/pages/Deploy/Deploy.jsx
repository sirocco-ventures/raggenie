import { useEffect, useState } from 'react';
import RouteTab from 'src/components/RouteTab/RouteTab';
import TitleDescription from 'src/components/TitleDescription/TitleDescription';
import TitleDescriptionContainer from 'src/components/TitleDescription/TitleDescriptionContainer';
import Button from 'src/components/Button/Button';
import style from "./Deploy.module.css"
import { deployTabroutes } from './deployTabRoutes';
import { RiRestartLine } from 'react-icons/ri';
import { API_URL } from 'src/config/const';
import PostService from 'src/utils/http/PostService';
import { toast } from 'react-toastify';


const Deploy = ({currentConfigID}) => {

  const generateYMAL = ()=>{
    PostService(API_URL + `/connector/createyaml/${currentConfigID}`,{},{loaderText: "Restarting Chatbot"}).then(()=>{
        toast.success("Chatbot Restarted")
    }).catch(()=>{
        toast.error("Failed to restart bot")
    })
  }

  return (
    <div>
      <div className={style.DeployURLContainer}>
      <TitleDescriptionContainer>
          <TitleDescription orderNumber={1} title='Restart your Chatbot' description='Deploy your chatbot to experience real-time updates based on your configuration changes.' />
        </TitleDescriptionContainer>
      <div className={`${style.DeployPageButton}`}>
        <Button onClick={generateYMAL} > 
          Restart Chatbot  <RiRestartLine/>
        </Button>

      </div>
        <TitleDescriptionContainer>
          <TitleDescription orderNumber={2} title='Deployment details' description='Get the URL to preview your chatbot live and the embed code to integrate it into your website or app.' />
        </TitleDescriptionContainer>
        <div>

        </div>
        
        <div style={{padding: "0px 30px"}}>
          <RouteTab Deployroutes={deployTabroutes(currentConfigID)}/>
        </div>
      </div>
    </div>
  );
};

export default Deploy;
