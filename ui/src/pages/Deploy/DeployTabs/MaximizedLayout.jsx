import React from 'react'
import CodeBlock from 'src/components/CodeBlock/CodeBlock'
import TitleDescription from 'src/components/TitleDescription/TitleDescription'
import style from './DeployTabs.module.css'
import Screenshot from "src/assets/images/screen_shot.svg"

const MaximizedLayout = (       { Codestyle }) => {
    return (
        <>
            <TitleDescription showOrder={false} title='Copy code for Maximized Layout' description='Experience a rich view environment with the minimized view' />
            <div className={style.MiniMaxContainer}>
                <div className={style.SubContents}>
                    <CodeBlock codeString={`window.raggenie("boot", {
  api_base: "https://api-iam.raggenie.com",
  app_id: "tyx1oo1f",
  user_id: user.id, // IMPORTANT: Replace "user.id" with the variable you use to capture the user's ID
  name: user.name, // IMPORTANT: Replace "user.name" with the variable you use to capture the user's name
  email: user.email, // IMPORTANT: Replace "user.email" with the variable you use to capture the user's email address
  created_at: user.raggenie, // IMPORTANT: Replace "user.raggenie" with the variable you use to capture the user's sign-up date
});`} />
                </div>
                <div className={style.SubContents}>
                    <img src={Screenshot} alt="raggnie UI" />
                </div>

                <div>

                </div>
            </div>
        </>
    )
}

export default MaximizedLayout