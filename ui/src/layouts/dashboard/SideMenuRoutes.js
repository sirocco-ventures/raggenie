
import previewIcon from "../../assets/icons/menu-icons/preview.svg"
import configIcon from "../../assets/icons/menu-icons/confiruration.svg"
import samplesIcon from "../../assets/icons/menu-icons/sample.svg"
import documentsIcon from "../../assets/icons/menu-icons/document.svg"
import deployIcon from "../../assets/icons/menu-icons/deploy.svg"
import pluginIcon from "../../assets/icons/menu-icons/plugin.svg"
import { v4 } from "uuid"

 const SideMenuRoutes = [

    {
        title: "Preview",
        path: `/preview/${v4()}/chat`,
        icon: previewIcon,
    },
    // {
    //     title: "Configuration",
    //     path: "/chat-configuration",
    //     icon: configIcon,
    // },
    {
        title: "Configuration ",
        path: "/bot-configuration",
        icon: configIcon,
    },
    {
        title: "Plugins",
        path: "/plugins",
        icon: pluginIcon,
    },
    {
        title: "Samples",
        path: "/samples",
        icon: samplesIcon,
    },
    // {
    //     title: "Documents",
    //     path: "/documents",
    //     icon: documentsIcon,
    // },
    {
        title: "Deploy",
        path: "/deploy",
        icon: deployIcon,
    }
  ]

  export  default SideMenuRoutes
