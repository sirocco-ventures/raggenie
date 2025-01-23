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
    const toggleRow = (index,focus=false) => {
      setExpandedRows((prev) => {
        const newExpandedRows = Object.keys(prev).reduce((acc, key) => {
          acc[key] = false;
          return acc;
        }, {});
        newExpandedRows[index] = !prev[index];
        return newExpandedRows;
      });
      if (focus) {
        setTimeout(() => {
          textAreaRefs.current[index]?.focus(); // Focus the textarea
        }, 0);
      }
    };
    const toggleColRow = (index,focus=false) => {
      setExpandedColRows((prev) => {
        const newExpandedColRows = Object.keys(prev).reduce((acc, key) => {
          acc[key] = false;
          return acc;
        }, {});
        newExpandedColRows[index] = !prev[index];
        return newExpandedColRows;
      });
      if (focus) {
        setTimeout(() => {
          colTextAreaRefs.current[index]?.focus(); // Focus the textarea
        }, 0);
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
        <table className={style.table}>
        <thead>
            <tr>
            <th>NAME</th>
            </tr>
        </thead>
        <tbody>
            {data.map((item, index) => (
              <React.Fragment key={index}>
              <tr>
                <td className={`${expandedRows[index] ? style.tdOnfocus : ""}`}>
                    <div>
                        <img src={expandedRows[index] ? collapseIcon : expandIcon} onClick={() => toggleRow(index)}></img>
                        <img src={tableIcon}></img>
                        {item.table_name}
                    </div>
                    <img src={pencilIcon} onClick={() => toggleRow(index,true)}></img>
                </td>
            </tr>
            {expandedRows[index] && (
              <div>
                <div className={style.descriptionContainer}>
                      <span>Description</span>
                      <textarea
                        ref={(el) => (textAreaRefs.current[index] = el)}
                        className={style.descriptionTextarea}
                        defaultValue={item.description || JSON.parse(localStorage.getItem('dbschema') || '{}')[item.table_id].description} 
                        onChange={(event) => handleDescriptionChange(event,item.table_id)}
                      ></textarea>
                    </div>
                {item.columns.map((column, colIndex) => (
                  <div className={style.dbColumnContainer}>
                    <td className={style.dbColumnTd}>
                       <div>
                          <img src={expandedColRows[colIndex] ? collapseIcon : expandIcon} onClick={() => toggleColRow(colIndex)}></img>
                          <img src={tableIcon}></img> 
                          {column.column_name} 
                        </div>
                        <img src={pencilIcon} onClick={() => toggleColRow(colIndex,true)}></img>
                       </td>
                       {expandedColRows[colIndex] && (
                         <div className={style.descriptionContainer}>
                          <span>Description</span>
                          <textarea
                            ref={(el) => (colTextAreaRefs.current[colIndex] = el)}
                            className={style.descriptionTextarea}
                          ></textarea>
                         </div>
                       )} 

                  </div>
                ))}
              </div>
              )}
            </React.Fragment>
            ))}
        </tbody>
        </table>
    </div>
    );
}



export default Table1;