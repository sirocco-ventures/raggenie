import React, { useEffect, useState } from 'react';
import style from './Auth.module.css';
import { useNavigate } from 'react-router-dom';
import { PiSmileySadLight } from "react-icons/pi";


const ErrorContainer = ({ message }) => {
    return (
        <div className={style.ErrorDiv}>
            <div className={style.WarningMessage}>
            <div className={style.SimileIcon}> <PiSmileySadLight color={"#FCBD73"} size={24}/> </div> <div> {message}</div>
            </div>
        </div>
    );
};

const BACKEND_LOGIN_URL = "http://localhost:8001/api/v1/auth/login";
const AuthLogin = () => {
    const navigate  = useNavigate()
    const[redirect,setRedirect] = useState(false)
    useEffect(() => {
        try {
              window.location.href = BACKEND_LOGIN_URL
        }catch(error){
            setRedirect(true)
            console.error('Failed to redirect to Zitadel')
        }
    } )

    return (
        <>
      </>
    );
};

export default AuthLogin;
