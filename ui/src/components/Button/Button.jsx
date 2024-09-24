import style from "./Button.module.css"

const Button = ({
        children, 
        buttonType="button",
        type = "solid",
        variant = "primary", 
        className = "",
        ...props
    })=>{


    return(
        <button type={buttonType} className={`${style.Button} ${style[`${type}-${variant}`]} ${className}`} {...props}>{children}</button>
    )
}

const BUTTON_TYPE = {
    SOLID: "solid",
    TRANSPARENT: "transparent"
}


const BUTTON_VARIANT = {
    PRIMARY: "primary",
    WARNING: "warning",
    DANGER: "danger",

    PRIMARY_SECONDARY: "primary-secondary",
    DANGER_SECONDARY: "danger-secondary",
}


export default Button
export { BUTTON_TYPE, BUTTON_VARIANT}