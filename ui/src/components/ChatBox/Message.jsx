
import style from "./ChatBox.module.css"
import botIcon from "./assets/bot-icon.svg"
import Time from "./Time"
import { useState } from "react"
import Feedback from "./Feedback"
import Table from "../Chart/Table/Table"
import BarChart from "../Chart/BarChart/BarChart"
import PieChart from "../Chart/PieChart/PieChart"
import LineChart from "../Chart/LineChart/LineChart"
import AreaChart from "../Chart/AreaChart/AreaChart"
import Summary from "./Summary"
const Message = ({
    message = {},
    onLike = ()=>{}, 
    onDisLike = ()=>{},
    onFeedbackSubmit = ()=>{},
    })=>{

    const [showFeedback, setShowFeedback] = useState(false)
    const [showChatSummary, setShowChatSummary] = useState(false)


    const handleOnLikeClick = (e)=>{
        onLike(e, true, "", message)
    }

    const handleOnDislikeClick = (e)=>{
        setShowFeedback(true)
        onDisLike(e)
    }

    const handleOnFeedbackClose = ()=>{
        setShowFeedback(false)
    }

    const handleOnSummaryOpen = ()=> {
        setShowChatSummary(true)
    }

    const handleOnSummaryClose = ()=>{
        setShowChatSummary(false)
    }


    return(
        <>
            <div className={style.Message}>
                <div className={message.isBot == false ? style.UserMessageContainer : style.BotMessageContainer}>
                    {message.isBot && <div> <img src={botIcon} className={style.MessageAvatar} /></div>}
                    <div>
                        <div className={`${style.MessageContainer}  ${message.isBot == false ? style.UserMessage : style.BotMessage}`}>{message.message}
                        {message.isBot == true &&  <Time onLike={handleOnLikeClick} onDisLike={handleOnDislikeClick} onSummaryClick={handleOnSummaryOpen} summaryOpen ={showChatSummary}  time={"Today 12:30pm"} message={message}/>}
                        </div>
                    </div>
                </div>
            </div>
            <div style={{marginLeft: "52px", marginBottom: "40px"}}>
                 {/* {showFeedback && message.isBot && <Feedback onSubmit={onFeedbackSubmit} onFeedBackClose={handleOnFeedbackClose} message={message} /> } */}
                 {/* {showChatSummary && message.isBot && <Summary onSummaryClose={handleOnSummaryClose} message={message} /> } */}
                 
                 
                 { (message.kind == "list" || message.kind == "table" || message.kind == "single" || message.kind == "none") && <Table data={message.data.chart.data} />}
                 { message.kind == "bar_chart" && <BarChart title={message.data.chart.title} data={message.data.chart.data} xAxis={message.data.chart.xAxis[0]} yAxis={message.data.chart.yAxis[0]}  /> }
                 { message.kind == "pie_chart" && <PieChart title={message.data.chart.title} data={message.data.chart.data} labelKey={message.data.chart.xAxis[0]} dataKey={message.data.chart.yAxis[0]}  /> }
                 { message.kind == "line_chart" && <LineChart title={message.data.chart.title} data={message.data.chart.data} xAxis={message.data.chart.xAxis[0]} yAxis={message.data.chart.yAxis[0]}  /> }
                 { message.kind == "area_chart" && <AreaChart title={message.data.chart.title} data={message.data.chart.data} xAxis={message.data.chart.xAxis[0]} yAxis={message.data.chart.yAxis[0]}  /> }
                 
            </div>
            
        </>
    )
}

export default Message