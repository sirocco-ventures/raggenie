import emptyConfiguationImg from "src/assets/images/empty-configuration.svg"
import style from "./Preview.module.css"
import Button from "src/components/Button/Button"
import { HiOutlinePlusCircle } from "react-icons/hi";
import { FaRegArrowAltCircleRight } from "react-icons/fa";
import restartIcon from "src/assets/icons/restart.svg"
import { Link } from "react-router-dom";

const EmptyPreview = ({currentState = 1, onRestartBot = ()=>{}})=>{

    return(
        <>
            <div className={style.EmptyDataContainer}>
                <div className={style.EmptyDataHeader}>
                    <h1 className={style.EmptyDataHeading}>Set Up Your Bot in 3 Easy Steps</h1>
                    <p className={style.EmptyDataParagraph}>Easily configure and launch your AI. Connect data, customize, and embed it for instant use</p>
                </div>
                <div className={style.StatusTimelimeContainer}>
                    <ul className={style.StatusTimeline}>
                        <li data-index="1"  className={currentState == 1 ? style.Current: currentState > 1 ? style.Completed : ""}>

                            <div className={style.StatusTimelineContent}>
                                <h6 className={style.StatusTimelineTitle}>Add Plugin</h6>
                                <div className={currentState != 1 ? style.StatusTimelineContentHide : ""}>
                                    <p className={style.StatusTimelineDescription}>You don't have any plugins added, click here to add one.</p>
                                    <Link to={"/plugins"}>
                                        <Button>Connect Plugin <HiOutlinePlusCircle size={22}/></Button>
                                    </Link>
                                </div>
                               
                            </div>

                        </li>
                        <li data-index="2" className={currentState == 2 ? style.Current: currentState > 2 ? style.Completed : ""} >
                            <div className={style.StatusTimelineContent}>
                                <h6 className={style.StatusTimelineTitle}>Bot Configuration</h6>
                                <div className={`${currentState != 2 ? style.StatusTimelineContentHide : ""}`}>
                                    <p className={style.StatusTimelineDescription}>Your chatbot configuration is incomplete.</p>
                                    <Link to={"/bot-configuration"}>
                                        <Button>Go to Bot Configuration <FaRegArrowAltCircleRight size={18}/></Button>
                                    </Link>
                                </div>
                            </div>

                        </li>
                        <li data-index="3" className={currentState == 3 ? style.Current: currentState > 3 ? style.Completed : ""}>
                            <div className={style.StatusTimelineContent}>
                                <h6 className={style.StatusTimelineTitle}>Restart Bot</h6>
                                <div className={`${currentState != 3 ? style.StatusTimelineContentHide : ""}`}>
                                    <p className={style.StatusTimelineDescription}>Please restart your chatbot to see recent configuration.</p>
                                    <Button onClick={onRestartBot} >Restart Chatbot <img src={restartIcon}/> </Button>
                                </div>
                            </div>

                        </li>
                    </ul>
                </div>
            </div>
        </>
    )
}

export default EmptyPreview