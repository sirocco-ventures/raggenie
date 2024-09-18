
import style from "./Tag.module.css"

const Tag = ({type = "primary", children, ...props})=>{


    return(
        <span className={`${style.Tag} ${style[`Tag-${type}`]}`} {...props}>{children}</span>
    )
}

export default Tag

