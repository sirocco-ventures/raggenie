import Sources from "src/pages/Sources/Sources";
import Configuration from "src/pages/Configuration/Configuration"
import Deploy from "src/pages/Deploy/Deploy";
import Preview from "src/pages/Preview/Preview";
import Samples from "src/pages/Samples/Samples";
import ChatConfiguration from "src/pages/ChatConfiguration/ChatConfigurationForm";
import ProviderForm from "src/pages/Configuration/ProviderForm/ProviderForm";
import BotConfiguration from "src/pages/ChatConfiguration/ChatConfigurationForm";
import Chat from "src/pages/Chat/Chat";
import NotFound from "src/layouts/errorPage/404";
import ServerError from 'src/layouts/errorPage/500';
import ChatConfigurationMain from "src/pages/ChatConfiguration/ChatConfiguration";

const  routes = [

    {
        title: "chatContext",
        path: "/preview/:contextId/chat",
        icon: "",
        page: <Preview/>,
        isPrivate: true
    },
    {
        title: "Plugins",
        path: "/plugins",
        icon: "",
        page: <Configuration/>,
        isPrivate: true
    },
    {
        title: "Samples",
        path: "/samples",
        icon: "",
        page: <Samples/>,
        isPrivate: true
    },
   
    // {
    //     title: "Deploy",
    //     path: "/deploy",
    //     icon: "",
    //     page: <Deploy/>,
    //     isPrivate: true
    // },
    {
        title: "Sources",
        path: "/plugins/sources",
        icon: "",
        page: <Sources/>,
        isPrivate: true
    },
    

    {
        title: "Provide Form",
        path: "/plugins/:providerId/:providerName",
        icon: "",
        page: <ProviderForm/>,
        isPrivate: true
    },

    {
        title: "Provide Form",
        path: "/plugins/:providerId/:providerName/:connectorId/details",
        icon: "",
        page: <ProviderForm/>,
        isPrivate: true
    },

    {
        title: "Chat Configuration",
        path: "/chat-configuration",
        icon: "",
        page: <ChatConfiguration/>,
        isPrivate: true
    },
    {
        title: "Bot Configuration",
        path: "/bot-configuration",
        icon: "",
        page: <ChatConfigurationMain/>,
        isPrivate: true
    },
    {
        title: "Bot Configuration",
        path: "/bot-configuration/sources",
        icon: "",
        page: <BotConfiguration/>,
        isPrivate: true
    },
    {
        title: "Bot Configuration",
        path: "/bot-configuration/:configId",
        icon: "",
        page: <BotConfiguration/>,
        isPrivate: true
    },
    {
        title: "Not Found",
        path: "*",  
        icon: "",
        page: <NotFound />, 
        isPrivate: false
    },
    {
        title: "Server Error",
        path: "/error",  
        icon: "",
        page: <ServerError />, 
        isPrivate: false
    },
  ]

  export default routes