import style from './ChatBox.module.css'

function ChatHistoryButton({icon,text, onClick = ()=>{}}) {
  return (
    <div style={{position:"absolute",right:"0",top:"50%",bottom:"50%"}} onClick={onClick} className={style.ButtonContainer}>
       <div className={style.ChatHistoryIcon}><img src={icon}/></div>
       <div className={style.ChatHistoryText}>{text}</div>
    </div>
  )
}

export default ChatHistoryButton