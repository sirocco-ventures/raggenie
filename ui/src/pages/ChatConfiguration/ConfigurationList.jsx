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

const ConfigurationList = ({ configurations = [], onConfigDelete }) => {

  const handleDelete = (config_id) => {
    confirmDialog(
        "Confirmation",
        "Are you sure you want to delete this?",
        () => {
          onConfigDelete(config_id);
        }
      );
  };


  let tableColumns = [

    {
        name: 'Name',
        selector: row =><div className="inline-flex-align-center">{row.name}</div>,
        // width: "400px"
    },
    {
        name: 'Description',
        // selector: row => row.connector_description?.slice(0,60) + "...",
        selector: row => <div style={{overflow: "hidden", width: "calc(50vh)"}}>{row.short_description}</div>
    },
    {
        name: '',
        selector: row => <>
                <div className={style.ConnectorAction}>
                    <span>
                        <Link to={`/bot-configuration/${row.id}`} ><GoPencil size={20} color="#3893FF" /> </Link>
                    </span>
                    {/* <span>
                        <TbMessagePlus size={20} color="#3893FF"/>
                    </span> */}
                    <span>
                    <LuTrash2 size={20} onClick={() => handleDelete(row.id)} color="#FF7F6D" />

                    </span>
                </div>

        </>,
        width: "100px"
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
                    <Link to={"/bot-configuration/sources"}>
                        <Button className="icon-button">Add New <HiOutlinePlusCircle/> </Button>
                    </Link>
                </div>
            </div>
            <Table columns={tableColumns} data={configurations} />
        </div>

    </>
)
}

export default ConfigurationList
