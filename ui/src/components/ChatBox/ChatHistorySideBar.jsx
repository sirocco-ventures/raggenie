import { useRef, useState } from 'react'
import style from "./ChatBox.module.css"
import plusIcon from "./assets/plus-image.svg"
import arrowRight from "./assets/arrow-right.svg"
import ChatHistoryButton from "src/components/ChatBox/ChatHistoryButton"
import Clock from "./assets/time-lap.svg"
import ChatDropdownMenu from './ChatDropdownMenu/ChatDropdownMenu'


function ChatHistorySideBar({handleNavigateChatContext=()=>{}, onCreateNewChat=()=>{}, onClick=()=> {}, chatHistory }) {

  const toggleHistoryRef = useRef(null)
  const [isHidden, setIsHidden] = useState(false);

  const showHideSideHistory = (e) => {
    onClick(e, setIsHidden)
  }

  const formatDate = (date) => {
      const options = { year: 'numeric', month: 'long' };
      return new Date(date).toLocaleDateString('en-US', options);
  };


const formattedData = chatHistory.reduce((acc, chat) => {
  
    const { chatContextId, chatQuery, date } = chat;

    // Format the date to "MONTH YEAR"
    const formattedDate = formatDate(date);

    // Initialize the entry if it doesn't exist
    if (!acc[formattedDate]) {
        acc[formattedDate] = {
            title: formattedDate,
            chatQuery: []
        };
    }

    // Add the message to the appropriate date group
    acc[formattedDate].chatQuery.push({
        contextId: chatContextId,
        message: chatQuery
    });

    return acc;
}, {});

const resultArray = Object.values(formattedData);


  return (
    <>
    <div className={isHidden ? `${style.toggleContainer}` : `${style.chatHistoryContainer}`} ref={toggleHistoryRef}>
      <div className={style.ChatBarStyle}>
        <div className={style.ChatNavBar}>
          {isHidden ? <></> : (<div className={style.HistoryArrowButton} onClick={(e) => {showHideSideHistory(e) }}>
            <img src={arrowRight} />
          </div>)}

          <h3>Chat History</h3>
          <button onClick={(e)=>{onCreateNewChat(e)}}>NewChat<span><img src={plusIcon} /></span></button>
        </div>
        <div className={style.ChatHistoryContent}>
          <div className={style.RecentChat}>
            <div className={style.RecentChats}>
            <ChatDropdownMenu handleNavigateChatContext={handleNavigateChatContext} data={resultArray}/>
            </div>
          </div>
        </div>
      </div>
    </div>
      {isHidden ? (<ChatHistoryButton onClick={() => { setIsHidden(!isHidden) }} icon={Clock} text={"History"} />) : null}
    </>

  )
}

export default ChatHistorySideBar