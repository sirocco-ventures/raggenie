import { useState, useEffect } from 'react'
import arrowImage from './assets/arrow.svg'
import logoImage from './assets/logo.svg'
import largeLogo from './assets/largelogo.svg'
import sendImage from './assets/send.png'
import botdpImage from './assets/bot-dp.svg'
import chatBotAPI from './ChatBotAPI'
import { useParams } from "react-router-dom"
import { isEmptyJSON } from "src/utils/utils"
import Message from 'src/components/ChatBox/Message'
import Loader from '../components/ChatBox/Loader'
import './ChatBot.css'


function ChatBot({ apiURL, uiSize }) {
  if (!apiURL) return console.error("apiURL is undefined")
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  let { contextId } = useParams()

  const toggleChatbox = () => {
    setIsOpen(!isOpen);
  }

  const simulate = (message) => {
    setMessages((prevMessages) => [
      ...prevMessages,
      { sender: 'user', message: message },
    ]);

    setLoading(true);

    chatBotAPI(message, contextId, apiURL)
      .then(response => {
        const res = response.data;
        const chatMessage = res.response.content;
        let chatError = isEmptyJSON(res.response.error) ? "" : res.response.error
        let chatEntity = res.response.main_entity
        let chatFormat = res.response.main_format
        let chatKind = res.response.kind
        let chatData = {
          chart: {
            data: res.response.data,
            title: res.response.title,
            xAxis: res.response.x,
            yAxis: res.response.y
          },
          query: res.response.query
        }


        // console.log({isBot: true, message: chatMessage, entity: chatEntity, error: chatError, format: chatFormat, kind: chatKind, data: chatData })
        // console.log(message)
        setMessages((prevMessages) => [
          ...prevMessages,
          { sender: 'bot', message: chatMessage, entity: chatEntity, error: chatError, format: chatFormat, kind: chatKind, data: chatData },
        ]);

        setLoading(false);

      })


  }

  const appendMessage = (user, message) => {

  }

  return (
    <div>
      {/* Chatbox Icon */}
      <button className={`float-button large ${isOpen ? 'open' : ''}`} onClick={toggleChatbox}>
        <img src={arrowImage} className='button-icon'></img>
      </button>

      {/* Chatbox Window */}
      {isOpen && (
        <div className={`chat-box ${uiSize === 'large' ? 'large' : ''}`}>
          <div className="chat-header">
            <img src={arrowImage} onClick={toggleChatbox} className='min-btn'></img>
            <img src={uiSize === 'large' ? largeLogo: logoImage}></img>
            <span className='header-text'>Assistant</span>
          </div>

          <div className={`chat-body ${uiSize === 'large' ? 'large' : ''}`}>
            <div className='message-wrapper'>
              {messages.map((message, index) => {
                if (message.sender === 'user') {
                  return (
                    <>
                      <div className='user-message'>{message.message}</div>
                      <div className='bot-message'>{loading && index === messages.length - 1 && <Loader />}</div>
                    </>
                  )
                } else if (message.sender === 'bot') {
                  return (
                    <>
                      <div className='bot-message'>
                        <img src={botdpImage} alt='bot avatar'></img>
                        {/* {message.message} */}
                        <Message message={message} />
                      </div>
                    </>)
                }
              })}
            </div>


          </div>

          <div className={`input-div ${uiSize === 'large' ? 'large' : ''}`}>
            <div
              className="chat-input"
              contentEditable="true"
              placeholder="Type a reply..."
              suppressContentEditableWarning={true}
              onKeyDown={(e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                  e.preventDefault();
                  // console.log(e.target.textContent)
                  const chatInput = e.target.textContent.trim();
                  simulate(chatInput)
                  e.target.textContent = ''; // Clear input
                }
              }}
            >
            </div>
            <button
              className='chat-button'
              onClick={() => {
                const chatInput = document.querySelector('.chat-input').textContent.trim();
                simulate(chatInput);
                document.querySelector('.chat-input').textContent = '';
              }}
            >
              <img src={sendImage}></img>
            </button>
          </div>
        </div>
      )}
    </div>
  )
}

export default ChatBot
