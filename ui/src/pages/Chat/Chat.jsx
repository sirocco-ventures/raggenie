import DashboardBody from "src/layouts/dashboard/DashboadBody"
import style from "./Chat.module.css"
import ChatBox from "src/components/ChatBox/ChatBox"
import {  useEffect, useState } from "react"
import GetService from "src/utils/http/GetService"
import { API_URL } from "src/config/const"
import PostService from "src/utils/http/PostService"
import { v4  as uuid4} from "uuid"


const Chat = ()=>{ 

    const [conversations, setConversation] = useState([])
    const [currentChat, setCurrentChat] = useState({})
    const [isChatLoading, setIsChatLoading] = useState(false) 
    const [contextId, setContextId] = useState("")
    const [enableChatbox, setEnableChatbox] = useState(0)
   
    const onChatBoyKeyDown = (e)=>{
        if(e.keyCode  == 13){
            e.preventDefault()
            let message = e.target.innerText;
            setCurrentChat({isBot: false, message: message})
            e.target.innerText = ""

            let axiosConfig = {
                headers: {
                    "x-llm-context-id": contextId
                }
            }
            setIsChatLoading(true)
            PostService( API_URL +  "/query/query",
                    { "content": message, "role":"user" }, {showLoader: false}, axiosConfig).then(response=>{
                let res = response.data
                let chatFormat = response.format
                let chatKind = res.response.main_format
                let chatData = res.response.data            

                setCurrentChat({isBot: true, message: res.response.content, format: chatFormat, kind: chatKind, data: chatData })
                setIsChatLoading(false)
            }).catch(()=>{
                setIsChatLoading(false)
               
                setCurrentChat({isBot: true, message: "Oops somethings went wrong, try again", format: "general_message", kind: "none", data: [] })
            })
        }
    }

    const getChatContexts =()=>{
        GetService(API_URL + "/chat/all").then(response=>{
            const chats = response.data.chats
            let tempChat = [];
            chats.map(chat =>{ 
                tempChat.push({ isBot: false, message: chat.chat_query })
                tempChat.push({ isBot: true, message: chat.chat_answer.answer })
            })
            setConversation(tempChat)
        })
    }

    useEffect(()=>{
        if(currentChat.message){
            let tempConversation = JSON.parse(JSON.stringify(conversations))
            tempConversation.push(currentChat)
            setConversation(tempConversation)
        }
    },[currentChat])
    

    const hasConfiguruated = ()=>{
        GetService(API_URL + "/connector/configuration/list",{}, {fullLoader: true}).then(response=>{
            let configs = response.data?.configurations
            
            if(configs?.length > 0){
                if(configs[0].status == 2){
                    setEnableChatbox(2)
                }else{
                    setEnableChatbox(1)
                }
            }else{
                setEnableChatbox(1)
            }
        })
    }
    
    useEffect(()=>{
       getChatContexts()
       setContextId(uuid4())
       hasConfiguruated()
    },[])


    return(
        <DashboardBody title="Chat" containerStyle={{padding: "0px 20px", height: "calc(100vh - 68px)"}}>
                {enableChatbox == 1 && (
                    <div className={style.DisableChatBox}>
                        <h2 className={style.MessageStyle}>Please Configure Chatbot</h2>
                    </div>
                )}
                <ChatBox isLoading={isChatLoading} conversations={conversations} onKeyDown={onChatBoyKeyDown}  />
        </DashboardBody>
    )
}

export default Chat