import { useEffect, useState } from "react"
import panelExpandIcon from "./assets/chevron-up.svg"
import panelCollapseIcon from "./assets/chevron-down.svg"
import style from "./Panel.module.css"



const Panel = ({title = "Panel", children, isExpanded = false, expandable = false, onExpandCollapse = ()=>{}, ...props})=>{

    const [expand, setExpand] = useState(false)

    const onExpandClick = ()=>{
        setExpand(!expand)
        onExpandCollapse(!expand)
    }

    useEffect(()=>{
        setExpand(isExpanded)
    }, [isExpanded])

    return(
        <div className={`${style.PanelContainer} ${expand == true ? "" : style.PanelContainerCollapse}`} {...props}>
            <div className={style.PanelHeader}>
                {expandable && <div onClick={onExpandClick} style={{cursor: "pointer"}}> {expand == true ? <img src={panelExpandIcon}/> : <img src={panelCollapseIcon}/>  } </div> }
                <div className={style.PanelTitle}>
                    {title}
                </div>
            </div>
            <div className={style.PanelBody}>
               {children}
            </div>
        </div>  
    )
}


export default Panel