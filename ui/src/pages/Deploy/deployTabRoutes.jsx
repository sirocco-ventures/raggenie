import CopyEmbedCode from "./DeployTabs/CopyEmbedCode";
import CopyURL from "./DeployTabs/CopyURL";
import MaximizedLayout from "./DeployTabs/MaximizedLayout";
import MinimizedLayout from "./DeployTabs/MinimizedLayout";

export const deployTabroutes = [
  {
    title: "Get URL for live preview",
    path: "/copyURL",
    icon: "",
    page: <CopyURL />,
    isPrivate: true,
  },
  {
    title: "Copy Chatbot embed code",
    path: "/Copyembedcode",  // Fixed the typo from 'Copyembeedcode' to 'Copyembedcode'
    icon: "",
    page: <CopyEmbedCode />,
    isPrivate: true,
    disabled: true
  },
];

export const ChatBotEmbeddedCodeTabs = [
  {
    title: "Minimized Layout",
    path: "/copyURL",
    icon: "",
    page: <MinimizedLayout/>,
    isPrivate: true,
  },
  {
    title: "Expanded Layout",
    path: "/Copyembedcode",  // Fixed the typo here as well
    icon: "",
    page: <MaximizedLayout/>,
    isPrivate: true,
  },
];
