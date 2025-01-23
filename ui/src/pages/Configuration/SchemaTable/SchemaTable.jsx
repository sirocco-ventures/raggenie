import React, { useState, useRef, useMemo } from "react";
import style from "./SchemaTable.module.css";
import expandIcon from "./assets/tableExpandIcon.svg";
import collapseIcon from "./assets/tableCollapseIcon.svg";
import tableIcon from "./assets/table.svg";
import pencilIcon from "./assets/pencil.svg";
import leftIcon from "./assets/ChevronLeft.svg"
import rightIcon from "./assets/ChevronRight.svg"


function SchemaTable({data, itemsPerPage = 8}) {
    const [expandedRows, setExpandedRows] = useState({});
    const [expandedColRows, setExpandedColRows] = useState({});
    const [currentPage, setCurrentPage] = useState(1);
    const textAreaRefs = useRef({});
    const colTextAreaRefs = useRef({});

    // Pagination logic
    const paginatedData = useMemo(() => {
        const startIndex = (currentPage - 1) * itemsPerPage;
        return data.slice(startIndex, startIndex + itemsPerPage);
    }, [data, currentPage, itemsPerPage]);

    const totalPages = Math.ceil(data.length / itemsPerPage);

    const toggleRow = (id, event) => {
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

    const toggleColRow = (id, event) => {
        setExpandedColRows(prev => ({
            ...Object.fromEntries(Object.keys(prev).map(k => [k, false])),
            [id]: !prev[id]
        }));
        const items = document.querySelectorAll(`[data-col-key]`);
    
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

    const handleDescriptionChange = (event, id) => {
        const newDescription = event.target.value;
        const dbSchema = JSON.parse(localStorage.getItem('dbschema') || '{}');
        if (dbSchema[id]) {
            dbSchema[id].description = newDescription;
            localStorage.setItem('dbschema', JSON.stringify(dbSchema));
        }
    };

    const handlePageChange = (newPage) => {
        setCurrentPage(newPage);
        setExpandedRows({});
        setExpandedColRows({});
        const rowItems = document.querySelectorAll(`[data-key]`);
        const colItems = document.querySelectorAll(`[data-col-key]`);
        [...rowItems, ...colItems].forEach(item => {
            item.style.display = "none";
        });
    };

    return (
        <div className={style.tableContainer}>
            <div className={style.tableHeader}>NAME</div>
            {paginatedData.map((item, index) => (
                <div key={item.table_id}>
                    <div className={`${style.rowTitle} ${expandedRows[item.table_id] ? style.tdOnfocus : ""}`}>
                        <div>
                            <img src={expandedRows[item.table_id] ? collapseIcon : expandIcon} onClick={() => toggleRow(item.table_id)}/>
                            <img src={tableIcon}/>
                            {item.table_name}
                        </div>
                        <img src={pencilIcon} onClick={(event) => toggleRow(item.table_id, event)}/>
                    </div>
                    <div>
                        <div className={style.descriptionContainer} data-key={item.table_id} style={{display: "none"}}>
                            <span>Description</span>
                            <textarea
                                ref={(el) => (textAreaRefs.current[index] = el)}
                                className={style.descriptionTextarea}
                                defaultValue={item.description} 
                                onChange={(event) => handleDescriptionChange(event, item.table_id)}
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
                                    <img src={pencilIcon} onClick={(event) => toggleColRow(column.column_id, event)}/>
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
            
            {/* Pagination Controls */}
            <div className={style.paginationContainer}>
              <button 
                onClick={() => handlePageChange(currentPage - 1)} 
                disabled={currentPage === 1}
              >
                <img src={leftIcon}></img>
              </button>

              {/* Page Numbers */}
              {[...Array(totalPages)].map((_, index) => (
                <button
                  key={index}
                  onClick={() => handlePageChange(index + 1)} 
                  className={currentPage === index + 1 ? style.activePage : ""}
                >
                  {index + 1}
                </button>
              ))}

              <button 
                onClick={() => handlePageChange(currentPage + 1)} 
                disabled={currentPage === totalPages}
              >
                <img src={rightIcon}></img>
              </button>
            </div>

        </div>
    );
}

export default SchemaTable;