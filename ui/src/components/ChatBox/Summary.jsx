
import close from './assets/close-modal-icon.svg'
import style from './ChatBox.module.css'

function Summary({ onSummaryClose=()=>{}, message={}}) {
  return (
    <>
        <div className={`${style.SummaryContainer}`} >
          <div className={style.SummartyHeading}>
            <h2 className={style.SummaryTitle}>Chat Summary</h2>
            <button className={`${style.SummaryCloseButton}`} onClick={onSummaryClose}>
              <img src={close} alt='closemodal' width={23} height={23} className={style.ImageBGRemove} />
            </button>
          </div>
          
          <div>
              <div className={style.ChatSummay}>
                  <p className={style.ChatSQLQuery}>{message.data.query}</p>
                  <p className={style.ChatDataSummary}>showing {message?.data?.chart?.data?.length > 12 ? 12 : message?.data?.chart?.data?.length } out of {message.data?.chart?.data?.length} items retreived</p>
              </div>
          </div>
        </div>
    </>
  )
}



export default Summary