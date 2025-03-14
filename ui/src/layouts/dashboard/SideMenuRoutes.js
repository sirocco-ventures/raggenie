
import previewIcon from "../../assets/icons/menu-icons/preview.svg"
import configIcon from "../../assets/icons/menu-icons/confiruration.svg"
import samplesIcon from "../../assets/icons/menu-icons/sample.svg"
import deployIcon from "../../assets/icons/menu-icons/deploy.svg"
import pluginIcon from "../../assets/icons/menu-icons/plugin.svg"
import { v4 } from "uuid"

 const SideMenuRoutes = [

    {
        title: "Preview",
        path: `/preview/${v4()}/chat`,
        icon: previewIcon,
    },
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
    //     title: "Deploy",
    //     path: "/deploy",
    //     icon: deployIcon,
    // }
  ]

  export  default SideMenuRoutes
