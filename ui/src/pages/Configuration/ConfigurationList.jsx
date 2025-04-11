// ConfigurationList.jsx

import React from "react";
import SearchInput from "src/components/SearchInput/SearchInput";
import Table from "src/components/Table/Table";
import Tag from "src/components/Tag/Tag";
import { GoPencil } from "react-icons/go";
import { HiOutlinePlusCircle } from "react-icons/hi";
import { LuTrash2 } from "react-icons/lu";
import Button from "src/components/Button/Button";
import style from "./Configuration.module.css";
import { Link } from "react-router-dom";
import { BACKEND_SERVER_URL } from "src/config/const";
import confirmDialog from "src/utils/ConfirmDialog";

const ConfigurationList = ({ configurations = [], onPluginDelete }) => {

  const handleDelete = (pluginId) => {
    confirmDialog(
      "Confirmation",
      "Are you sure you want to delete this?",() => {
        onPluginDelete(pluginId);
      }
    );
  };


  let tableColumns = [

    {
        name: 'Name',
        selector: row =><div className="inline-flex-align-center"><img  className={style.ConnectorIcon} src={`${BACKEND_SERVER_URL}${row.icon}`}/>  { row.connector_name} </div>,
        // width: "400px"
    },
    {
        name: 'Description',
        // selector: row => row.connector_description?.slice(0,60) + "...",
        selector: row => <div style={{overflow: "hidden", width: "calc(50vh)"}}>{row.connector_description}</div>
    },
    {
        name: 'Status',
        selector: row => <Tag type="success">{row.enable ==  true ? "Completed" : "Documention Pending"}</Tag>,
        width: "200px"
    },
    {
        name: '',
        selector: row => <>
                <div className={style.ConnectorAction}>
                    <span>
                        <Link to={`/plugins/${row.connector_type}/${row.connector_key}/${row.connector_id}/details`} ><GoPencil size={20} color="#3893FF" /> </Link>
                    </span>
                    {/* <span>
                        <TbMessagePlus size={20} color="#3893FF"/>
                    </span> */}
                    <span>
                    <LuTrash2 size={20} onClick={() => handleDelete(row.connector_id)} color="#FF7F6D" />

                    </span>
                </div>

        </>,
        width: "200px"
    }

]
  return(
    <>
        <div>
            <div className={` ${style.SearchContainer}`}>
                <div className="flex-grow-1">
                    <SearchInput style={{width: "349px"}}/>
                </div>
                <div>
                    <Link to={"/plugins/sources"}>
                        <Button className="icon-button">Add Plugins <HiOutlinePlusCircle/> </Button>
                    </Link>
                </div>
            </div>
            <Table columns={tableColumns} data={configurations} />
        </div>

    </>
)
}

export default ConfigurationList
