import ChatBox from "src/components/ChatBox/ChatBox"
import {  useEffect, useRef, useState } from "react"
import GetService from "src/utils/http/GetService"
import { API_URL } from "src/config/const"
import PostService from "src/utils/http/PostService"
import { v4 as uuidv4 } from 'uuid';
import { useNavigate, useParams } from "react-router-dom"
import EmptyPreview from "./EmptyPreview"
import { getConnectors } from "src/services/Connectors"
import { getBotConfiguration, restartBot } from "src/services/BotConfifuration"
import { toast } from "react-toastify"
import { isEmptyJSON } from "src/utils/utils"


const PreviewChatBox = ({urlPrex = "/preview"})=>{ 

    const [feedbackStatus, setFeedbackStatus] = useState(false); // for dislike and like activation
    const [currentConfigID, setCurrentConfigID] = useState(0)
    const [conversations, setConversation] = useState([])
    const [chatHistory,setchatHistory] = useState([])
    const [currentChat, setCurrentChat] = useState({})
    const [isChatLoading, setIsChatLoading] = useState(false) 
    const [enableChatbox, setEnableChatbox] = useState(false)
    const [currentState, setCurrentState] = useState(1)
    // currentState Values
    // 1. to add plungs
    // 2. setup bot configuration
    // 3. restart bot


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
                    { "content": message, "role":"user" }, {showLoader: false,allowAuthHeaders:true}, axiosConfig).then(response=>{
                       
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
        GetService(API_URL + `/chat/get/${contextId}`,{},{allowAuthHeaders:false}).then(response=>{
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
        GetService(API_URL + "/chat/list/context/all",{},{allowAuthHeaders:false}).then(response => {  
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
            chatHistory = chatHistory.reverse()      
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
                    setCurrentState(1)
                }
            })
    }

    const getConfig = ()=>{
        getBotConfiguration().then(response=>{
            let configs = response.data?.data?.configurations
            if(configs?.length > 0){
                setCurrentConfigID(configs[0].id)
                if(configs[0].inference[0]?.id){
                    if(configs[0].status == 1){
                        setCurrentState(3)
                    }else{
                        setEnableChatbox(true)
                    }
                }else {
                    setCurrentState(2)
                }
            }else{
                setCurrentState(2)
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

    const restartChatBot = ()=>{
        restartBot(currentConfigID).then(()=>{
            toast.success("Chatbot Restarted")
            setEnableChatbox(true)
        }).catch(()=>{
            toast.error("Failed to restart bot")
        })
    }


    
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
            {enableChatbox ? <ChatBox messageBoxRef={messageBoxRef} handleNavigateChatContext={handleNavigateChatContext} onCreateNewChat={onCreateNewChat} chatHistory={chatHistory} isLoading={isChatLoading} conversations={conversations} onKeyDown={onChatBoyKeyDown} onSendClick={onSendClick}  /> :<EmptyPreview currentState={currentState} onRestartBot={restartChatBot} />} 
            
        </>
    )
}

export default PreviewChatBox