import { forwardRef, useEffect, useRef } from "react"
import style from "./ChatBox.module.css"
import Message from "./Message"

import Loader from "./Loader"

import ChatHistorySideBar from "./ChatHistorySideBar"


const ChatBox = forwardRef(({messageBoxRef = null, handleNavigateChatContext=()=>{}, onCreateNewChat=()=>{}, chatHistory=[], isLoading = false, onFeedBackSubmit=()=>{}, conversations = [], onKeyDown = ()=>{}, onKeyUp = ()=>{}, onSendClick = ()=>{}, onLike = ()=>{} , onDisLike = ()=>{} }, ref)=>{

    const chatListRef = useRef(null)
   
    const handleOnLikeClick = (e, feedbackStatus, feedbackMessage, message)=>{
        onLike(e, feedbackStatus, feedbackMessage, message)
    } 

    const handleOnDisLikeClick = (e,message)=>{
        onDisLike(message)
    }


    const toggleContainer = (e, setIsHidden) => {
        setIsHidden(prev => !prev); 
      };

    useEffect(()=>{
        document.querySelector("#messageBody").scrollIntoView({ behavior: "smooth", block: "end", inline: "nearest" });
    },[conversations])

    return(
        <>  
            <div className={style.ChatBoxContainer}>
                <div className={style.ChatMessagesContainer}>
                    <div className={style.ChatMessageContainer}>
                        <div id="messageBody" ref={chatListRef} className={style.chatList}>
                            {
                                conversations.map((message, index) => {
                                    return <Message onLike={handleOnLikeClick} onDisLike={handleOnDisLikeClick} onFeedbackSubmit={onFeedBackSubmit} key={index} message={message} />

                                })
                            }
                            {isLoading && <Loader />}
                        </div>
                    </div>

                    <div>
                        <div className={style.ChatBoxTextContainer}>
                            <div ref={messageBoxRef} className={style.ChatBoxTextBox} contentEditable="plaintext-only" onKeyDown={onKeyDown} onKeyUp={onKeyUp}>
                            </div>
                            <div>
                                <div className={style.ChatBoxSendIcon} onClick={onSendClick}></div>
                            </div>
                        </div>
                        <div>
                            <p className={style.ChatBottomMessage}>RAG Builder may display inaccurate info, including about people, so double-check its responses.</p>
                        </div>
                    </div>
                </div>
                <ChatHistorySideBar handleNavigateChatContext={handleNavigateChatContext} onCreateNewChat={onCreateNewChat} chatHistory={chatHistory} onClick={(e, setIsHidden) => toggleContainer(e, setIsHidden)}/>     
          </div>
        </>
    )
})

export default ChatBox