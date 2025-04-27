import CopyEmbedCode from "./DeployTabs/CopyEmbedCode";
import CopyURL from "./DeployTabs/CopyURL";
import MaximizedLayout from "./DeployTabs/MaximizedLayout";
import MinimizedLayout from "./DeployTabs/MinimizedLayout";

export const deployTabroutes = (currentConfigID) => [
  {
    title: "Get URL for live preview",
    path: "/copyURL",
    icon: "",
    page: <CopyURL />,
    isPrivate: true,
  },
  {
    title: "Copy Chatbot embed code",
    path: "/copyEmbedCode",  
    icon: "",
    page: <CopyEmbedCode currentConfigID={currentConfigID}/>,
    isPrivate: true,
  },
];

export const ChatBotEmbeddedCodeTabs = (currentConfigID) => [
  {
    title: "Minimized Layout",
    path: "/minimzedLayout",
    icon: "",
    page: <MinimizedLayout currentConfigID={currentConfigID}/>,
    isPrivate: true,
  },
  {
    title: "Expanded Layout",
    path: "/maximizedLayout",  
    icon: "",
    page: <MaximizedLayout currentConfigID={currentConfigID}/>,
    isPrivate: true,
  },
];
