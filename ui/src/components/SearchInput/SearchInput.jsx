
import style from "./SearchInput.module.css"

const SearchInput = ({
    label="",
    placeholder = "Search",
    defaultValue = "",
    className = "",
    onChange = ()=>{},
    ...props
})=>{

    return(
        <>
            {label !== "" && <lable className={style.InputLabel}>{label}</lable> }
            <input type="text" placeholder={placeholder} className={style.Input} onChange={onChange} {...props} />
        </>
    )
}

export default SearchInput