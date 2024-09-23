import {useEffect, useState } from 'react';
import style from './ChatDropdownMenu.module.css';
import arrowDown from '../assets/arrow-down.svg';
import arrowUp from '../assets/arrow-up.svg';

export default function ChatDropdownMenu({ handleNavigateChatContext = () => {}, data = [], showDropdownArrow = true }) {
    const [openDropdown, setOpenDropdown] = useState([]);
    const [showUpto, setShowUpto] = useState(4); // Start with 4 items visible
    const [isExpanded, setIsExpanded] = useState(false); // Track expansion

    const toggleDropdown = (index) => {
        if (index === 0) return; // Prevent toggling for index 0

        setOpenDropdown((prevState) =>
            prevState.includes(index) ? prevState.filter((i) => i !== index) : [...prevState, index]
        );
    };

    useEffect(() => {
        // Open all dropdowns except for index 0 on initial load
        const allIndexes = data.map((_, index) => index).filter((index) => index !== 0);
        setOpenDropdown([0, ...allIndexes]);
    }, [data]);

    if (data.length > 0) {
        data[0].title = 'Recent Chat';
    }

    const toggleVisibility = (index, chatQuery = []) => {
        if (index === 0) {
            if (isExpanded) {
                setShowUpto(4); 
            } else {
                setShowUpto(chatQuery.length); // Show all items on "See More"
            }
            setIsExpanded(!isExpanded); // Toggle expansion state
        }
    };

    return (
        <div className={style.chatDropDown}>
            {data.map((item, index) => (
                <div key={index}>
                    <div
                        className={style.chatHistoryHeadWithArrow}
                        onClick={() => toggleDropdown(index)}
                    >
                        <h3>{item.title}</h3>
                        {index !== 0 && showDropdownArrow && (
                            <div>
                                <img
                                    src={openDropdown.includes(index) ? arrowUp : arrowDown}
                                    alt="arrowIcon"
                                />
                            </div>
                        )}
                    </div>
                    <div
                        className={`${
                            openDropdown.includes(index) ? style.ActiveDropDown : style.InActiveDropDown
                        }`}
                    >
                        <ul>
                            {item.chatQuery.slice(0, showUpto).map((chat, chatIndex) => (
                                <span key={chatIndex} className={style.listOptions}>
                                    <li onClick={(e) => handleNavigateChatContext(e, chat.contextId)}>
                                        {chat?.message}
                                    </li>
                                </span>
                            ))}
                        </ul>
                        {Array.isArray(item.chatQuery) && item.chatQuery.length > 4 && index === 0 && (
                            <button
                                className={style.SeeMoreDropDown}
                                onClick={() => toggleVisibility(index, item.chatQuery)}
                            >
                                <span style={{ paddingTop: '6px' }}>
                                    <img
                                        src={isExpanded ? arrowUp : arrowDown}
                                        alt="arrowIcon"
                                    />
                                </span>
                                <span>{isExpanded ? 'Show Less' : 'See More'}</span>
                            </button>
                        )}
                    </div>
                </div>
            ))}
        </div>
    );
}
