import React, { useEffect } from 'react';
import { useForm } from 'react-hook-form';
import style from './Auth.module.css';
import logo from './assets/gennie-logo.svg';
import Input from 'src/components/Input/Input';
import Button from 'src/components/Button/Button';
import { AuthService } from 'src/services/Auth';

const AuthLogin = () => {
    // Initialize useForm for form handling
    const { register: authRegister, setValue: authSetValue, handleSubmit: authHandleSubmit, formState: authFormState, setError: authSetError, clearErrors: authClearErrors, watch: authWatch } = useForm({ mode: 'all' });

    const { errors: authFormError } = authFormState;



    // Handle form submission
    const onSubmit = (data) => {
        const authCredentials ={
            "username": data.username,
            "password": data.password
        }
        AuthService(authCredentials)
    };

    return (
        <>
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

                            <Button buttonType="submit" className={style.SubmitButton}>
                                Login
                            </Button>
                        </form>
                    </div>
                </div>
            </div>
        </>
    );
};

export default AuthLogin;
