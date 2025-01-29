import React, { useEffect, useState } from 'react';
import { useForm } from 'react-hook-form';
import style from './Auth.module.css';
import logo from './assets/gennie-logo.svg';
import Input from 'src/components/Input/Input';
import Button from 'src/components/Button/Button';
import { AuthLoginService } from 'src/services/Auth';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';
import GeneralLayout from '../general/GeneralLayout';
import { v4  as uuid4} from "uuid"
import useAppSettings, { storeToken } from 'src/store/authStore';
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
