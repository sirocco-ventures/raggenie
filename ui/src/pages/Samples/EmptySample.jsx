import Button from "src/components/Button/Button"
import { HiOutlinePlusCircle } from "react-icons/hi";
import emptySampleImg from "./assets/empty-icon.svg"
import style from "./Samples.module.css"

const EmptySample = ( {onCreateClick = ()=>{}} )=>{

    return(
        <>
            <div className={style.EmptySample}>
                    <div> <img src={emptySampleImg}/> </div>
                    <div><p>You don't have any samples created, to get started <br/> go and add a sample</p> </div>
                    <div> <Button onClick={onCreateClick}>Create Sample <HiOutlinePlusCircle/></Button> </div>
            </div>
        </>
    )
}

export default EmptySample