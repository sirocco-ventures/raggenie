
import { Children, useEffect, useState } from "react"
import style from "./Tab.module.css"

const renderTab = (title, key, isActive, onTabClick, disabled = false, hide = false) => {
    return (
        <>
           {hide == false && <div key={key} className={`${style.TabButton} ${disabled == true ? style.TabButtonDisabled : ""} ${isActive == true ? style.TabButtonActive : ''}`} onClick={() => disabled == false ? onTabClick(key): ()=>{}} >{title}</div> }
        </>
    )
}

const Tabs = ({ activeTab, children }) => {
    const [activetab, setActivetab] = useState(activeTab)
    let content = ""

    const onTabClick = (key) => setActivetab(key)

    useEffect(() => {
        setActivetab(activeTab)
    }, [activeTab]);

    return (
        <>
            <div className={style.Tabs}>
                {Children.map(children, (child) => {
                   
                    if(child){
                        if (activetab == child.props.tabKey){content = child.props.children}
                        return renderTab(child.props.title, child.props.tabKey, activetab == child.props.tabKey, onTabClick, child.props.disabled ?? false, child.props.hide ?? false)
                    }
                })}
            </div>
            <div className={style.TabBody}>
                {
                   Children.map(children, (child, index)=>{
                        return (<>
                              {child && <div key={index} className={`${style.TabPanel} ${child.props.tabKey == activetab ? style.TabPanelActive : ""}`}>
                                {child}
                                </div>}
                            </>
                        )
                   }) 
                }
            </div>
        </>
    )

}

export default Tabs