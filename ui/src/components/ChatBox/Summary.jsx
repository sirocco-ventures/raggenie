
import { useState } from 'react'
import queryOpenImg from "./assets/query-open.svg"
import queryCloseImg from "./assets/query-close.svg"
import style from './ChatBox.module.css'

function Summary({message={}}) {
  const [summaryOpen, setSummaryOpen] = useState(false);
  const [queryOpen, setQueryOpen] = useState(false);

  return (
    <>
        <div className={`${style.SummaryContainer} ${summaryOpen ? style.SummaryContainerOpen: ""}`} >
          <div className={style.SummartyHeader} onClick={()=>setSummaryOpen(!summaryOpen)}>
            <button className={` ${style.SummaryToggleButton}`} onClick={()=>setSummaryOpen(!summaryOpen)}>
              <img src={""} alt='closemodal' width={18} height={18} className={`${summaryOpen ? style.SummaryToggleIconClose: style.SummaryToggleIconOpen}`} />
            </button>
            <div>
              <h2 className={style.SummaryHeaderTitle}>Summary</h2>
            </div>
          </div>
          
          <div>
              <div className={style.ChatSummayContainer}>
                  <div>
                     
                        <p className={style.ChatSQLSummary}>
                          { message?.data?.chart?.data?.length > 0 && <>
                            Showing {message?.data?.chart?.data?.length > 12 ? 12 : message?.data?.chart?.data?.length } out of {message.data?.chart?.data?.length} items retreived
                          </> }
                          { message?.data?.chart?.data?.length == 0 && <>
                            There are no entries to show at the moment.
                          </> }
                        </p>
                     
                     
                  </div>
                  <div onClick={()=>setQueryOpen(!queryOpen)}>
                      <div className={style.QueryTitle}>
                          <div className={style.QueryInnerTitle}>
                            <img src={queryOpen ? queryOpenImg : queryCloseImg}/>
                            Query
                            <img src={queryOpen ? queryOpenImg : queryCloseImg}/>
                          </div>
                      </div>
                      <div className={queryOpen ? style.SQLQueryOpen : style.SQLQueryClose}>
                          <p className={style.ChatSQLSummary}>{message.data.query}</p>
                      </div>
                  </div>
              </div>
              {/* <div>

                 
                  <p className={style.ChatDataSummary}>showing {message?.data?.chart?.data?.length > 12 ? 12 : message?.data?.chart?.data?.length } out of {message.data?.chart?.data?.length} items retreived</p>
              </div> */}
          </div>
        </div>
    </>
  )
}



export default Summary