import style from "./UserAuth.module.css"
import logo from './assets/gennie-logo.svg';
import googleLogo from "./assets/googleLogo.svg"
import Input from 'src/components/Input/Input';
import Button from 'src/components/Button/Button';
import React, { useEffect, useState } from 'react';
import { useForm } from 'react-hook-form';
import { AuthLoginService, IdpLoginService } from 'src/services/Auth';

const UserLogin = () => {
    const { register: authRegister, setValue: authSetValue, handleSubmit: authHandleSubmit, formState: authFormState, setError: authSetError, clearErrors: authClearErrors, watch: authWatch } = useForm({ mode: 'all' });
    const { errors: authFormError } = authFormState;
    const [showError, setShowError] = useState(false);
    const [errorMessage, setErrorMessage] = useState('');
    

    const onSubmit = (data) => {
            const authCredentials = {
                "username": data.username,
                "password": data.password
            };
            AuthLoginService(authCredentials).then((response) => {
                const authResponse = response.data
                console.log(authResponse)
                // const token = authResponse.data.token
                // storeToken(token)
                // setIsAuthenticated(true)
                // toast.success(authResponse.message);
                // navigate(`/preview/${uuid4()}/chat`)
            }).catch(() => {
                setErrorMessage("Incorrect username or password. Please try again.");
                setShowError(true);
            });
        };

    return (
        <>
        {/* add div to display error */}
        <div className={style.AuthBackground}>
            <span style={{marginTop: "15px",color: "#3893FF",fontFamily: "Inter",fontSize: "14px"}}>Forgot password?</span>
            <div className={style.FieldContainer}>
                <img src={logo} alt="Genie Logo" />
                <h2 className={style.Welcome}>Welcome Back</h2>
                <p>Login to your Ragggenie account</p>
                <div style={{ width: "100%", backgroundColor: "#FFF"}}>
                        <form onSubmit={authHandleSubmit(onSubmit)}>
                            <Input
                                label="Email"
                                placeholder="Enter your email address"
                                hasError={authFormError.username?.message ? true : false}
                                errorMessage={authFormError.username?.message}
                                {...authRegister('username', { required: 'Username is required' })}
                            />

                            <Input
                                label="Password"
                                placeholder="Enter your password"
                                type="password"
                                hasError={authFormError.password?.message ? true : false}
                                errorMessage={authFormError.password?.message}
                                {...authRegister('password', { required: 'Password is required' })}
                            />
                            <div className={style.CheckBox}>
                                <input type="checkbox"></input>
                                <span>Remeber me</span>

                            </div>

                            <Button buttonType="submit" className={style.SubmitButton}>
                                Login
                            </Button>
                        </form>
                        <div className={style.OAuthLogin}>
                            <span className={style.OrLogin}>Or Login with</span>
                            <div className={style.LoginGoogle} onClick={IdpLoginService}>
                                <img src={googleLogo} />
                                <span>Login with Google</span>
                            </div>

                        </div>
                    </div>
            </div>
        </div>

        </>
    );
};

export default UserLogin;
