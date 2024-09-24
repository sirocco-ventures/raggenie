import { useState } from 'react';
import style from './RouteTab.module.css';

export default function RouteTab({className, TabName="", Deployroutes, TabStyle, ContainerStyle, ...props }) {
    // State to track the active tab
    const [activeTab, setActiveTab] = useState(Deployroutes[0].path);
    return (
        <>
            <nav>
                <div className={`${style.TabNavBar} ${className}`} style={ContainerStyle}{...props}>
                    {Deployroutes.map((item, index) => (
                        <div style={TabStyle}
                            key={index}
                            className={`${style.TabNavBarLinkActive} ${activeTab === item.path ? style.active : ''} ${item.disabled? style.TabDisable : ""}`}
                            onClick={() => item.disabled ? ()=>{} : setActiveTab(item.path)}
                        >
                            {item.title}
                        </div>
                    ))}
                </div>
            </nav>
            <div className={`${style.TabContent}`}>
                {Deployroutes.map((item, index) => (
                    activeTab === item.path && (
                        <div key={index}>
                            {item.page}
                        </div>
                    )
                ))}
            </div>
        </>
    );
}
