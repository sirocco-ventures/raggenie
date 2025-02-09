import style from "./UserAuth.module.css"
import logo from './assets/gennie-logo.svg';
import googleLogo from "./assets/googleLogo.svg"
import Input from 'src/components/Input/Input';
import Button from 'src/components/Button/Button';


const UserSignUp = () => {


    return (
        <>
        <div className={style.AuthBackground}>
            <div className={style.FieldContainer}>
                <img src={logo} alt="Genie Logo" />
                <h2 className={style.Welcome}>Welcome Back</h2>
                <p>Login to your Ragggenie account</p>
                <div style={{ width: "100%", backgroundColor: "#FFF"}}>
                        <form>
                            <Input
                                label="Name"
                                placeholder="Enter your name"
                            />
                            <Input
                                label="Last Name"
                                placeholder="Enter your last name"
                            />
                            <Input
                                label="Email"
                                placeholder="Enter you email address"
                            />
                            <Input
                                label="Password"
                                placeholder="Enter your password"
                                type="password"
                            />
                            <Input
                                label="Confirm Password"
                                placeholder="Confirum your password"
                                type="password"
                            />
                            <div className={style.CheckBox}>
                                <input type="checkbox"></input>
                                <span>I accept the term and the privacy policy</span>

                            </div>

                            <Button buttonType="submit" className={style.SubmitButton}>
                                Sign Up
                            </Button>
                        </form>
                        <div className={style.OAuthLogin}>
                            <span className={style.OrLogin}>Or Sign up with</span>
                            <div className={style.LoginGoogle}>
                                <img src={googleLogo} />
                                <span>Sign up with Google</span>
                            </div>

                        </div>
                    </div>
            </div>
        </div>

        </>
    );
};

export default UserSignUp;
