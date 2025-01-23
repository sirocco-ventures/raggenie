import React, {useState, useRef} from "react";
import style from "./Table1.module.css";
import expandIcon from "./assets/tableExpandIcon.svg";
import collapseIcon from "./assets/tableCollapseIcon.svg";
import tableIcon from "./assets/table.svg"
import pencilIcon from "./assets/pencil.svg"
import Textarea from "../Textarea/Textarea";


function Table1({data}) {
    const [expandedRows, setExpandedRows] = useState({});
    const [expandedColRows, setExpandedColRows] = useState({});
    const textAreaRefs = useRef({});
    const colTextAreaRefs = useRef({});

    const toggleRow = (id,event) => {
      setExpandedRows(prev => ({
        ...Object.fromEntries(Object.keys(prev).map(k => [k, false])),
        [id]: !prev[id]
      }));

      const items = document.querySelectorAll(`[data-key]`); 
      items.forEach((item) => {
        if (item.getAttribute("data-key") === id ) {
          item.style.display = item.style.display === "block" ? "none" : "block";
        } else {
          item.style.display = "none";
        }
      });
      if (event) {
        event.target.parentNode.nextElementSibling.firstChild.lastChild.focus();
      }
    };

    const toggleColRow = (id,event) => {
      setExpandedColRows(prev => ({
        ...Object.fromEntries(Object.keys(prev).map(k => [k, false])),
        [id]: !prev[id]
      }));
      const items = document.querySelectorAll(`[data-col-key]`); // Select all elements with the data-key attribute
    
      items.forEach((item) => {
        if (item.getAttribute("data-col-key") === id) {
          item.style.display = item.style.display === "block" ? "none" : "block";
        } else {
          item.style.display = "none";
        }
      });
      if (event) {
        event.target.parentNode.nextElementSibling.lastChild.focus();
      }
    };

    const handleDescriptionChange = (event,id) => {
      const newDescription = event.target.value;
      // Update local storage
      const dbSchema = JSON.parse(localStorage.getItem('dbschema') || '{}');
      if (dbSchema[id]) {
        dbSchema[id].description = newDescription;
        localStorage.setItem('dbschema', JSON.stringify(dbSchema));
      }
    };
    return (
      <div className={style.tableContainer}>
          <div className={style.tableHeader}>NAME</div>
          {data.map((item, index) => (
            <div key={index}>
              <div className={`${style.rowTitle} ${expandedRows[item.table_id] ? style.tdOnfocus : ""}`}>
                  <div>
                      <img src={expandedRows[item.table_id] ? collapseIcon : expandIcon} onClick={() => toggleRow(item.table_id)}/>
                      <img src={tableIcon}/>
                      {item.table_name}
                  </div>
                  <img src={pencilIcon} onClick={(event) => toggleRow(item.table_id,event)}/>
              </div>
                <div>
                  <div className={style.descriptionContainer} data-key={item.table_id} style={{display: "none"}}>
                        <span>Description</span>
                        <textarea
                          ref={(el) => (textAreaRefs.current[index] = el)}
                          className={style.descriptionTextarea}
                          defaultValue={item.description} 
                          onChange={(event) => handleDescriptionChange(event,item.table_id)}
                        />
                  </div>
                  {item.columns.map((column, colIndex) => (
                    <div className={style.dbColumnContainer} key={colIndex} data-key={item.table_id} style={{display: "none"}}>
                      <div className={`${style.dbColumnTd} ${style.rowTitle} ${expandedColRows[column.column_id] ? style.colOnfocus : ""}`} >
                         <div>
                            <img src={expandedColRows[column.column_id] ? collapseIcon : expandIcon} onClick={() => toggleColRow(column.column_id)}/>
                            <img src={tableIcon}/> 
                            {column.column_name} 
                          </div>
                          <img src={pencilIcon} onClick={(event) => toggleColRow(column.column_id,event)}/>
                      </div>
                         <div className={`${style.descriptionContainer} ${style.coldescription}`} data-col-key={column.column_id} style={{display: "none"}}>
                          <span>Description</span>
                          <textarea
                            ref={(el) => (colTextAreaRefs.current[colIndex] = el)}
                            className={style.descriptionTextarea}
                          />
                         </div>
                    </div>
                  ))}
                </div>
            </div>
          ))}
      </div>
  );
}



export default Table1;