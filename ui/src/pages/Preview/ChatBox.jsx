import ChatBox from "src/components/ChatBox/ChatBox"
import {  useEffect, useRef, useState } from "react"
import GetService from "src/utils/http/GetService"
import { API_URL } from "src/config/const"
import PostService from "src/utils/http/PostService"
import { v4 as uuidv4 } from 'uuid';
import { useNavigate, useParams } from "react-router-dom"
import EmptyPreview from "./EmptyPreview"
import { getConnectors } from "src/services/Connectors"
import { getBotConfiguration } from "src/services/BotConfifuration"
import { isEmptyJSON } from "src/utils/utils"


const PreviewChatBox = ({urlPrex = "/preview"})=>{ 

    const [feedbackStatus, setFeedbackStatus] = useState(false); // for dislike and like activation

    const [conversations, setConversation] = useState([])
    const [chatHistory,setchatHistory] = useState([])
    const [currentChat, setCurrentChat] = useState({})
    const [isChatLoading, setIsChatLoading] = useState(false) 
    // const [contextId, setContextId] = useState("")
    const [enableChatbox, setEnableChatbox] = useState(false)
    const [currentState, setCurrentState] = useState(0)
    const [messageBoxText, setMessageBox] = useState(`You don't have any sources added, to get started go \r\n to plugin section and add a source`)
    const [emptyURL, setEmptyURL] = useState("/plugins/sources")
    const [messageBoxButtonText, setMessageBoxButtonText] = useState("Add Plugin")

    let { contextId } = useParams()
    const navigate = useNavigate()
    const messageBoxRef = useRef(null)


    const chatQuery = (message)=>{

        setCurrentChat({isBot: false, message: message})
        
            let axiosConfig = {
                headers: {
                    "x-llm-context-id": contextId
                }
            }
            setIsChatLoading(true)
            PostService(API_URL + "/query/query",
                    { "content": message, "role":"user" }, {showLoader: false}, axiosConfig).then(response=>{
                       
                let res = response.data
                let chatMessage =  res.response.content
                let chatError = isEmptyJSON(res.response.error) ? "" : res.response.error
                let chatEntity =  res.response.main_entity
                let chatFormat = res.response.main_format
                let chatKind = res.response.kind
                let chatData =  { 
                        chart: {
                            data: res.response.data,
                            title: res.response.title,
                            xAxis: res.response.x,
                            yAxis: res.response.y
                        },
                        query: res.response.query
                    }
                
              
                setCurrentChat({isBot: true, message: chatMessage, entity: chatEntity, error: chatError, format: chatFormat, kind: chatKind, data: chatData })
                setIsChatLoading(false)
                getChatHistory()
                
            }).catch((err)=>{
                setIsChatLoading(false)
                setCurrentChat({isBot: true, message: "Oops somethings went wrong, try again", error: err.message, format: "general_message", kind: "none", data: [] })
            })
    }

    const onChatBoyKeyDown = (e)=>{

        if(e.keyCode  == 13){
            e.preventDefault()
            let message = e.target.innerText;
            if(message != ""){
                chatQuery(message)
                e.target.innerText = ""
            }
        }
    }
    
    const onSendClick = ()=>{
        let message = messageBoxRef.current.innerText;
        if(message != ""){
            chatQuery(message)
            messageBoxRef.current.innerText = ""
        }
    }

    const getChatByContexts =(contextId)=>{
        GetService(API_URL + `/chat/get/${contextId}`,{},{allowHeaders:false}).then(response=>{
            const chats = response.data.data.chats
            let tempChat = [];
            let tempChatDetails = [];

            chats?.map(chat =>{ 

                let chatData =  { 
                    chart: {
                        data: chat.chat_answer.data,
                        title: chat.chat_answer.title,
                        xAxis: chat.chat_answer.x,
                        yAxis: chat.chat_answer.y
                    },
                    query: chat.chat_answer.query
                }

               
                tempChat.push({isBot: false, message: chat.chat_query, chat_context_id: chat.chat_context_id, chat_id: chat.chat_id, feedback_status: 0, })
                tempChat.push({isBot: true, message: chat.chat_answer.content, error:  isEmptyJSON(chat.chat_answer.error) ? "" : chat.chat_answer.error, entity: chat.chat_answer.main_entity, format: chat.chat_answer.main_format, kind: chat.chat_answer.kind, data: chatData })
            })
            setConversation(tempChat)
        })
    }

// ===================CHAT HISTROY START==============================
    const getChatHistory = () => {
        GetService(API_URL + "/chat/list/context/all",{},{allowHeaders:false}).then(response => {  
            let chatHistory = []; 
            let chats = response.data.data.chats;
    
            chats?.map((item) => {
                chatHistory.push({
                    chatId: item.chat_id,
                    chatContextId: item.chat_context_id,
                    chatQuery: item.chat_query,
                    chatSummary: item.chat_summary,
                    date: new Date(item.created_at), // Convert date string to Date object
                });
            });           
            setchatHistory(chatHistory);
        })
    }

    function generateContextUUID() {
        return uuidv4();
    }

    const onCreateNewChat=()=>{
        navigate(`${urlPrex}/${generateContextUUID()}/chat`)
      }

    const handleNavigateChatContext=(e, contextId)=>{
        navigate(`${urlPrex}/${contextId}/chat`)    
    }

// ===================CHAT HISTROY END==============================

    const getPluginList = ()=>{  
            getConnectors().then(response=>{
                if (response.data.data.connectors?.length > 0){
                    getConfig()
                }else{
                    setCurrentState(false)
                }
            })
    }

    const getConfig = ()=>{
        getBotConfiguration().then(response=>{
            let configs = response.data?.data?.configurations
            if(configs?.length > 0){
                setEnableChatbox(true)
                if(configs[0].inference[0]?.id){
                    setEnableChatbox(true)
                }else {
                    setEnableChatbox(false)
                    setEmptyURL("/bot-configuration")
                    setMessageBoxButtonText("Add Inference")
                    setMessageBox("Please configure the inference endpoint details in the bot configuration to proceed.")
                }
            }else{
                setEnableChatbox(false)
                setEmptyURL("/bot-configuration")
                setMessageBoxButtonText("Add Configuration")
                setMessageBox("You need to configure chat box")
            }
        })
    }


    const onFeedback = (e, feedbackStatus, feedbackMessage = "", message) => {

        PostService(API_URL + `/chat/feedback`, {
            chat_context_id: message.chat_context_id,
            chat_id: message.chat_id,
            feedback_status: feedbackStatus === true ? 1 : 0, 
            feedback_json: { reason: feedbackMessage }
        })
        .then(response => {
            setFeedbackStatus(response.data.feedback_status === 1 ? true : false );
        })
    };
    
    useEffect(()=>{
        if(currentChat.message){
            let tempConversation = JSON.parse(JSON.stringify(conversations))
            tempConversation.push(currentChat)
            setConversation(tempConversation)
        }
    },[currentChat])

    useEffect(()=>{
        getChatByContexts(contextId)
    }, [contextId])


    useEffect(()=>{
        getChatHistory()
        getPluginList();
        if(contextId == undefined){
            onCreateNewChat()
        }
     },[])
 

    return(
        <>
            {enableChatbox ? <ChatBox messageBoxRef={messageBoxRef} handleNavigateChatContext={handleNavigateChatContext} onCreateNewChat={onCreateNewChat} chatHistory={chatHistory} isLoading={isChatLoading} conversations={conversations} onKeyDown={onChatBoyKeyDown} onSendClick={onSendClick}  /> : <EmptyPreview message={messageBoxText} url={emptyURL} buttonText={messageBoxButtonText} />} 
        </>
    )
}

export default PreviewChatBox