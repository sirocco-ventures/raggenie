import CodeBlock from 'src/components/CodeBlock/CodeBlock'
import TitleDescription from 'src/components/TitleDescription/TitleDescription'
import style from './DeployTabs.module.css'
import Screenshot from "src/assets/images/screen_shot.svg"
import { API_URL } from "src/config/const"

const MinimizedLayout = () => {

    return (
        <>
            <TitleDescription showOrder={false} title='Copy code for Minimized Layout' description='Experience a rich view environment with the minimized view' />
            <div className={style.MiniMaxContainer}>
                <div className={style.SubContents}>
                <CodeBlock codeString={`<script>
(function injectChatbot() {
    const script = document.createElement('script');
    script.src = 'http://${window.location.host}/dist-library/chatbox.js';
    script.type = 'text/javascript';
    script.onload = function () {
    const container = document.createElement('div');
    container.id = 'chatbox-container';
    document.body.appendChild(container);
    if (ChatBot.mountChatbox) {
        ChatBot.mountChatbox('chatbox-container', {
        apiURL: '${API_URL}',
        });
    } else {
        console.error('ChatBot object is not defined.');
    }
    };
    document.head.appendChild(script);
})();
</script>`} />
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

export default MinimizedLayout