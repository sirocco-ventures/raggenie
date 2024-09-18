import React from 'react'
import style from "./ChatBox.module.css"



function Time({message={}, time= "", onLike = ()=>{}, onDisLike = ()=>{}, summaryOpen = false, onSummaryClick = ()=>{}}) {
  return (
      <>
          <div className={style.MessageExtraInfo}>
              <div className={style.Timecontainer}>
                  {/* <div className={style.Timelabel}>
                      {time}
                  </div>
                  <div className={style.LikeIcon}>
                        <div className={`${message.feedback_status == 1 ? `${style.LikeButton} ${style.Activeliked}` : style.LikeButton}`} onClick={(e)=>onLike(e)}></div>
                        <div className={`${message.feedback_status == 0 ? `${style.DislikeButton} ${style.ActiveDisliked}` : style.DislikeButton}`} onClick={(e)=>{onDisLike(e)}}></div>
                  </div> */}
              </div>
              <div>
                
                 { message.data?.query && <div className={style.SummaryMenuContainer} onClick={onSummaryClick}>
                        <div><span className={style.Summarylabel}>Chat Summary </span></div>
                        <div className={`${style.SummaryImgContainer} ${summaryOpen ? style.SummaryOpenImgContainer : style.SummaryCloseImgContainer}`}> 
                            <img src={"./assets/summary-down.svg"} className={summaryOpen ? style.SummaryOpen : style.SummaryClose } />  
                        </div>
                    </div>
                  }
              </div>
          </div>
      </>
  )
}

export default Time