import { useState } from 'react'
import close from './assets/close-modal-icon.svg'
import style from './ChatBox.module.css'

function Feedback({ onSubmit=()=>{}, message={}, onFeedBackClose = ()=>{}}) {

  const [inputValue,setInputValue] = useState()
  const feedBackPredefinedComment = ["Incorrect", "Confusing", "Incomplete", "Unclear"]
  
  const handleSuggestClick = (e, item) => {
    setInputValue(item)
  }


  return (
    <>
        <div className={`${style.FeedbackCommet}`} >
          <div className={style.TitleHead}>
            <h2>Why did you choose this rating?</h2>
            <button className={`${style.CloseIconBtn}`} onClick={onFeedBackClose}>
              <img src={close} alt='closemodal' width={23} height={23} className={style.ImageBGRemove} />
            </button>
          </div>
          <div className={style.SuggestedComment}>
            {feedBackPredefinedComment.map((item) => <span onClick={(e) => { handleSuggestClick(e, item) }}>{item}</span>)}
          </div>
          <textarea value={inputValue} onChange={e => setInputValue(e.target.value)} className={style.FeedbackTextarea} cols="30" rows="5" wrap="on" />
          <div>
            <button className={style.FeedbackButton} onClick={(e) => onSubmit(e, false, inputValue, message)}>Submit</button>
          </div>
        </div>
    </>
  )
}

export default Feedback