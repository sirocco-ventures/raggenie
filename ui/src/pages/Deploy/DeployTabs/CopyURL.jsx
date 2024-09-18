import React, { useRef, useState } from 'react'
import Input from 'src/components/Input/Input'
import style from './DeployTabs.module.css'
import { PiCopySimpleBold } from "react-icons/pi";
import Button from 'src/components/Button/Button';
import TitleDescription from 'src/components/TitleDescription/TitleDescription';
import preview from "src/assets/icons/preview-arrow.svg"


const CopyURL = () => {
    const[url,setUrl]= useState("https://www.raggenie.com/gshgadhsljvfsdggyeuhdjiaX")

    const CopyUrlRef = useRef(null)

    const handleCopyUrl=()=>{
       try {
        var copyText = CopyUrlRef.current.innerText;
        if(copyText){
        navigator.clipboard.writeText(copyText);
        }
       } catch (error) {
        console.log(error);
       }

    }
    return (
        <>
            <div>
                <TitleDescription showOrder={false} title={"Copy URL for live preview"} description={"Provide your database connection details and database data description can make your application more efficient."} />
            </div>
            <div className={`${style.CopyContainer}`}>
                <div className={`${style.CopyLinkContainer}`}>
                    <div className={`${style.CopyLinkInputBox}`}>
                        <div ref={CopyUrlRef} contentEditable={false} className={`${style.CopyText}`}>{url}</div><span onClick={handleCopyUrl} className={`${style.CopyNow}`}><span >Copy URL</span><PiCopySimpleBold size={18} /></span>
                    </div>
                </div>
                <Button buttonType="submit" className={`${style.ButtonClass}`}>Preview<img src={preview} alt="previewIcon"/></Button>
            </div>
        </>
    )
}

export default CopyURL