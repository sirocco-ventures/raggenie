import { forwardRef, useEffect, useState } from "react"
import style from "./Input.module.css"



const Input = forwardRef(({
        label = "",
        type = "text",
        value = "",
        placeholder = "Enter here",
        className = "",
        minLength = 0,
        maxLength = Infinity,
        hasError = false,
        errorMessage = "",
        onChange = ()=>{},
        ...props
    }, ref
)=>{

    const [textLength, setTextLength] = useState(0)

    const inputOnChange = (e)=>{
        setTextLength(e.target?.value?.length)
        onChange(e)
    }

    useEffect(()=>{
        setTextLength(value?.length)
    },[value])


    return(
        <>
            <div className={style.InputContainer}>
                {label !== "" && <label className={style.InputLabel}>{label}</label> }
                <input ref={ref} type={type} defaultValue={value} placeholder={placeholder} className={`${style.Input} ${hasError ? style.HasError : ""} ${className}`} onChange={inputOnChange} {...props} />
                { type == "text" && <div className={style.InputHintContainer}>
                    <div className={style.InputHint}>
                            { minLength > 0 && maxLength == Infinity && <span className={style.InputHintMessage}>{`Min characters ${minLength}`}</span> }  
                            { minLength == 0 && maxLength != Infinity &&  <span className={style.InputHintMessage}>{ `Max characters ${maxLength}`}</span> }  
                            { minLength > 0 && maxLength != Infinity && <span className={style.InputHintMessage}>{ `Min characters ${minLength} and Max characters ${maxLength}`}</span> }  
               
                    </div>
                    <div>
                       {(minLength > 0 || maxLength != Infinity) && <span className={style.InputHintMessage}>{textLength}/ { maxLength != Infinity ? maxLength: minLength }</span> }
                    </div>
                </div>}
                {errorMessage !== "" && <span className={style.ErrorMessage}>{errorMessage}</span>}
            </div>

        </>
    )
})

export default Input