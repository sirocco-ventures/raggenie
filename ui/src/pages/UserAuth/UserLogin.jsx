import style from "./UserAuth.module.css"
import logo from './assets/gennie-logo.svg';
import googleLogo from "./assets/googleLogo.svg"
import Input from 'src/components/Input/Input';
import Button from 'src/components/Button/Button';


const UserLogin = () => {


    return (
        <>
        <div className={style.AuthBackground}>
            <span style={{marginTop: "15px",color: "#3893FF",fontFamily: "Inter",fontSize: "14px"}}>Forgot password?</span>
            <div className={style.FieldContainer}>
                <img src={logo} alt="Genie Logo" />
                <h2 className={style.Welcome}>Welcome Back</h2>
                <p>Login to your Ragggenie account</p>
                <div style={{ width: "100%", backgroundColor: "#FFF"}}>
                        <form>
                            <Input
                                label="Email"
                                placeholder="Enter your email address"
                            />

                            <Input
                                label="Password"
                                placeholder="Enter your password"
                                type="password"
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
                            <div className={style.LoginGoogle}>
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
