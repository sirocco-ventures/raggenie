import style from "./UserAuth.module.css"
import logo from './assets/gennie-logo.svg';
import googleLogo from "./assets/googleLogo.svg";
import githubLogo from "./assets/githubLogo.svg"
import Input from 'src/components/Input/Input';
import Button from 'src/components/Button/Button';
import React, { useEffect, useState } from 'react';
import { useForm } from 'react-hook-form';
import { AuthLoginService, IdpLoginService, GetIdpList } from 'src/services/Auth';
import { useNavigate } from "react-router-dom";
import { v4 as uuid4 } from "uuid"
import { toast } from "react-toastify";



const UserLogin = () => {
    const { register: authRegister, setValue: authSetValue, handleSubmit: authHandleSubmit, formState: authFormState, setError: authSetError, clearErrors: authClearErrors, watch: authWatch } = useForm({ mode: 'all' });
    const { errors: authFormError } = authFormState;
    const [showError, setShowError] = useState(false);
    const [errorMessage, setErrorMessage] = useState('');
    const [idpList, setIdpList] = useState([]);
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate()

    useEffect(() => {
        GetIdpList().then(response => {
            setIdpList(response.data.idp_list);
        }).catch(error => {
            console.error("failed to fetch idp list", error);
        })
    }, []);

    function capitalizeFirstLetter(str) {
        return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase();
    }
    
    /* fucntion to render idp buttons dynamically */

    const renderIdpButtons = () => {
        return idpList?.slice(0,1).map((idp) => {
            let logo = idp.type === "PROVIDER_TYPE_GOOGLE" ? googleLogo : 
                       idp.type === "PROVIDER_TYPE_GITHUB" ? githubLogo : null;
            return (
                <div key={idp.id} className={style.LoginGoogle} onClick={() => IdpLoginService(idp.id)}>
                    {logo && <img src={logo} alt={idp.type} />}
                    <span>Login with {capitalizeFirstLetter(idp.type.replace("PROVIDER_TYPE_", ""))}</span>
                </div>
            );
        });
    };

    const onSubmit = (data) => {
            setLoading(true);
            const authCredentials = {
                "username": data.username,
                "password": data.password
            };
            AuthLoginService(authCredentials).then((response) => {
                const authResponse = response.data
                console.log("authResponse", authResponse)
                toast.success("Login successful");
                navigate(`/preview/${uuid4()}/chat`)
                setLoading(false);
                // const token = authResponse.data.token
                // storeToken(token)
                // setIsAuthenticated(true)
            }).catch(() => {
                setErrorMessage("Incorrect username or password. Please try again.");
                setShowError(true);
                setLoading(false);
            });
        };

    return (
        <>
        {/* add div to display error */}
        <div className={style.AuthBackground}>
            {/* <span style={{marginTop: "15px",color: "#3893FF",fontFamily: "Inter",fontSize: "14px"}}>Forgot password?</span> */}
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
                                {loading ? <span className={style.loader}></span> : "Login"}
                            </Button>
                        </form>
                        <div className={style.OAuthLogin}>
                            <span className={style.OrLogin}>Or Login with</span>
                            {renderIdpButtons()}

                        </div>
                    </div>
            </div>
        </div>

        </>
    );
};

export default UserLogin;
