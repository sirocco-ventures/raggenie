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

const AuthLogin = () => {
    const [activeLoginButton,setActiveLoginButton] = useState(true)

    const [showError, setShowError] = useState(false);
    const [errorMessage, setErrorMessage] = useState('');

    const { register: authRegister, setValue: authSetValue, handleSubmit: authHandleSubmit, formState: authFormState, setError: authSetError, clearErrors: authClearErrors, watch: authWatch } = useForm({ mode: 'all' });

    const { errors: authFormError } = authFormState;

    const navigate = useNavigate()

    const onSubmit = (data) => {
        const authCredentials = {
            "username": data.username,
            "password": data.password
        };
        AuthLoginService(authCredentials).then((response) => {
            const authResponse = response.data
            const token = authResponse.data.token
            storeToken(token)
            toast.success(authResponse.message);
            navigate(`/preview/${uuid4()}/chat`)
        }).catch(() => {
            setErrorMessage("Incorrect username or password. Please try again.");
            setShowError(true);
        });
    };


    return (
        <>
        <GeneralLayout>
           <div className={style.AuthBackground}>
                <div className={style.FIeldContainer}>
                    <img src={logo} alt="Gennie Logo" />
                    <h2 className={style.Welcome}>Welcome Back</h2>
                    <p>Login to your Ragggenie account</p>
                    {showError && <ErrorContainer message={errorMessage} />}
                    <div style={{ width: "100%", backgroundColor: "#FFF"}}>
                        <form onSubmit={authHandleSubmit(onSubmit)}>
                            <Input
                                label="Username"
                                hasError={authFormError.username?.message ? true : false}
                                errorMessage={authFormError.username?.message}
                                {...authRegister('username', { required: 'Username is required' })}
                            />

                            <Input
                                label="Password"
                                type="password"
                                hasError={authFormError.password?.message ? true : false}
                                errorMessage={authFormError.password?.message}
                                {...authRegister('password', { required: 'Password is required' })}
                            />

                            <Button disabled={!activeLoginButton} buttonType="submit" className={style.SubmitButton}>
                                Login
                            </Button>
                        </form>
                    </div>
                </div>
            </div> 
        </GeneralLayout>
            
        </>
    );
};

export default AuthLogin;
