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
import { storeToken } from 'src/store/authStore';


const AuthLogin = () => {
    const [activeLoginButton,setActiveLoginButton] = useState(true)

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
            if (authResponse.status == true && authResponse.status_code == 200) {
                toast.success(authResponse.message);
                navigate(`/preview/${uuid4()}/chat`)
            }
        }).catch(() => {
            toast.error("Incorrect username or password. Please try again");
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
                    <div style={{ width: "100%", backgroundColor: "#FFF", paddingTop: "50px" }}>
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
